<template>
  <div class="home-container">
    <el-card class="welcome-card" shadow="hover">
      <div class="header">
        <h2 class="title">欢迎使用 BIM 自动合规性审查系统</h2>
      </div>

      <el-divider></el-divider>

      <p class="description">上传您的 BIM 文件，系统将自动进行合规性审查，并提供详细的审查报告</p>

      <div class="action-area">
        <router-link to="/upload">
          <el-button
              type="primary"
              size="large"
              icon="el-icon-upload"
              class="upload-btn"
          >
            开始审查
          </el-button>
        </router-link>

        <div class="secondary-actions">
          <el-button
              type="text"
              class="learn-more"
              @click="showHelpDialog"
          >
            了解如何使用 <i class="el-icon-question"></i>
          </el-button>

          <router-link to="/history">
            <el-button
                type="text"
                class="history-btn"
            >
              历史记录 <i class="el-icon-time"></i>
            </el-button>
          </router-link>
        </div>
      </div>
    </el-card>

    <!-- 帮助对话框 -->
    <el-dialog title="使用帮助" v-model:visible="helpDialogVisible" width="50%">
      <div class="help-content">
        <h4>如何使用本系统：</h4>
        <ol>
          <li>点击"开始审查"按钮上传您的BIM文件</li>
          <li>系统将自动分析文件内容</li>
          <li>审查参考了《住宅设计规范》、《建筑窗口洞口大小》、《建筑设计防火规范》等</li>
          <li>查看生成的合规性报告</li>
          <li>下载报告或分享结果</li>
        </ol>
        <h4>支持的文件格式：</h4>
        <ul>
          <li>IFC (.ifc)</li>
        </ul>
      </div>
      <template v-slot:footer>
    <span class="dialog-footer">
      <el-button @click="helpDialogVisible = false">关 闭</el-button>
    </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
// console.log(Response.user.id)
export default {

  name: 'HomeView',
  data() {
    return {
      helpDialogVisible: false
    }
  },
  methods: {
    showHelpDialog() {
      this.helpDialogVisible = true
    }
  }
}
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.welcome-card {
  margin-bottom: 30px;
  padding: 30px;
  text-align: center;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.title {
  color: #303133;
  font-size: 24px;
  margin-bottom: 10px;
  margin-top: 10px;
}

.description {
  color: #606266;
  font-size: 16px;
  margin-bottom: 30px;
}

.action-area {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.secondary-actions {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}

.upload-btn {
  width: 200px;
  margin-bottom: 15px;
}

.learn-more,
.history-btn {
  color: #909399;
}

.help-content {
  line-height: 2;
}

.help-content h4 {
  margin: 15px 0 10px;
  color: #303133;
}

.help-content ol,
.help-content ul {
  padding-left: 20px;
}
</style>