<template>
  <!-- 盗版游戏检查 -->
  <el-table class="elTable" :data="table_data" border :header-cell-style="{
    background: '#2c3e50',
    color: '#bdc3c7',
    borderColor: 'black',
  }" :cell-style="{ borderColor: 'black' }">
    <el-table-column align="center" prop="title" label="标题" width="180" />
    <el-table-column align="center" prop="icon" label="图标">
      <template #default="scope">
        <el-image style="width: 128px; height: 128px" :src="scope.row.icon" fit="cover" />
      </template>
    </el-table-column>
    <el-table-column align="center" prop="link" label="链接">
      <template #default="scope">
        <a :href="scope.row.link"> {{ scope.row.link }} </a>
      </template>
    </el-table-column>
    <el-table-column align="center" prop="content" label="描述" />
    <el-table-column align="center" prop="source" label="渠道" />
  </el-table>
</template>

<script lang="ts" setup>
import { get_piracy_info } from "@/request/api"
import { ref } from 'vue'
import { ICheck } from "@/type/check"

let table_data = ref<ICheck[]>([])

get_piracy_info().then((res) => {
  table_data.value = res.content
  console.log(table_data)
})
</script>

<style lang="scss" scoped>
.elTable {
  border: 1px solid black;
}
</style>