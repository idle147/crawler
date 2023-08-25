<template>
    <el-table :data="tableData" class="elTable" :cell-style="{ borderColor: 'black' }" border :header-cell-style="{
        background: '#2980B9',
        color: 'white',
        borderColor: 'black'
    }">
        <!--关键词选择组件 -->
        <el-table-column align="center" fixed prop="keyword" label="关键词">
            <template #default="scope">
                <el-input v-if="scope.row.id !== -1" v-model="scope.row.keyword" :readonly="true" />
                <el-input v-else v-model="scope.row.keyword" placeholder="请输入关键词" />
            </template>
        </el-table-column>

        <!--渠道选择组件 -->
        <el-table-column align="center" prop="source" label="渠道" width="600">
            <template #default="scope">
                <el-checkbox-group v-if="scope.row.id !== -1" v-model="scope.row.sources">
                    <el-checkbox :label="item" v-for="item in scope.row.sources" :key="item" disabled>
                    </el-checkbox>
                </el-checkbox-group>
                <span v-else-if="whole_array.length === 0" type="flex" justify="center" style="color: red">
                    渠道接口加载失败,请检查服务器 </span>
                <el-checkbox-group v-else v-model="scope.row.sources">
                    <el-checkbox :label="item.label" v-for="item in whole_array" :key="item">
                    </el-checkbox>
                </el-checkbox-group>
            </template>
        </el-table-column>

        <!--定时器组件 -->
        <el-table-column align="center" prop="scheduled" label="定时选择" width="400">
            <template #default="scope">
                每
                <span v-if="scope.row.id !== -1"> {{ scope.row.schedule }}</span>
                <el-input-number v-else v-model="scope.row.schedule" :precision="1" :step="0.1" :max="24" :min="1" />
                小时执行一次
            </template>
        </el-table-column>

        <!--状态判定组件 -->
        <el-table-column align="center" prop="state" label="状态" width="100" />

        <!--操作组件 -->
        <el-table-column align="center" fixed="right" prop="operation" label="操作">
            <template #default="scope">
                <el-button v-if="scope.row.state === '未启动'" type="success" size="normal"
                    @click.prevent="startScheduled(scope.row)">
                    <h3>启动定时任务</h3>
                </el-button>
                <el-button v-else type="warning" size="normal"
                    @click.prevent="deleteScheduled(scope.row, scope.$index)">
                    <h3>删除定时任务</h3>
                </el-button>

            </template>
        </el-table-column>
    </el-table>

    <div style="text-align:center">
        <br>
        <el-button class="mt-4" round="true" type="primary" size=large style="width: 50%" @click="onAddItem">
            创建定时任务
        </el-button>
    </div>


</template>

<script lang="ts" setup>
import { ref, onBeforeMount } from 'vue'
import { IStateModel } from "@/type/start"
import {
    get_source_list,
    get_schedule_list,
    start_schedule,
    delete_schedule
} from "@/request/api"
import { ElMessage, ElMessageBox } from 'element-plus'
import { ISchedule } from "@/type/schedule"
import Bus from '@/type/bus'

// 源判断
const whole_array = ref<IStateModel[]>([])

// 接收源清单
Bus.on('sources_array', (data) => { whole_array.value = data as IStateModel[] })

const schedule = ref(1)
const tableData = ref<ISchedule[]>([{ id: -1, keyword: "", state: "未启动", sources: whole_array.value.map(ele => ele.label), schedule: schedule.value }])

// 添加条目
const onAddItem = () => {
    tableData.value.push({ id: -1, keyword: "", state: "未启动", sources: whole_array.value.map(ele => ele.label), schedule: schedule.value })
}

// 启动定时任务
const startScheduled = (info: any) => {
    /* 提交确认 */
    ElMessageBox.confirm(
        '确认启动定时任务?',
        '消息',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'info',
            center: true,
        }
    ).then(() => {
        // 关键词校验
        if (info["keyword"] === "") {
            ElMessage.error("请输入查询关键字!")
            return
        }

        // 渠道校验
        if (info["sources"].length === 0) {
            ElMessage.error("没有选择渠道,请选择!")
            return
        }

        start_schedule(info["keyword"], info["sources"], info["schedule"]).then((res: any) => {
            if (res) {
                ElMessage({
                    type: 'success',
                    message: '定时任务启动成功~',
                })
                info["id"] = res.id
                info["state"] = res.state
            } else {
                ElMessage({
                    type: 'warning',
                    message: '定时任务启动失败!',
                })
            }
        })

    }).catch(() => {
        ElMessage({
            type: 'info',
            message: '取消启动定时任务',
        })
    })
}

// 删除定时任务
const deleteScheduled = (info: any, index: number) => {
    /* 提交确认 */
    ElMessageBox.confirm(
        '确认删除定时任务?',
        '消息',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'info',
            center: true,
        }
    )
        .then(() => {
            // 渠道校验
            if (info["id"] === -1) {
                ElMessage.error("删除ID错误")
                return
            }
            console.log(info["id"])
            delete_schedule(info["id"]).then((res: any) => {
                console.log(res)
                if (res) {
                    ElMessage({
                        type: 'success',
                        message: '定时任务删除成功~',
                    })
                    tableData.value.splice(index, 1)
                } else {
                    ElMessage({
                        type: 'warning',
                        message: '定时任务删除失败!',
                    })
                }
            })
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '取消删除定时任务',
            })
        })
}


function source_judge() {
    //获取源清单
    if (whole_array.value.length === 0) {
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
}

// 计划任务清单
function schedule_list() {
    let schedule_list: ISchedule[]
    // 获取定时方案
    get_schedule_list().then((res: any) => {
        schedule_list = res.content
        console.log(schedule_list)
        // 写入表格中
        tableData.value = []
        for (const pos in schedule_list) {
            tableData.value.push({
                id: schedule_list[pos].id,
                keyword: schedule_list[pos].keyword,
                sources: schedule_list[pos].sources,
                state: schedule_list[pos].state,
                schedule: schedule_list[pos].schedule,
            })
        }
        onAddItem()
    })
}


// 页面渲染之前的操作
onBeforeMount(() => {
    source_judge()

    // 获取定时任务清单
    schedule_list()
});

</script>


<style lang="scss" scoped>
.elTable {
    border: 1px solid black;
}
</style>