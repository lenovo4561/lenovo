import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/column'
        },

        {
            path: '/',
            component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
            children: [
                {
                    path: '/column',
                    component: () => import(/* webpackChunkName: "column" */ '../components/page/Column.vue'),
                    meta: { title: '栏目配置' }
                },
                {
                    path: '/AticleEditing',
                    component: () => import(/* webpackChunkName: "column" */ '../components/page/AticleEditing.vue'),
                    meta: { title: '文章配置' }
                },
                {
                    path: '/PicEditing',
                    component: () => import(/* webpackChunkName: "column" */ '../components/page/PicEditing.vue'),
                    meta: { title: '图片配置' }
                },
                {
                    path: '/EditingArticle',
                    component: () => import(/* webpackChunkName: "column" */ '../components/page/EditingArticle.vue'),
                    meta: { title: '文章编辑' }
                },
                {
                    path: '/EditingPic',
                    component: () => import(/* webpackChunkName: "column" */ '../components/page/EditingPic.vue'),
                    meta: { title: '图片编辑' }
                },
                {
                    path: '/HomeModuleOne',
                    component: () => import(/* webpackChunkName: "HomeModuleOne" */ '../components/page/HomeModuleOne.vue'),
                    meta: { title: '首页模块一' }
                },
                {
                    path: '/HomeModuleTwo',
                    component: () => import(/* webpackChunkName: "HomeModuleTwo" */ '../components/page/HomeModuleTwo.vue'),
                    meta: { title: '首页模块二' }
                },
                {
                    path: '/EditingModuleOne',
                    component: () => import(/* webpackChunkName: "HomeModuleOne" */ '../components/page/EditingModuleOne.vue'),
                    meta: { title: '模块编辑一' }
                },
                {
                    path: '/EditingModuleTwo',
                    component: () => import(/* webpackChunkName: "HomeModuleTwo" */ '../components/page/EditingModuleTwo.vue'),
                    meta: { title: '模块编辑二' }
                },
                {
                    path: '/AboutModuleOne',
                    component: () => import(/* webpackChunkName: "AboutModuleOne" */ '../components/page/AboutModuleOne.vue'),
                    meta: { title: '模块编辑一' }
                },
                {
                    path: '/AboutModuleTwo',
                    component: () => import(/* webpackChunkName: "EditingModuleTwo" */ '../components/page/AboutModuleTwo.vue'),
                    meta: { title: '模块编辑二' }
                },
                {
                    path: '/LeaveMessage',
                    component: () => import(/* webpackChunkName: "EditingModuleTwo" */ '../components/page/LeaveMessage.vue'),
                    meta: { title: '留言列表' }
                },
                {
                    path: '/ContactUs',
                    component: () => import(/* webpackChunkName: "EditingModuleTwo" */ '../components/page/ContactUs.vue'),
                    meta: { title: '联系我们' }
                },
                {
                    path: '/ProductModuleOne',
                    component: () => import(/* webpackChunkName: "EditingModuleTwo" */ '../components/page/ProductModuleOne.vue'),
                    meta: { title: '产品分类' }
                },
                {
                    path: '/StyleModuleOne',
                    component: () => import(/* webpackChunkName: "EditingModuleTwo" */ '../components/page/StyleModuleOne.vue'),
                    meta: { title: '风格展示' }
                },
                {
                    path: '/CompanyModuleOne',
                    component: () => import(/* webpackChunkName: "EditingModuleTwo" */ '../components/page/CompanyModuleOne.vue'),
                    meta: { title: '公司动态' }
                },
            ],
        },
        {
            path: '/',
            component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
            meta: { title: '自述文件' },
            children: [
                {
                    path: '/table',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/BaseTable.vue'),
                    meta: { title: '轮播图配置' }
                },
                {
                    path: '/form',
                    component: () => import(/* webpackChunkName: "form" */ '../components/page/BaseForm.vue'),
                    meta: { title: '基本表单' }
                },
                {
                    // 富文本编辑器组件
                    path: '/editor',
                    component: () => import(/* webpackChunkName: "editor" */ '../components/page/VueEditor.vue'),
                    meta: { title: '富文本编辑器' }
                },
                {
                    // 图片上传组件
                    path: '/upload',
                    component: () => import(/* webpackChunkName: "upload" */ '../components/page/Upload.vue'),
                    meta: { title: '文件上传' }
                },
                {
                    path: '/404',
                    component: () => import(/* webpackChunkName: "404" */ '../components/page/404.vue'),
                    meta: { title: '404' }
                },
                {
                    path: '/403',
                    component: () => import(/* webpackChunkName: "403" */ '../components/page/403.vue'),
                    meta: { title: '403' }
                }
            ]
        },
        {
            path: '/login',
            component: () => import(/* webpackChunkName: "login" */ '../components/page/Login.vue'),
            meta: { title: '登录' }
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
});
