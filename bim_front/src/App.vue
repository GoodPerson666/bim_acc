<template>
  <div id="app">

    <el-container>
      <el-header>BIM 自动合规性审查系统</el-header>
      <el-main><router-view/></el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
.el-header{
  background-color: #e5e7ea;
  color: #333;
  text-align: center;
  line-height: 60px;
  font-size: 40px;
}
</style>
