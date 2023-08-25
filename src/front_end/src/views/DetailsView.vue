<template>
    <!-- 查看详情 -->
    <div style="margin-bottom: 20px">
    </div>
    <el-tabs v-model="editableTabsValue" type="border-card" class="demo-tabs">
        <el-tab-pane v-for="item in editableTabs" :key="item" :label="item" :name="item">
            <el-table class="elTable" style="width: 100%" border :data="show_list" :header-cell-style="{
                background: '#FFEFBA',
                color: '#606266',
                borderColor: 'black',
            }" :cell-style="{ borderColor: 'black' }">
                <el-table-column align="center" v-for="(data, index) in tableHeader" :key="index" :prop="data.prop"
                    :label="data.label">

                    <template #default="scope">
                        <template v-if="data.prop === 'is_piracy'">
                            <el-button :icon="Edit" type="primary" round v-if="!scope.row[data.prop]"
                                @click.stop="sign_piracy(scope.row)">
                                标记为盗版
                            </el-button>
                            <span type="info" round v-else style="color: red">已标记</span>
                        </template>
                        <template v-else-if="data.prop === 'icon'">
                            <el-image style="width: 128px; height: 128px" :src="scope.row[data.prop]" fit="cover" />
                        </template>
                        <template v-else-if="data.prop === 'link'">
                            <a :href="scope.row[data.prop]"> {{ scope.row[data.prop] }}</a>
                        </template>
                        <template v-else>{{ scope.row[data.prop] }}</template>
                    </template>

                </el-table-column>
            </el-table>
            <el-pagination background layout="total, prev, pager, next" :hide-on-single-page="hide_value"
                :page-size="pagination.page_size" :total="pagination.length" @current-change="currentChange"
                @size-change="sizeChange" />
        </el-tab-pane>
    </el-tabs>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { IDetailData } from "@/type/search"
import { get_detail_list, put_piracy } from "@/request/api"
import { ElMessage } from 'element-plus'
import { Edit } from '@element-plus/icons-vue'
import { useRoute } from "vue-router"
import { Pagination } from "@/function/pagination"

const currentRoute = useRoute()
const editableTabsValue = ref('0')
const editableTabs = ref<string[]>([])
const hide_value = ref(true);   //隐藏的value
const pagination = ref<Pagination>(new Pagination([]))


// 表头数据
const tableHeader = [
    { prop: "title", label: "标题" },
    { prop: "icon", label: "图标" },
    { prop: "link", label: "链接" },
    { prop: "content", label: "描述" },
    { prop: "source", label: "渠道" },
    { prop: "is_piracy", label: "操作" }
]

//表格数据
const date = currentRoute.query.date as string
const sources = currentRoute.query.sources as string
editableTabs.value = sources.split(",")

get_detail_list(date).then((res: any) => {
    pagination.value.data_list = res.content
    let tab_set = new Set()
    for (let entry in res.content) {
        // 创建标签
        console.log(entry)
        tab_set.add(res.content[entry]["source"])
    }
    editableTabsValue.value = editableTabs.value[0]
})

//表格内数据的构建
const show_list = computed(() => {
    return pagination.value.filter({
        source: editableTabsValue.value,
    })
})

const sign_piracy = (row_info: IDetailData) => {
    put_piracy(row_info.id).then((res: any) => {
        if (res["message"] === "success") {
            ElMessage({
                showClose: true,
                message: "成功标记为盗版",
                type: "success",
            })
            // 修改控件
            row_info.is_piracy = true
        } else {
            ElMessage({
                showClose: true,
                message: "标记盗版失败",
                type: "warning",
            })
        }
    })
}

// 当前页改变时触发
const currentChange = (page: number) => {
    pagination.value.page = page
}

// 当单页数量改变时触发
const sizeChange = (page_size: number) => {
    pagination.value.page_size = page_size
}
</script>

<style lang="scss" scoped>
.demo-tabs>.el-tabs__content {
    padding: 48px;
    color: #277BC0;
    font-size: 48px;
    font-weight: 600;
}

.demo-tabs .custom-tabs-label .el-icon {
    vertical-align: middle;
    margin-left: 4px;
}

.elTable {
    border: 1px solid black;
}

.el-pagination {
    margin-top: 20px;
    display: flex;
    justify-content: right;
}
</style>
