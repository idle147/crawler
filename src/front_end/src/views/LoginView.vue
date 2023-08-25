<template>
    <!-- 登录页面 -->
    <div>
        <el-button v-if="username === null" size=large class="login-btn" type="primary" @click="to_login()">
            请登录
        </el-button>
        <template v-else>
            <p> 尊敬的[{{ username }}]: </p>
            <br>
            <el-button size=large class="login-btn" disabled type="primary">
                您已经登录过了
            </el-button>
        </template>

    </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { login_judge } from "@/request/api";
import setting from "../settings"
import Bus from "@/type/bus"


const current_url = encodeURIComponent(window.location.href)
const username = ref<string | null>(localStorage.getItem('username'))
const to_login = () => {
    // 跳转到登录页面
    console.log(setting.BASEURL + "openid/login?next=" + current_url)
    location.href = setting.BASEURL + "openid/login?next=" + current_url
}

login_judge().then((res) => {
    // 将token进行保存
    console.log(res)
    if (res === undefined) {
        localStorage.removeItem("username")
        username.value = null
    }
    else if ("username" in res) {
        localStorage.setItem("username", res.username)
        username.value = res.username
        Bus.emit('is_login', true)
    }
})
</script>



<style scoped>
</style> 