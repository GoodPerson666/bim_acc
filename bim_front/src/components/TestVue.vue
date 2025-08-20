<template>
  <!-- 3D 画布 -->
  <div ref="containerRef" class="viewport"></div>

  <!-- 顶部操作栏 -->
  <div class="top-bar">
    <el-upload
        class="upload-btn"
        accept=".ifc"
        :show-file-list="false"
        :before-upload="beforeUpload"
    >
      <el-button type="primary" plain>上传 IFC</el-button>
    </el-upload>

    <el-button-group>
      <el-button type="success" plain @click="getCompliance">合规</el-button>
      <el-button type="danger" plain @click="getNonCompliance">不合规</el-button>
      <el-button type="info" plain @click="getNormal">不适用</el-button>
      <el-button type="primary" plain @click="clearColor">清空</el-button>
    </el-button-group>
  </div>

  <!-- 固定右侧控制面板（非抽屉） -->
  <aside class="control-card" v-if="!isMobile || showPanel">
    <div class="card-header">
      <span>模型信息</span>
      <el-button
          v-if="isMobile"
          size="small"
          circle
          @click="showPanel = false"
      >
        ✕
      </el-button>
    </div>

    <!-- Selected Item -->
    <el-divider content-position="left">所选构件</el-divider>
    <el-empty v-if="!localId" description="在场景中点击元素" :image-size="60" />
    <div v-else>
      <p class="item-name">{{ selectedName || '…' }}</p>

      <el-button
          type="primary"
          size="small"
          :disabled="!localId"
          @click="onLogAttributes"
      >构件信息</el-button
      >
      <div class="row">
        <el-button
            type="primary"
            size="small"
            :disabled="!localId"
            @click="onLogPsets"
        >日志信息</el-button
        >
        <el-checkbox v-model="formatPset">Format</el-checkbox>
      </div>
      <el-button
          type="primary"
          size="small"
          :disabled="!localId"
          @click="onLogGeometry"
      >Log Geometry</el-button
      >
    </div>

    <!-- Categories -->
    <el-divider content-position="left">类别</el-divider>
    <el-select v-model="currentCategory" placeholder="请选择类别" style="width: 100%">
      <el-option
          v-for="c in categories"
          :key="c"
          :label="c"
          :value="c"
      />
    </el-select>

    <div class="row">
      <el-button size="small" @click="onLogNames">类别名称</el-button>
<!--      <el-checkbox v-model="uniqueNames">Unique</el-checkbox>-->
    </div>
    <el-button size="small" @click="onLogGeometries">加载类别</el-button>
    <el-button size="small" @click="onDisposeMeshes">清除类别</el-button>
  </aside>

  <!-- 手机端浮动按钮 -->
  <el-button
      v-if="isMobile && !showPanel"
      class="fab"
      circle
      size="large"
      @click="showPanel = true"
  >
    <el-icon><Setting /></el-icon>
  </el-button>

  <!-- Stats -->
  <div ref="statsRef" class="stats"></div>

  <!-- 弹窗 -->
  <el-dialog
      v-model="isPopupVisible"
      title="构件详情"
      width="500"
      align-center
  >
    <p><b>构件名称：</b>{{ ifcName }}</p>
    <p><b>规范条文：</b></p>

    <!-- 使用表格展示 -->
    <el-table
        :data="formattedRules"
        border
        stripe
        style="width: 100%; margin-top: 10px"
        max-height="300"
    >
      <el-table-column prop="content" label="条文内容" />
      <el-table-column prop="result" label="结果" width="100" />
    </el-table>

    <template #footer>
      <el-button @click="closePopup">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import {ref, onMounted, nextTick, computed} from 'vue'
import * as THREE from 'three'
import * as OBC from '@thatopen/components'
import * as FRAGS from '@thatopen/fragments'
import { Setting } from '@element-plus/icons-vue'
import axios from "axios";

/* ---------- 基础声明 ---------- */
const containerRef = ref()
const statsRef = ref()

const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent,
)

/* ---------- 响应式状态 ---------- */
const categories = ref([])
const localId = ref(null)
const selectedName = ref(null)
const formatPset = ref(true)
const uniqueNames = ref(false)
const currentCategory = ref('')
const showPanel = ref(false)

const ifcName = ref('')
const ifcRule = ref('')
const isPopupVisible = ref(false)

/* ---------- Three / Fragments 实例 ---------- */
let components
let world
let fragments
let model
let LOCKED_ID = []

const meshes = []

/* ---------- 初始化 ---------- */
onMounted(async () => {
  await nextTick()

  components = new OBC.Components()
  const worlds = components.get(OBC.Worlds)
  world = worlds.create()
  world.scene = new OBC.SimpleScene(components)
  world.scene.setup()
  world.scene.three.background = null

  world.renderer = new OBC.SimpleRenderer(components, containerRef.value)
  world.camera = new OBC.SimpleCamera(components)
  await world.camera.controls.setLookAt(58, 22, -25, 13, 0, 4.2)
  components.init()

  const grids = components.get(OBC.Grids)
  grids.create(world)

  const workerUrl = '/worker.mjs'
  fragments = new FRAGS.FragmentsModels(workerUrl)

  world.camera.controls.addEventListener('rest', () => fragments.update(true))
  fragments.models.list.onItemSet.add(({ value: m }) => {
    m.useCamera(world.camera.three)
    world.scene.three.add(m.object)
    fragments.update(true)
  })
})

/* ---------- 文件上传 ---------- */
async function beforeUpload(file) {
  const arrayBuffer = await file.arrayBuffer()
  await convertAndLoadIfc(arrayBuffer)
  return false
}

async function convertAndLoadIfc(arrayBuffer) {
  const serializer = new FRAGS.IfcImporter()
  serializer.wasm = {
    absolute: true,
    path: 'https://unpkg.com/web-ifc@0.0.69/',
  }

  const fragmentBytes = await serializer.process({
    bytes: new Uint8Array(arrayBuffer),
    progressCallback: (progress, data) => console.log(progress, data),
  })

  await loadModel(fragmentBytes)
}

async function loadModel(buffer) {
  if (model) {
    world.scene.three.remove(model.object)
    await fragments.unload(model)
    model = null
  }
  model = await fragments.load(buffer, { modelId: 'example' })
  categories.value = await model.getCategories()
  setupRaycasting()
}

/* ---------- 射线拾取 ---------- */

/**
 * 批量设置构件颜色
 * @param {number[]} localIds 本地 ID 列表
 * @param {'green'|'red'|'orange'} colorName 颜色标识
 */
async function setColorByIds(localIds, colorName) {
  if (!model || !localIds.length) return
  
  // 清除之前的高亮
  await model.resetHighlight()
  // 映射颜色
  const colorMap = {
    green: new THREE.Color(0x00c853),
    red:   new THREE.Color(0xd50000),
    orange:new THREE.Color(0xff6d00)
  }
  const color = colorMap[colorName] || colorMap.orange

  // 应用材质
  const material = {
    color,
    renderedFaces: FRAGS.RenderedFaces.TWO,
    opacity: 1,
    transparent: false
  }

  model.highlight(localIds, material)
  await fragments.update(true)
}
function setupRaycasting() {
  const highlightMaterial = {
    color: new THREE.Color('purple'),
    renderedFaces: FRAGS.RenderedFaces.TWO,
    opacity: 1,
    transparent: false,
  }

  const mouse = new THREE.Vector2()

  containerRef.value.addEventListener('click', async (event) => {
    if (!model) return

    const rect = containerRef.value.getBoundingClientRect()
    mouse.x = event.clientX - rect.left
    mouse.y = event.clientY - rect.top

    const result = await model.raycast({
      camera: world.camera.three,
      mouse,
      dom: world.renderer.three.domElement,
    })

    const promises = []

    if (result) {
      // 如果之前选中的不是 LOCKED 的，就恢复
      if (localId.value !== null && !LOCKED_ID.includes(localId.value)) {
        promises.push(model.resetHighlight([localId.value]))
      }

      localId.value = result.localId
      selectedName.value = null

      // ✅ 只对非 LOCKED 的构件设置红色高亮
      if (!LOCKED_ID.includes(result.localId)) {
        promises.push(model.highlight([result.localId], highlightMaterial))
      }

      await updateSelectedName()
    } else {
      // ✅ 点击空白：只 reset 非 LOCKED 的构件
      const toReset = localId.value !== null && !LOCKED_ID.includes(localId.value)
          ? [localId.value]
          : []
      if (toReset.length) promises.push(model.resetHighlight(toReset))

      localId.value = null
      selectedName.value = null
    }

    promises.push(fragments.update(true))
    await Promise.all(promises)
  })
}


/* ---------- 获取信息 ---------- */
async function updateSelectedName() {
  if (!localId.value || !model) return
  const [data] = await model.getItemsData([localId.value], {
    attributesDefault: false,
    attributes: ['Name'],
  })
  const name = data.Name?.value
  selectedName.value = typeof name === 'string' ? name : null
}

/* ---------- 功能回调 ---------- */

const formattedRules = computed(() => {
  if (!Array.isArray(ifcRule.value)) return []
  return ifcRule.value.map(item => ({
    content: item?.内容 || '',
    result: item?.判断结果 || '未知'
  }))
})

async function onLogAttributes() {
  if (!localId.value || !model) return
  const [data] = await model.getItemsData([localId.value], {
    attributesDefault: true,
  })
  console.log('Attributes:', data)
  ifcName.value = selectedName.value

  const guid = data._guid.value

  try {
    // 向后端请求
    const rules = await axios.get('http://localhost:5000/ifcView/getRules', {
      params: { guid }  // 使用 params 传递查询参数
    });
    ifcRule.value = rules.data.data
    console.log('ifcrule', rules.data.data);

  } catch (error) {
    console.error('获取 rule 失败:', error);
  }
  isPopupVisible.value = true
}

async function onLogPsets() {
  if (!localId.value || !model) return
  const [data] = await model.getItemsData([localId.value], {
    attributesDefault: false,
    attributes: ['Name', 'NominalValue'],
    relations: {
      IsDefinedBy: { attributes: true, relations: true },
      DefinesOcurrence: { attributes: false, relations: false },
    },
  })
  const rawPsets = data.IsDefinedBy || []
  const result = formatPset.value ? formatItemPsets(rawPsets) : rawPsets
  console.log('PropertySets:', result)
}

function formatItemPsets(rawPsets) {
  const result = {}
  for (const pset of rawPsets) {
    const psetName = pset.Name?.value
    const propsArr = pset.HasProperties
    if (!psetName || !Array.isArray(propsArr)) continue
    const props = {}
    for (const prop of propsArr) {
      const name = prop.Name?.value
      const value = prop.NominalValue?.value
      if (name !== undefined && value !== undefined) props[name] = value
    }
    result[psetName] = props
  }
  return result
}

async function onLogGeometry() {
  if (!localId.value || !model) return
  const [geo] = await model.getItemsGeometry([localId.value])
  console.log('Geometry:', geo)
}

async function onLogNames() {
  if (!currentCategory.value || !model) return
  const ids = await model.getItemsOfCategories([
    new RegExp(`^${currentCategory.value}$`),
  ])
  const localIds = ids[currentCategory.value]
  const data = await model.getItemsData(localIds, {
    attributesDefault: false,
    attributes: ['Name'],
  })
  const names = data
      .map((d) => (d.Name?.value ? String(d.Name.value) : null))
      .filter(Boolean)
  const final = uniqueNames.value ? [...new Set(names)] : names
  console.log('Names:', final)
}

async function onLogGeometries() {
  if (!currentCategory.value || !model) return
  const items = await model.getItemsOfCategories([
    new RegExp(`^${currentCategory.value}$`),
  ])
  const localIds = Object.values(items).flat()
  const geometries = await model.getItemsGeometry(localIds)
  console.log(`Geometries of ${currentCategory.value}:`, geometries)

  const mat = new THREE.MeshLambertMaterial({ color: 'purple' })
  geometries.forEach((geoArr) =>
      geoArr.forEach((g) => {
        const mesh = createMesh(g, mat)
        if (mesh) world.scene.three.add(mesh)
      }),
  )
  await model.setVisible(localIds, false)
  await fragments.update(true)
}

function createMesh(data, material) {
  const { positions, indices, normals, transform } = data
  if (!(positions && indices && normals)) return null
  const geo = new THREE.BufferGeometry()
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geo.setAttribute('normal', new THREE.BufferAttribute(normals, 3))
  geo.setIndex(Array.from(indices))
  const mesh = new THREE.Mesh(geo, material)
  mesh.applyMatrix4(transform)
  meshes.push(mesh)
  return mesh
}

async function onDisposeMeshes() {
  meshes.forEach((m) => {
    m.removeFromParent()
    m.geometry.dispose()
    const materials = Array.isArray(m.material) ? m.material : [m.material]
    materials.forEach((mat) => mat.dispose())
  })
  meshes.length = 0
  if (model) {
    await model.setVisible(undefined, true)
    await fragments.update(true)
  }
}


function closePopup() {
  isPopupVisible.value = false
}

async function getCompliance() {
  LOCKED_ID.splice(0, LOCKED_ID.length)
  try {
    const { data } = await axios.post('http://localhost:5000/ifcView/compliance')
    const guid_list = data
    const localIds = await model.getLocalIdsByGuids(guid_list)
    LOCKED_ID.push(...localIds)

    await setColorByIds(localIds, 'green')
  } catch (e) {
    console.error(e)
  }
}

async function getNonCompliance() {
  LOCKED_ID.splice(0, LOCKED_ID.length)
  try {
    const { data } = await axios.post('http://localhost:5000/ifcView/Noncompliance')
    const guid_list = data
    const localIds = await model.getLocalIdsByGuids(guid_list)
    LOCKED_ID.push(...localIds)

    // ✅ 关键：着色
    await setColorByIds(localIds, 'red')
  } catch (e) {
    console.error(e)
  }
}

async function getNormal() {
  LOCKED_ID.splice(0, LOCKED_ID.length)
  try {
    const { data } = await axios.post('http://localhost:5000/ifcView/normal')
    const guid_list = data
    const localIds = await model.getLocalIdsByGuids(guid_list)
    LOCKED_ID.push(...localIds)

    // ✅ 关键：着色
    await setColorByIds(localIds, 'orange')
  } catch (e) {
    console.error(e)
  }
}


async function clearColor() {
  LOCKED_ID.splice(0,LOCKED_ID.length)
  if (model) {
    // 清除所有高亮
    await model.resetHighlight(); // ✅ 关键：清除所有高亮
  }
  setupRaycasting()
  await fragments.update(true)          // 3. 立即刷新场景
  console.log('lock',LOCKED_ID)
}



</script>

<style scoped>
.viewport {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.top-bar {
  position: absolute;
  top: 1rem;
  left: 1rem;
  z-index: 1001;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.control-card {
  position: fixed;
  top: 1rem;
  right: 1rem;
  width: 30vh;
  height: 65vh;
  max-height: 90vh;
  background: #ffffffee;
  backdrop-filter: blur(6px);
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  overflow-y: auto;
  z-index: 999;
  margin-top: 10vh;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0.5rem 0;
}

.item-name {
  font-weight: 600;
  margin: 0.5rem 0;
}

.fab {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  z-index: 1000;
}

.stats {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 10;
}
</style>