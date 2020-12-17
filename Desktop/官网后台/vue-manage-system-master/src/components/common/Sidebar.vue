<template>
    <div class="sidebar">
        <el-menu
            class="sidebar-el-menu"
            :default-active="onRoutes"
            :collapse="collapse"
            background-color="#324157"
            text-color="#bfcbd9"
            active-text-color="#20a0ff"
            unique-opened
            router
        >
            <template v-for="item in items">
                <template v-if="item.subs">
                    <el-submenu :index="item.index" :key="item.index">
                        <template slot="title">
                            <i :class="item.icon"></i>
                            <span slot="title">{{ item.title }}</span>
                        </template>
                        <template v-for="subItem in item.subs">
                            <el-submenu
                                v-if="subItem.subs"
                                :index="subItem.index"
                                :key="subItem.index"
                            >
                                <template slot="title">{{ subItem.title }}</template>
                                <el-menu-item
                                    v-for="(threeItem,i) in subItem.subs"
                                    :key="i"
                                    :index="threeItem.index"
                                >{{ threeItem.title }}</el-menu-item>
                            </el-submenu>
                            <el-menu-item
                                v-else
                                :index="subItem.index"
                                :key="subItem.index"
                            >{{ subItem.title }}</el-menu-item>
                        </template>
                    </el-submenu>
                </template>
                <template v-else>
                    <el-menu-item :index="item.index" :key="item.index">
                        <i :class="item.icon"></i>
                        <span slot="title">{{ item.title }}</span>
                    </el-menu-item>
                </template>
            </template>
        </el-menu>
    </div>
</template>

<script>
import bus from '../common/bus';
export default {
    data() {
        return {
            collapse: false,
            items: [
                {
                    icon: 'el-icon-lx-home',
                    index: 'column',
                    title: '栏目配置'
                },
                {
                    icon: 'el-icon-lx-calendar',
                    index: '4',
                    title: '内容管理',
                    subs: [
                        {
                            index: 'AticleEditing',
                            title: '文章集'
                        },
                        {
                            index: 'PicEditing',
                            title: '图片集'
                        }
                    ]
                },
                {
                    icon: 'el-icon-lx-copy',
                    index: '5',
                    title: '模块配置',
                    subs: [
                        {
                            index: '3-1',
                            title: '首页模块',
                            subs: [
                                {
                                    index: 'HomeModuleOne',
                                    title: '模块一'
                                },
                                {
                                    index: 'HomeModuleTwo',
                                    title: '模块二'
                                },
                            ]
                        },
                        {
                            index: '3-2',
                            title: '关于模块',
                            subs: [
                                {
                                    index: 'AboutModuleOne',
                                    title: '模块一'
                                },
                                {
                                    index: 'AboutModuleTwo',
                                    title: '模块二'
                                },
                            ]
                        },
                        {
                            index: '3-3',
                            title: '产品分类模块',
                            subs: [
                                {
                                    index: 'ProductModuleOne',
                                    title: '模块一'
                                }
                            ]
                        },
                        {
                            index: '3-4',
                            title: '风格展示模块',
                            subs: [
                                {
                                    index: 'StyleModuleOne',
                                    title: '模块一'
                                }
                            ]
                        },
                        {
                            index: '3-5',
                            title: '企业动态模块',
                            subs: [
                                {
                                    index: 'CompanyModuleOne',
                                    title: '模块一'
                                }
                            ]
                        },
                    ]
                },
                {
                    icon: 'el-icon-c-scale-to-original',
                    index: 'ContactUs',
                    title: '联系我们'
                },
                {
                    icon: 'el-icon-s-comment',
                    index: 'LeaveMessage',
                    title: '留言列表'
                },
                // {
                //     icon: 'el-icon-lx-calendar',
                //     index: '3',
                //     title: '表单相关',
                //     subs: [
                //         {
                //             index: 'form',
                //             title: '基本表单'
                //         },
                //         {
                //             index: '3-2',
                //             title: '三级菜单',
                //             subs: [
                //                 {
                //                     index: 'editor',
                //                     title: '富文本编辑器'
                //                 },
                //             ]
                //         },
                //         {
                //             index: 'upload',
                //             title: '文件上传'
                //         }
                //     ]
                // },
            ]
        };
    },
    computed: {
        onRoutes() {
            return this.$route.path.replace('/', '');
        }
    },
    created() {
        // 通过 Event Bus 进行组件间通信，来折叠侧边栏
        bus.$on('collapse', msg => {
            this.collapse = msg;
            bus.$emit('collapse-content', msg);
        });
    }
};
</script>

<style scoped>
.sidebar {
    display: block;
    position: absolute;
    left: 0;
    top: 70px;
    bottom: 0;
    overflow-y: scroll;
}
.sidebar::-webkit-scrollbar {
    width: 0;
}
.sidebar-el-menu:not(.el-menu--collapse) {
    width: 250px;
}
.sidebar > ul {
    height: 100%;
}
</style>
