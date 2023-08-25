<template>
  <div class="home_box">
    <!-- 回到顶部控件 -->
    <el-backtop :right="100" :bottom="100" />
    <el-container>
      <!-- 主体布局内容 -->
      <el-main>
        <el-menu class="el-menu-demo" mode="horizontal" text-color="aliceblue" active-text-color="#448AFF"
          background-color="#123456" router :ellipsis="false">
          <!-- router开启路由, 通过el-menu-item index进行跳转-->
          <el-menu-item :index="item.path" v-for="item in router_list" :key="item.path">
            <span> {{ item.meta.title }}</span>
          </el-menu-item>
          <div class="flex-grow" />
          <el-menu-item index="" @click="del_token" v-show="is_login">退出登录</el-menu-item>
        </el-menu>
      </el-main>
      <!-- 展示区域布局内容 -->
      <el-footer>
        <!-- 设置路由出口 -->
        <router-view></router-view>
      </el-footer>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from 'element-plus';
import { logout } from "@/request/api";
import Bus from '@/type/bus'

//路由设置
const currentRoute = useRoute()
const router = useRouter();
const router_list = router.getRoutes().filter(v => v.meta.isShow);
const is_login = ref<string | null>(localStorage.getItem('username'))

Bus.on('is_login', (data) => { is_login.value = data as string })

//监听登录结果
watch(currentRoute, (newVal, old_val) => {
  console.log(old_val)
  if (newVal.query.refresh) {
    is_login.value = localStorage.getItem('username')
  }
}, { immediate: true });

//退出登录
const del_token = () => {
  ElMessageBox.confirm(
    '是否退出登录?',
    'Warning',
    {
      confirmButtonText: '是',
      cancelButtonText: '否',
      type: 'warning',
    }
  )
    .then(() => {
      // 发送退出登录接口
      localStorage.removeItem('username')
      logout()
      is_login.value = null
      router.push('/login')
      ElMessage({
        type: 'success',
        message: '退出登录成功~',
      })
      router.go(0)

    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消退出登录',
      })
    })
}
</script>



<style lang="scss" scoped>
.home_box {
  width: 100%;
  height: 100%;
  background: url("../assets/bg.jpg");
  background-size: 100% 100%;
}

.flex-grow {
  flex-grow: 1;
}
</style>
