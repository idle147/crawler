<template>
    <el-row :gutter="15">
        <el-col :span="12" v-for="item in sources_array" :key="item" style="margin-bottom:15px;">
            <el-card class="box-card" shadow="always" :body-style="{ height: 400 + 'px', 'overflow-y': 'auto' }">
                <template #header>
                    <div class="card-header">
                        <span>[{{ item.source }}]日志文件:[{{ currentRoute.query.date }}]</span>
                        <!-- 循环开启websocket -->
                        <el-button class="button" type="primary" size="large" round @click="return_index()">
                            返回
                        </el-button>
                    </div>
                </template>
                <div v-html="item.message"></div>
            </el-card>
        </el-col>
    </el-row>
</template>

<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from "vue-router"
const currentRoute = useRoute()
const router = useRouter();
function return_index() {
    router.back()
}

const sources = currentRoute.query.sources as string
const sources_array = ref<any>(sources.split(",").map(ele => {
    return {
        source: ele,
        ws: null,
        message: ''
    }
}))

function openlog(item: any) {
    console.log("打开")
    console.log('ws://' + window.location.host + '/log/' + currentRoute.query.date + '/' + item.source)
    item.ws = new WebSocket('ws://' + window.location.host + '/log/' + currentRoute.query.date + '/' + item.source)
    item.ws.onopen = function (evt: any) {
        console.log("打开websocket连接", evt)
        item.ws.send("Hello, message")
    }

    item.ws.onmessage = function (e: any) {
        const tmp = JSON.parse(e.data).message
        for (const pos in tmp) {
            item.message += "<br>" + tmp[pos]
        }
    }

    item.ws.onclose = function (e: any) {
        console.log("断开连接:", e.code + " " + e.reason + " " + e.wasClean);
    }
}


onMounted(() => {
    sources_array.value.forEach((item: any) => {
        openlog(item)
    })
})

onBeforeUnmount(() => {
    sources_array.value.forEach((item: any) => {
        if (item.ws !== null) {
            item.ws.close()
        }
    })
})
</script>

<style>
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 30px;
    border: 10px;
}

.item {
    margin-bottom: 18px;
}
</style>