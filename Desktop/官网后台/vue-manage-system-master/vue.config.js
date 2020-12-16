module.exports = {
    assetsDir: 'mhwStatic',
    productionSourceMap: false,
    devServer: {
        proxy: {
            '/':{
                target:'http://192.168.124.6:8989',
                changeOrigin:true,
                pathRewrite:{
                    '/':''
                }
            }
        }
    }
}
