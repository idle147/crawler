import axios from "axios"
//创建axios实例
const service = axios.create({
    baseURL: '/api',
    timeout: 5000,
    withCredentials: true

})

//响应拦截
service.interceptors.response.use((res: { status: number; data: any; }) => {
    const code: number = res.status
    if (code == 200 || code == 201) {
        return res.data
    }
    return Promise.reject(res.data)

}, (err: string) => {
    console.log(err)
})

//向外暴露服务
export default service