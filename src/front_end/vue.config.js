const { defineConfig } = require('@vue/cli-service')
const AutoImport = require('unplugin-auto-import/webpack')
const Components = require('unplugin-vue-components/webpack')
const { ElementPlusResolver } = require('unplugin-vue-components/resolvers')

module.exports = defineConfig({
  transpileDependencies: true,

  configureWebpack: {
    plugins: [
      AutoImport({
        resolvers: [ElementPlusResolver()],
      }),
      Components({
        resolvers: [ElementPlusResolver()],
      }),
    ],
  },

  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000/api/inspection/',
        ws: true,
        changeOrigin: false,
        pathRewrite: {
          '/api': ''
        }
      }, '/static': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }, '/log': {
        target: 'http://localhost:8000',
        ws: true,
        changeOrigin: true
      },
    }
  }
})
