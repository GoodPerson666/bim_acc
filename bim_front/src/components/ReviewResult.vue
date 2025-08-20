<template>
  <div class="result-container">
    <el-card class="result-card" shadow="hover">
      <!-- 顶部标题区域 -->
      <div class="result-header">
        <h2 class="result-title">BIM 文件审查结果</h2>
        <el-button
            type="primary"
            size="small"
            :icon="Download"
            @click="exportResult"
            class="export-btn"
        >
          导出报告
        </el-button>
        <el-button
            type="primary"
            size="small"
            :icon="IfcView"
            @click="GoIFCView"
            class="ifc-btn">
          查看模型
        </el-button>
      </div>

      <el-divider />

      <!-- 主要内容区域 -->
      <div v-if="result" class="result-content">
        <!-- 文件信息卡片 -->
        <el-card class="info-card" shadow="never">
          <template #header>
            <div class="card-header">
              <el-icon :component="Document" />
              <span>文件信息</span>
            </div>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="文件名">
              {{ result.文件路径.split('/').pop() }}
            </el-descriptions-item>
            <el-descriptions-item label="文件路径">
              {{ result.文件路径 }}
            </el-descriptions-item>
            <el-descriptions-item label="审查时间">
              {{ new Date().toLocaleString() }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 审查结果卡片 -->
        <el-card class="result-card" shadow="never">
          <template #header>
            <div class="card-header">
              <el-icon :component="Finished" />
              <span>审查结果</span>
              <el-tag :type="getResultStatus(result)" class="status-tag">
                {{ getResultStatusText(result) }}
              </el-tag>
            </div>
          </template>

          <!-- 结构化结果展示 -->
          <div v-if="isStructuredResult(result.审查结果)" class="structured-result">
            <el-collapse v-model="activePanels" accordion>
              <el-collapse-item
                  v-for="(item, category) in result.审查结果"
                  :key="category"
                  :name="category"
                  :title="formatCategoryName(category)"
              >
                <el-table :data="formatResultItems(item)" border style="width: 100%">
                  <el-table-column prop="item" label="检查项" width="180">
                  </el-table-column>
                  <el-table-column prop="status" label="状态" width="100">
                    <template #default="{ row }">
                      <el-tag :type="getStatusType(row.status)" size="small">
                        {{ row.status }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="message" label="详细信息">
                  </el-table-column>
                </el-table>
              </el-collapse-item>
            </el-collapse>
          </div>

          <!-- 非结构化结果展示 -->
          <div v-else class="unstructured-result">
            <el-alert
                title="原始审查结果"
                type="info"
                :closable="false"
                show-icon
            ></el-alert>
            <pre class="result-pre">{{ formatUnstructuredResult(result.审查结果) }}</pre>
          </div>
        </el-card>

        <!-- 操作按钮区域 -->
        <div class="action-buttons">
          <el-button-group>
            <el-button
                type="primary"
                :icon="RefreshLeft"
                @click="reReview"
            >
              重新审查
            </el-button>
            <el-button
                type="success"
                :icon="Upload"
                @click="uploadNewFile"
            >
              上传新文件
            </el-button>
            <el-button
                type="info"
                :icon="ChatDotRound"
                @click="showFeedbackDialog"
            >
              提交反馈
            </el-button>
          </el-button-group>
        </div>
      </div>

      <!-- 无结果提示 -->
      <div v-else class="no-result">
        <el-empty description="暂无审查结果">
          <el-button type="primary" @click="uploadNewFile">上传文件</el-button>
        </el-empty>
      </div>
    </el-card>

    <!-- 反馈对话框 -->
    <el-dialog
        title="提交反馈"
        v-model="feedbackDialogVisible"
        width="50%"
    >
      <el-form :model="feedbackForm" label-width="80px">
        <el-form-item label="反馈类型">
          <el-select v-model="feedbackForm.type" placeholder="请选择反馈类型">
            <el-option label="结果不正确" value="incorrect"></el-option>
            <el-option label="建议改进" value="improvement"></el-option>
            <el-option label="其他问题" value="other"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="详细描述">
          <el-input
              type="textarea"
              v-model="feedbackForm.content"
              :rows="4"
              placeholder="请详细描述您的问题或建议"
          ></el-input>
        </el-form-item>
        <el-form-item label="联系方式">
          <el-input
              v-model="feedbackForm.contact"
              placeholder="请输入您的邮箱或电话（可选）"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="feedbackDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitFeedback">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import {
  Document,
  Finished,
  RefreshLeft,
  Upload,
  ChatDotRound,
  Download
} from "@element-plus/icons-vue";

export default {
  data() {
    return {
      result: null,
      activePanels: [], // 当前展开的面板
      feedbackDialogVisible: false,
      feedbackForm: {
        type: '',
        content: '',
        contact: ''
      }
    };
  },
  created() {
    if (this.$route.query.result) {
      this.result = JSON.parse(this.$route.query.result);
      // 默认展开第一个分类
      if (this.isStructuredResult(this.result?.审查结果)) {
        this.activePanels = [Object.keys(this.result.审查结果)[0]];
      }
    }
  },
  methods: {
    isStructuredResult(result) {
      return result && typeof result === 'object' && !Array.isArray(result);
    },
    formatUnstructuredResult(result) {
      if (typeof result === 'string') {
        return result;
      }
      return JSON.stringify(result, null, 2);
    },
    formatCategoryName(category) {
      const map = {
        structural: '结构审查',
        fireSafety: '消防安全',
        accessibility: '无障碍设施',
        energyEfficiency: '能源效率',
        default: category
      };
      return map[category] || category;
    },
    formatResultItems(items) {
      if (Array.isArray(items)) {
        return items.map(item => ({
          item: item.rule || item.item,
          status: item.status || (item.passed ? '通过' : '未通过'),
          message: item.message || item.detail
        }));
      }
      return [];
    },
    getStatusType(status) {
      const statusMap = {
        通过: 'success',
        合格: 'success',
        未通过: 'danger',
        不合格: 'danger',
        警告: 'warning',
        待确认: 'info'
      };
      return statusMap[status] || 'info';
    },
    getResultStatus(result) {
      if (!result?.审查结果) return 'info';
      if (typeof result.审查结果 === 'string') {
        return result.审查结果.includes('通过') ? 'success' : 'warning';
      }
      return 'success'; // 结构化数据默认显示成功
    },
    getResultStatusText(result) {
      const status = this.getResultStatus(result);
      const statusTextMap = {
        success: '审查通过',
        warning: '部分问题',
        danger: '审查未通过',
        info: '待审查'
      };
      return statusTextMap[status];
    },
    exportResult() {
      this.$message.success('报告正在导出，请稍候...');
      axios.get('http://localhost:5000/review-result/result', {
        responseType: 'blob'
      })
          .then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const a = document.createElement('a');
            a.href = url;
            a.download = 'result.txt';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            this.$message.success('报告下载成功');
          })
          .catch(error => {
            this.$message.error('报告下载失败: ' + error.message);
          });
    },
    GoIFCView(){
      this.$router.push('/ifcView');
      // window.location.href = "http://localhost:5173/";
    },
    reReview() {
      if (this.result?.文件路径) {
        this.$confirm('确定要重新审查此文件吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$message.info('正在重新审查文件...');
          // 实际调用重新审查的API
        }).catch(() => {
          this.$message.info('已取消重新审查');
        });
      }
    },
    uploadNewFile() {
      this.$router.push('/upload');
    },
    showFeedbackDialog() {
      this.feedbackDialogVisible = true;
    },
    submitFeedback() {
      if (!this.feedbackForm.content) {
        this.$message.warning('请填写反馈内容');
        return;
      }
      this.$message.success('反馈提交成功，感谢您的意见！');
      this.feedbackDialogVisible = false;
      this.feedbackForm = {
        type: '',
        content: '',
        contact: ''
      };
    }
  },
  setup() {
    return {
      Document,
      Finished,
      RefreshLeft,
      Upload,
      ChatDotRound,
      Download
    };
  }
};
</script>

<style scoped>
.result-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.result-card {
  padding: 20px;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.result-title {
  margin: 0;
  color: #303133;
}

.export-btn {
  position: absolute;
  right: 0;
}

.ifc-btn{
  position: absolute;
  right: 20vh;
}

.card-header {
  display: flex;
  align-items: center;
  font-weight: bold;
}

.card-header i {
  margin-right: 8px;
  font-size: 18px;
}

.status-tag {
  margin-left: 15px;
}

.info-card {
  margin-bottom: 20px;
}

.structured-result {
  margin-top: 10px;
}

.unstructured-result {
  margin-top: 10px;
}

.result-pre {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  white-space: pre-wrap;
  font-family: Consolas, Monaco, monospace;
  line-height: 1.5;
  max-height: 500px;
  overflow-y: auto;
}

.action-buttons {
  margin-top: 30px;
  text-align: center;
}

.no-result {
  padding: 50px 0;
}
</style>