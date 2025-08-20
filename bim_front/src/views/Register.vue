<template>
  <div class="register-container">
    <el-card class="register-card" shadow="always">
      <template v-slot:header>
        <div  class="text-center">
          <h3>用户注册</h3>
        </div>
      </template>

      <el-form
          ref="registerForm"
          :model="registerForm"
          :rules="rules"
          label-width="100px"
          status-icon
      >
        <el-form-item label="用户名" prop="username">
          <el-input
              v-model="registerForm.username"
              placeholder="请输入用户名"
              prefix-icon="el-icon-user"
              clearable
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="el-icon-lock"
              show-password
              clearable
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              prefix-icon="el-icon-lock"
              show-password
              clearable
          ></el-input>
        </el-form-item>
        <el-form-item v-if="errorMessage" class="error-message">
          <el-alert
              :title="errorMessage"
              type="error"
              show-icon
              :closable="false"
          ></el-alert>
        </el-form-item>
        <el-form-item>
          <el-button
              type="primary"
              @click="handleRegister"
              :loading="loading"
              style="width: 100%"
          >
            {{ loading ? '注册中...' : '立即注册' }}
          </el-button>
        </el-form-item>
      </el-form>
      <div class="login-link text-center">
        <span>已有账号？</span>
        <el-link type="primary" @click="handleClick">立即登录</el-link>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserRegister',
  data() {
    // 验证密码一致性
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入的密码不一致'));
      } else {
        callback();
      }
    };

    return {
      registerForm: {
        username: '',
        password: '',
        confirmPassword: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度应在 3 到 20 个字符之间', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 3, max: 20, message: '密码长度应在 3 到 20 个字符之间', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' }
        ]
      },
      errorMessage: '',
      loading: false
    };
  },
  methods: {
    handleClick(){
      this.$router.push('/login');
    },

    async handleRegister() {
      this.errorMessage = '';
      this.loading = true;

      // 先进行表单验证
      try {
        await this.$refs.registerForm.validate();

        try {
          const response = await axios.post('http://localhost:5000/register', {
            username: this.registerForm.username,
            password: this.registerForm.password
          });

          if (response.data.success) {
            this.$message.success('注册成功！请登录');
            this.$router.push('/login');
          } else {
            // 处理注册失败
            this.errorMessage = response.data.message || '注册失败，请重试';
          }
        } catch (error) {
          // 处理网络错误或其他异常
          console.error('注册失败:', error);
          this.errorMessage = '网络错误，请稍后再试';
        }
      } catch (error) {
        // 表单验证失败
        console.log('表单验证失败:', error);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  background-color: #f5f7fa;
}

.register-card {
  width: 400px;
  padding: 20px;
}

.text-center {
  text-align: center;
}

.login-link {
  margin-top: 20px;
}

.error-message {
  margin-bottom: 0;
}
</style>