<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 留言列表
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
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
                <el-table-column align="center" prop="name" label="姓名"></el-table-column>
                <el-table-column align="center" prop="phone" label="手机号"></el-table-column>
                <el-table-column align="center" prop="content" label="内容">
                    <template slot-scope="scope">
                        <div class="flag_">{{ scope.row.content }}</div>
                    </template>
                </el-table-column>
                <el-table-column align="center" prop="created_at" label="创建时间">
                    <template slot-scope="scope">
                        {{ scope.row.created_at | timestampToTime(scope.row.created_at) }}
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                    :hide-on-single-page="total <= 20"
                    style="margin-top: 20px"
                    background
                    layout="prev, pager, next"
                    :page-size="20"
                    @current-change="handleCurrentChange"
                    :total="total">
            </el-pagination>
        </div>
    </div>
</template>

<script>
    import { getMessageBoard,addModuleOne } from '../../api/index';
    export default {
        name: 'HomeModuleOne',
        data() {
            return {
                total:undefined,
                currentPage:1,
                pageSize:20,
                tableData: [],
            };

        },
        created() {

        },
        methods: {
            handleCurrentChange(val) {
                this.currentPage = val
                this.getMessageBoard()
            },
            getData() {
                var that = this
                getMessageBoard({
                    currentPage: that.currentPage,
                    pageSize : that.pageSize
                }).then(res => {
                    console.log(res.data)
                    this.tableData = res.data.data;
                    this.total = Number(res.data.total)
                });
            },
            Edit(data){

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
    .flag_ {
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        line-clamp: 2;
        -webkit-box-orient: vertical;
    }
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
