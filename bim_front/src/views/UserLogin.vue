<template>

  <div class="login-container">
    <el-card class="login-card" shadow="always">
      <template v-slot:header>
        <div class="text-center">
          <h3>用户登录</h3>
        </div>
      </template>

      <el-form
          ref="loginForm"
          :model="loginForm"
          :rules="rules"
          label-width="80px"
          status-icon
      >
        <el-form-item label="用户名" prop="username">
          <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              prefix-icon="el-icon-user"
              clearable
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
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
              @click="handleLogin"
              :loading="loading"
              style="width: 100%"
          >
            {{ loading ? '登录中...' : '立即登录' }}
          </el-button>
        </el-form-item>
      </el-form>
      <div class="register-link text-center">
        <span>还没有账号？</span>
        <el-link type="primary" @click="handleClick">立即注册</el-link>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserLogin',
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
        role:''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度应在 3 到 20 个字符之间', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 3, max: 20, message: '密码长度应在 6 到 20 个字符之间', trigger: 'blur' }
        ]
      },
      errorMessage: '',
      loading: false
    };
  },
  methods: {
    handleClick(){
      this.$router.push('/register');
    },
    async handleLogin() {
      this.errorMessage = '';
      this.loading = true;

      // 先进行表单验证
      try {
        await this.$refs.loginForm.validate();

        try {
          const response = await axios.post('http://localhost:5000/login', {
            username: this.loginForm.username,
            password: this.loginForm.password,
            role:this.loginForm.role
          });

          if (response.data.success) {
            // 保存用户信息（例如 token）
            localStorage.setItem('userID', response.data.user.id);
            localStorage.setItem('userName',response.data.user.username);
            localStorage.setItem('role',response.data.user.role)
            this.$message.success('登录成功！');

            // 跳转到主页
            if (localStorage.getItem('role')=='user'){
              this.$router.push('/home');
            }
            else if(localStorage.getItem('role')=='admin'){
              this.$router.push('/admin');
            }


          } else {
            // 处理登录失败
            this.errorMessage = response.data.message || '登录失败，请重试';
          }
        } catch (error) {
          // 处理网络错误或其他异常
          console.error('登录失败:', error);
          this.errorMessage = '密码错误，请重试';
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
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  background-color: #f5f7fa;
}

.login-card {
  width: 400px;
  padding: 20px;
}

.text-center {
  text-align: center;
}

.register-link {
  margin-top: 20px;
}

.error-message {
  margin-bottom: 0;
}
</style>