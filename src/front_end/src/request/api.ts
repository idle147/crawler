import service from "@/request/index";
// 登录接口
// 采用页面重定向方式

// 登出接口
export function logout() {
    return service({
        url: "logout",
        method: "get",
    })
}

// 登录状态判断接口
export function login_judge() {
    return service({
        url: "loginJudge",
        method: "get"
    })
}

// 查看详细数据接口
export function get_source_list() {

    return service({
        url: "source",
        method: "get"
    })
}

// 启动爬虫任务
export function start(keyword: string, sources: string[]) {

    return service({
        url: "start",
        method: "post",
        xsrfCookieName: "csrftoken",
        xsrfHeaderName: "X-CSRFToken",
        data: {
            keyword: keyword,
            sources: sources
        }
    })
}


//中止任务
export function put_end_mission(key: string) {
    return service({
        url: "kill",
        method: "put",
        xsrfCookieName: "csrftoken",
        xsrfHeaderName: "X-CSRFToken",
        data: {
            date: key
        },
    })
}

// 查看详细数据接口
export function get_detail_list(time: string) {
    return service({
        url: "detail",
        method: "get",
        params: {
            date: time
        },
    })
}

// 查看状态接口
export function get_state_list() {
    return service({
        url: "state",
        method: "get"
    })
}


//获取盗版信息
export function get_piracy_info() {
    return service({
        url: "piracyList",
        method: "get",
    })
}

//标记为盗版接口
export function put_piracy(num: number) {
    return service({
        url: "piracyMark",
        method: "put",
        xsrfCookieName: "csrftoken",
        xsrfHeaderName: "X-CSRFToken",
        data: {
            id: num
        },
    })
}


//获取线图数据
export function get_line_data() {
    return service({
        url: "lineChart",
        method: "get"
    })
}

//获取线图数据
export function get_pie_data() {
    return service({
        url: "pieChart",
        method: "get"
    })
}

//获取定时任务接口
export function get_schedule_list() {
    return service({
        url: "scheduled",
        method: "get"
    })
}

//启动定时任务接口
export function start_schedule(keyword: string, source: string[], time: number) {
    return service({
        url: "scheduled",
        method: "post",
        xsrfCookieName: "csrftoken",
        xsrfHeaderName: "X-CSRFToken",
        data: {
            keyword: keyword,
            sources: source,
            time: time
        },
    })
}


//删除定时任务接口
export function delete_schedule(id_info: number) {
    return service({
        url: "scheduled",
        method: "delete",
        xsrfCookieName: "csrftoken",
        xsrfHeaderName: "X-CSRFToken",
        data: {
            id: id_info
        }
    })
}