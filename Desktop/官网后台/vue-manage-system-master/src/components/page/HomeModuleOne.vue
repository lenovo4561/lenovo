<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 首页模块一
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-button type="success" style="margin: 10px 0" @click="add_column">添加</el-button>
            <el-table
                    :data="tableData"
                    border
                    row-key="id"
                    class="table"
                    ref="multipleTable"
                    header-cell-class-name="table-header"
                    :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
            >
                <el-table-column type="index" label="序号" width="55" align="center"></el-table-column>
                <el-table-column align="center" prop="alt" label="描述"></el-table-column>
                <el-table-column align="center" prop="path" label="path"></el-table-column>
                <el-table-column label="是否外链" width="155">
                    <template slot-scope="scope">{{scope.row.is_link | filterValue(scope.row.is_link)}}</template>
                </el-table-column>
                <el-table-column label="banner图" align="center" width="155">
                    <template slot-scope="scope">
                        <el-image
                                class="table-td-thumb"
                                :src="scope.row.url"
                                :preview-src-list="[scope.row.url]"
                        ></el-image>
                    </template>
                </el-table-column>
                <el-table-column align="center" prop="created_at" label="创建时间">
                    <template slot-scope="scope">
                        {{ scope.row.created_at | timestampToTime(scope.row.created_at) }}
                    </template>
                </el-table-column>
                <el-table-column align="center" prop="updated_at" label="更新时间">
                    <template slot-scope="scope">
                        {{ scope.row.updated_at | timestampToTime(scope.row.updated_at) }}
                    </template>
                </el-table-column>
                <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <el-button
                                v-if="scope.row.path"
                                type="warning"
                                @click="Edit(scope.row)"
                        >编辑</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>
    import { getModuleOne,addModuleOne } from '../../api/index';
    export default {
        name: 'HomeModuleOne',
        data() {
            return {
                tableData: [],
            };

        },
        created() {

        },
        methods: {
            getData() {
                getModuleOne().then(res => {
                    this.tableData = res.data.data;
                });
            },
            Edit(data){
                const id = data.id
                this.$router.push({
                    path: '/EditingModuleOne',
                    query:{id}
                })
            },
            add_column(){
                this.$router.push({
                    path: '/EditingModuleOne'
                })
            }
        },
        mounted() {
            this.getData()
        },
        filters: {
            timestampToTime (timestamp) {
                if(!timestamp){return null}
                var date = new Date(timestamp);
                var Y = date.getFullYear() + '-';
                var M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
                var D = (date.getDate() < 10 ? '0'+date.getDate() : date.getDate()) + ' ';
                var h = (date.getHours() < 10 ? '0'+date.getHours() : date.getHours()) + ':';
                var m = (date.getMinutes() < 10 ? '0'+date.getMinutes() : date.getMinutes()) + ':';
                var s = (date.getSeconds() < 10 ? '0'+date.getSeconds() : date.getSeconds());
                var strDate = Y+M+D+h+m+s;
                return strDate;
            },
            filterValue (v) {
                return  v == 1? '是' : '否';
            },
            contentType(i){
                return  i == 1? '普通文章' : '图片集';
            }
        },
    };
</script>

<style scoped>
    .handle-box {
        margin-bottom: 20px;
    }

    .handle-select {
        width: 120px;
    }

    .handle-input {
        width: 300px;
        display: inline-block;
    }
    .table {
        width: 100%;
        font-size: 14px;
    }
    .red {
        color: #ff0000;
    }
    .mr10 {
        margin-right: 10px;
    }
    .table-td-thumb {
        display: block;
        margin: auto;
        width: 40px;
        height: 40px;
    }
</style>
