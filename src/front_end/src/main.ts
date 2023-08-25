import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'element-plus/theme-chalk/index.css'
import * as ECharts from 'echarts'
import axios from 'axios'

axios.defaults.baseURL = '/api'        //关键代码
const app = createApp(App)
app.config.globalProperties.$ECharts = ECharts
app.use(router).mount('#app')
