<template>
  <div class="upload-container">
    <el-card class="upload-card" shadow="hover">
      <div class="upload-header">
        <el-page-header @back="$router.go(-1)" />
        <h2 class="upload-title">上传 BIM 文件</h2>
        <p class="upload-subtitle">支持 IFC 的 BIM 格式</p>
      </div>

      <el-divider />

      <div class="upload-area">
        <el-upload
            class="upload-demo"
            drag
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            :file-list="fileList"
            accept=".ifc"
        >
          <el-icon class="el-icon-upload" />
          <div class="el-upload__text">
            将文件拖到此处，或<em>点击选择文件</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">文件大小不超过 100MB</div>
          </template>
        </el-upload>

        <div class="upload-actions">
          <el-button
              type="primary"
              size="large"
              :loading="loading"
              :disabled="!selectedFile"
              @click="uploadFile"
              class="upload-btn"
          >
            <template v-if="!loading">
              <el-icon class="el-icon-upload" /> 上传并审核
            </template>
            <template v-else> 正在上传... </template>
          </el-button>

          <el-progress
              v-if="loading"
              :percentage="uploadProgress"
              :stroke-width="6"
              :text-inside="true"
              :status="uploadStatus"
              style="width: 100%; margin-top: 20px;"
          />

          <el-button
              type="text"
              @click="showFileRequirements"
              class="requirements-btn"
          >
            <el-icon class="el-icon-info" /> 查看文件要求
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 文件要求对话框 -->
    <el-dialog
        title="BIM 文件要求"
        v-model="requirementsDialogVisible"
        width="50%"
    >
      <div class="requirements-content">
        <h4>支持的文件格式：</h4>
        <ul>
          <li>IFC (.ifc) - 行业基础类</li>
        </ul>

        <h4>文件要求：</h4>
        <ul>
          <li>文件大小不超过 100MB</li>
          <li>文件应包含完整的模型信息</li>
          <li>建议使用最新版本的软件导出</li>
          <li>确保文件没有损坏</li>
        </ul>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="requirementsDialogVisible = false">关 闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      selectedFile: null,
      fileList: [],
      loading: false,
      requirementsDialogVisible: false,
      uploadProgress: 0,
      uploadStatus: null
    };
  },

  methods: {
    handleFileChange(file, fileList) {
      this.selectedFile = file.raw;
      this.fileList = fileList.slice(-1); // 只保留最新选择的文件
      this.uploadProgress = 0;
      this.uploadStatus = null;
    },

    async uploadFile() {
      if (!this.selectedFile) {
        ElMessage.error('请先选择文件');
        return;
      }

      // 检查文件大小
      if (this.selectedFile.size > 100 * 1024 * 1024) {
        ElMessage.error('文件大小不能超过100MB');
        return;
      }

      this.loading = true;
      this.uploadStatus = null;
      const formData = new FormData();
      formData.append('file', this.selectedFile);

      const userID = localStorage.getItem('userID');
      if (!userID) {
        ElMessage.error('未获取到用户ID，请重新登录');
        this.loading = false;
        return;
      }
      formData.append('userID', userID);

      try {
        const response = await axios.post('http://localhost:5000/review', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: progressEvent => {
            this.uploadProgress = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
            );
          }
        });

        this.uploadStatus = 'success';
        ElMessage.success('文件上传成功，正在分析...');

        // 跳转到结果页，并传递审查结果
        this.$router.push({
          path: '/review-result',
          query: { result: JSON.stringify(response.data) }
        });
      } catch (error) {
        console.error('上传失败:', error);
        this.uploadStatus = 'exception';
        let errorMessage = '上传失败，请重试';

        if (error.response) {
          switch (error.response.status) {
            case 413:
              errorMessage = '文件太大，请压缩后重新上传';
              break;
            case 415:
              errorMessage = '不支持的文件格式';
              break;
            case 500:
              errorMessage = '服务器处理文件时出错';
              break;
          }
        }
        ElMessage.error(errorMessage);
      } finally {
        this.loading = false;
        // 3秒后重置进度条
        setTimeout(() => {
          this.uploadProgress = 0;
          this.uploadStatus = null;
        }, 30000);
      }
    },

    showFileRequirements() {
      this.requirementsDialogVisible = true;
    }
  }
};
</script>

<style scoped>
.upload-container {
  max-width: 800px;
  max-height: 800px;
  margin: 0 auto;
  padding: 10px;
}

.upload-card {
  padding: 30px;
  text-align: center;
}

.upload-header {
  margin-bottom: 10px;
}

.upload-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 15px;
}

.upload-title {
  color: #303133;
  font-size: 24px;
  margin-bottom: 10px;
  margin-top: 5px;
}

.upload-subtitle {
  color: #909399;
  font-size: 14px;
}

.upload-area {
  margin: 30px 0;
}

.upload-actions {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-btn {
  width: 200px;
  margin-bottom: 15px;
}

.requirements-btn {
  color: #909399;
  margin-top: 15px;
}

.requirements-content {
  line-height: 2;
}

.requirements-content h4 {
  margin: 15px 0 10px;
  color: #303133;
}

.requirements-content ul {
  padding-left: 20px;
}
</style>