<template>
    <div>
        <!-- 回到顶部控件 -->
        <el-backtop :right="100" :bottom="100" />
        <el-container>
            <!-- 主体布局内容 -->
            <el-main>
                <!-- 输入组件 -->
                <div class="input">
                    <el-row :gutter="15" type="flex" justify="center">
                        <el-col :span="5">
                            <el-input v-model="input" @keyup.enter="submit" class="w-50 m-2" maxlength="25"
                                placeholder="请输入查询游戏名称" clearable type="text" :prefix-icon="Search" ref="input_ref" />
                        </el-col>
                        <el-col :span="2">
                            <el-button type="primary" round :icon="Search" @click="submit">启动爬虫</el-button>
                        </el-col>
                    </el-row>
                </div>
                <!-- 渠道选择组件 -->
                <div id="source_check">
                    <el-row v-if="whole_array.length !== 0" :gutter="15" type="flex" justify="center">
                        <el-col :span="2" v-for="(item, index) in whole_array" :key="index">
                            <el-checkbox v-model="item.is_checked" :label="item.label" size="large" />
                        </el-col>
                    </el-row>
                    <el-row v-if="whole_array.length !== 0" type="flex" justify="center">
                        <span style="color: #ebd172"> 注: 5577渠道接口不稳定,慎用(网站打开很慢) </span>
                    </el-row>
                    <span v-else type="flex" justify="center" style="color: red"> 渠道接口加载失败,请检查服务器或刷新重试 </span>
                    <br />
                </div>
            </el-main>

            <!-- 表单布局内容 -->
            <el-footer>
                <!-- 结果表格组件 -->
                <div id=" result_table">
                    <el-table class="elTable" :data="showedDataList" border :header-cell-style="{
                        background: '#2980B9',
                        color: 'white',
                        borderColor: 'black'
                    }" :cell-style="{ borderColor: 'black' }">
                        <el-table-column align="center" prop="date" label="时间" width="250" />
                        <el-table-column align="center" prop="keyword" label="关键词" />
                        <el-table-column align="center" prop="source" label="渠道" />
                        <el-table-column align="center" prop="state" label="状态" />
                        <el-table-column align="center" prop="operations" label="操作" width="250">
                            <template #default="scope">
                                <el-space wrap spacer="|">
                                    <el-button v-if="scope.row.state === '爬取数据中'" type="danger"
                                        @click="handleStop(scope.row)">
                                        中止任务
                                    </el-button>
                                    <el-button v-else-if="scope.row.state === '已完成'" type="success"
                                        @click="handleDetail(scope.row)">
                                        查看详情
                                    </el-button>
                                    <el-button @click="handleLog(scope.row)">
                                        查看Log
                                    </el-button>
                                </el-space>
                            </template>
                        </el-table-column>
                    </el-table>
                    <el-pagination background layout="total, prev, pager, next" :page-size="pagination.page_size"
                        :total="pagination.length" @current-change="currentChange" @size-change="sizeChange" />
                </div>
            </el-footer>
        </el-container>
    </div>
</template>

<script lang="ts" setup>

import { computed, ref, onBeforeMount, onMounted, onUnmounted } from "vue";
import { Search } from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from 'element-plus'
import { IStateData, IAbortRes } from "@/type/search"
import { IStateModel } from "@/type/start"
import { start, get_source_list, get_state_list, put_end_mission } from "@/request/api"
import { useRouter } from "vue-router";
import { Pagination } from "@/function/pagination"
import { get_schedule_list } from "@/request/api"
import Bus from "@/type/bus"

const input = ref("");
const input_ref: any = ref(undefined);
const router = useRouter();

// 源判断
const whole_array = ref<IStateModel[]>([])
const checked_array = computed(() => {
    return whole_array.value.filter(ele => ele.is_checked).map(ele => ele.label)
})

const pagination = ref<Pagination>(new Pagination([]))

function source_judge() {
    //获取源清单
    get_source_list().then((res: any) => {
        whole_array.value = res.source.map((ele: any) => {
            return {
                label: ele,
                is_checked: true,
            }
        })
        Bus.emit('sources_array', whole_array.value)
    })
}

//终止任务句柄
const handleStop = (row: IStateData) => {
    put_end_mission(row.date).then((res: IAbortRes) => {
        if (res.message == "爬虫终止成功") {
            ElMessage({
                showClose: true,
                message: "成功中止任务",
                type: "success",
            })
            row.state = "已取消"
        } else if (res.message == "爬虫已被终止") {
            ElMessage({
                showClose: true,
                message: "爬虫已被中止",
                type: "success",
            })
            row.state = "已取消"
        }
        else {
            ElMessage({
                showClose: true,
                message: "中止任务失败",
                type: "warning",
            })
        }
    })
}

let is_finish = false
let interval_time = 1500
// 获取用户的操作结果
function flush_state() {
    get_state_list().then((res: any) => {
        pagination.value.data_list = res.content
        pagination.value.length = res.content.length
        is_finish = pagination.value.data_list.every((ele) => {
            return ele.state === "已完成" || ele.state === "已取消"
        })
    })

    // 如果有定时任务则is_finish不变设为false, 且定时器设置为间隔事件
    // 重设定时器, 最小间隔时间向后端请求一次
    get_schedule_list().then((res: any) => {
        let min_hour_time = 999
        for (const pos in res.content) {
            const current_time = +res.content[pos].schedule
            if (current_time < min_hour_time) {
                min_hour_time = current_time
            }
        }
        if (min_hour_time !== 999 && is_finish === true) {
            console.log("定时任务激活")
            is_finish = false
            interval_time = min_hour_time * 60 * 60 * 1000 + 3
            console.log(interval_time)
        } else {
            interval_time = 1500
        }
    })
}

let task_timer: any = null
function start_timer() {
    if (task_timer === null) {
        // 还未启动定时器
        is_finish = false
        task_timer = window.setInterval(() => {
            if (is_finish) {
                clearInterval(task_timer)
                task_timer = null
            } else {

                flush_state()
            }
        }, interval_time)
    }
}

//查看log句柄
const handleLog = (row: IStateData) => {
    console.log(row)
    router.push({
        name: "log",
        query: {
            date: row.date,
            sources: row.source.toString()
        }
    });
};

//查看详情
const handleDetail = (row: IStateData) => {
    console.log(row)

    router.push({
        name: "details",
        query: {
            date: row.date,
            sources: row.source.toString()
        }
    });
};

// 计算属性, 切割出实际上需要展示的数据
const showedDataList = computed(() => {
    return pagination.value.get_data()
})

// 当前页改变时触发
const currentChange = (page: number) => {
    pagination.value.page = page
}

// 当单页数量改变时触发
const sizeChange = (page_size: number) => {
    pagination.value.page_size = page_size
}

// 页面渲染之前的操作
onBeforeMount(() => {
    start_timer()
    source_judge()
    //获取爬取的状态清单
    flush_state()
});

// 页面渲染完之后的操作
onMounted(() => {
    //焦点定位到输入框
    input_ref.value.focus()
});

// 页面销毁操作
onUnmounted(() => {
    if (task_timer !== null) {
        console.log("结束任务")
        clearInterval(task_timer)
        task_timer = null
    }
});

//提交
const submit = () => {
    // 关键字校验
    if (input.value == "") {
        ElMessage.error("没有输入查询游戏名,请输入!")
        return
    }

    // 渠道校验
    if (checked_array.value.length === 0) {
        ElMessage.error("没有选择渠道,请选择!")
        return
    }

    //提交确认
    to_submit()
    return
}

const to_submit = () => {
    /* 提交确认 */
    ElMessageBox.confirm(
        '确认启动爬虫吗?',
        '消息',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'info',
            center: true,
        }
    )
        .then(() => {
            // 发送接口,判断爬虫是否启动成功
            start(input.value, checked_array.value).then((res: any) => {
                if (res) {
                    ElMessage({
                        type: 'success',
                        message: '爬虫启动成功~',
                    })
                    flush_state()
                    start_timer()
                } else {
                    ElMessage({
                        type: 'warning',
                        message: '爬虫启动失败!',
                    })
                }
            })

        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '取消爬虫',
            })
        })
}

</script>



<style lang="scss" scoped>
.elTable {
    border: 1px solid black;
}

.input {
    padding-top: 100px;
}

.el-pagination {
    margin-top: 20px;
    display: flex;
    justify-content: right;
}

.el-button {
    min-width: 90px;
    max-width: 90px;
}
</style>