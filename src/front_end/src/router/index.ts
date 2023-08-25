import { createRouter, createWebHashHistory, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    redirect: "index", //路由重定向
    children: [{
      path: "/index",
      name: "index",
      meta: {
        isShow: true,
        title: "首页"
      },
      component: () => import(/* webpackChunkName: "index" */ '../views/IndexView.vue')
    }, {
      path: "/scheduled",
      name: "scheduled",
      meta: {
        isShow: true,
        title: "定时计划"
      },
      component: () => import(/* webpackChunkName: "details" */ '../views/ScheduledView.vue')
    }, {
      path: "/details",
      name: "details",
      meta: {
        isShow: false,
        title: "查看详情"
      },
      component: () => import(/* webpackChunkName: "details" */ '../views/DetailsView.vue')
    }, {
      path: '/check',
      name: 'check',
      meta: {
        isShow: true,
        title: "盗版查看"
      },
      component: () => import(/* webpackChunkName: "check" */ '../views/CheckView.vue')
    }, {
      path: '/data',
      name: 'data',
      meta: {
        isShow: true,
        title: "数据报表"
      },
      component: () => import(/* webpackChunkName: "data" */ '../views/ChartView.vue')
    }, {
      path: '/login',
      name: 'login',
      meta: {
        isShow: true,
        title: "登录页面"
      },
      component: () => import(/* webpackChunkName: "login" */ '../views/LoginView.vue')
    }]
  }, {
    path: '/log',
    name: 'log',
    component: () =>
      import(/* webpackChunkName:"log" */'@/views/LogView.vue')
  }
]

const router = createRouter({
  // history: createWebHistory(process.env.BASE_URL),
  history: createWebHashHistory(),
  routes
})

// 全局守卫：登录拦截 本地没有存token,请重新登录
router.beforeEach((to, from, next) => {
  const token: string | null = localStorage.getItem('username')
  // 判断有没有登录
  if (!token && to.path !== '/login') {
    next('/login')
  } else {
    next()
  }
});

export default router
