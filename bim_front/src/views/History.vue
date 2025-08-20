<template>
  <div class="history-container">
    <el-page-header @back="$router.go(-1)" content="历史记录" class="page-header" />

    <el-card shadow="never" class="main-card">
      <div v-if="loading" class="loading-state">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-if="error" class="error-message">
        <el-alert :title="error" type="error" show-icon :closable="false" class="error-alert">
          <el-button @click="fetchHistory" type="primary" size="small">重试</el-button>
        </el-alert>
      </div>

      <div v-if="historyList.length > 0" class="history-content">
        <el-table
            :data="historyList"
            style="width: 100%"
            border
            stripe
            highlight-current-row
            @row-click="handleRowClick"
        >
          <el-table-column prop="review_user_id" label="用户名" width="180">
            <template >
             {{userName}}
            </template>
          </el-table-column>
          <el-table-column prop="review_time" label="审核时间" width="200" sortable>
            <template #default="{row}">
              {{ row.review_time }}
            </template>
          </el-table-column>
          <el-table-column prop="review_content" label="审核内容">
            <template #default="{row}">
              <div class="content-box">
                {{ row.review_content}}
              </div>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-wrapper" v-if="total > pageSize">

          <el-pagination
              :current-page="currentPage"
              :page-size="pageSize"
              layout="prev, pager, next"
              :total="total"
              @current-change="handlePageChange"
              @size-change="handleSizeChange"
          >
          </el-pagination>
        </div>
      </div>

      <div v-else-if="!loading" class="empty-state">
        <el-empty description="暂无历史记录">
          <el-button type="primary" @click="fetchHistory">刷新</el-button>
        </el-empty>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {

  name: 'HistoryPage',
  data() {
    return {
      historyList: [],  // 存储后端返回的数组数据
      loading: false,
      error: null,
      currentPage: 1,
      pageSize: 1,
      total: 0,
      userName:localStorage.getItem('userName')
    }
  },
  created() {
    this.fetchHistory();
  },
  methods: {
    async fetchHistory() {
      this.loading = true;
      this.error = null;

try {
  const userID = localStorage.getItem('userID');
  if (!userID) {
    this.error = '用户未登录';
    return;
  }
  const response = await axios.post('http://localhost:5000/history', {
    userID: userID,
    page: this.currentPage,  // 传递当前页码
    pageSize: this.pageSize  // 传递每页大小
  });

        if (response.data.success) {
          this.historyList = response.data.history || [];
          this.total = response.data.total || 0;  // 获取总记录数
        } else {
          this.error = response.data.message || '获取历史记录失败';
        }
      } catch (err) {
        console.error('获取历史记录失败:', err);
        if (err.response) {
          if (err.response.status === 404) {
            this.error = '未找到该用户的历史记录';
          } else {
            this.error = err.response.data?.message || `服务器错误: ${err.response.status}`;
          }
        } else {
          this.error = '网络错误，请检查连接';
        }
      } finally {
        this.loading = false;
      }
    },
handlePageChange(page) {
  this.currentPage = page;
  this.fetchHistory();  // 切换页码时重新加载数据
},
handleSizeChange(size) {
  this.pageSize = size;
  this.currentPage = 1;
  this.fetchHistory();  // 切换每页大小时重新加载数据
}
  }
}
</script>

<style scoped>
.history-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
}

.main-card {
  min-height: 500px;
  border-radius: 8px;
}

.loading-state {
  padding: 20px;
}

.error-message {
  margin: 20px 0;
}

.error-alert {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.history-content {
  padding: 10px;
}

.content-box {
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
  white-space: pre-line;
  line-height: 1.6;
}

.empty-state {
  height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .history-container {
    padding: 10px;
  }

  :deep(.el-table) {
    font-size: 12px;
  }

  :deep(.el-table__cell) {
    padding: 4px 0;
  }

  .pagination-wrapper {
    overflow-x: auto;
  }
}
</style>
<script setup>
</script>