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
<!--                <el-table-column align="center" prop="content" label="内容">-->
<!--                    <template slot-scope="scope">-->
<!--                        <el-collapse v-model="scope.row.content" @change="handleChange">-->
<!--                            <el-collapse-item title="一致性 Consistency" name="1">-->
<!--                                <div> {{ scope.row.content }}</div>-->
<!--                            </el-collapse-item>-->
<!--                        </el-collapse>-->
<!--                    </template>-->
<!--                </el-table-column>-->

                <el-table-column align="center" prop="created_at" label="创建时间">
                    <template slot-scope="scope">
                        {{ scope.row.created_at | timestampToTime(scope.row.created_at) }}
                    </template>
                </el-table-column>
                <el-table-column align="center" prop="remarks" label="备注">
                    <template slot-scope="scope">
                        <div class="flag_">{{ scope.row.remarks }}</div>
                    </template>
                </el-table-column>
                <el-table-column align="center" prop="is_checked" label="是否已读">
                    <template slot-scope="scope">
                        <el-switch :active-value="1" :inactive-value="0" v-model="scope.row.is_checked" @change='changeStatus($event,scope.row,scope.$index)' active-color="#13ce66"></el-switch>
                    </template>
                </el-table-column>
                <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <el-button
                                type="primary"
                                @click="handleChildrenEdit(scope.$index, scope.row)"
                        >查看</el-button>
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
        <!-- 已读信息 -->
        <el-dialog title="备注" :show-close="false" :visible.sync="editVisible" width="30%">
            <el-input
                    type="textarea"
                    placeholder="请输入内容"
                    v-model="remarks"
                    show-word-limit
            >
            </el-input>
            <span slot="footer" class="dialog-footer">
                 <el-button type="danger" @click="changeData_del">取 消</el-button>
                <el-button type="primary" @click="saveData">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 查看详情 -->
        <el-dialog title="详情" @close='del_' :visible.sync="editVisible1" width="30%">
            <el-form ref="form" :model="data2" label-width="70px">
                <el-form-item label="详细内容">
                    <el-input type="textarea" disabled v-model="data2.content"></el-input>
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>
</template>

<script>
    import { getMessageBoard,addModuleOne,changeStatus } from '../../api/index';
    export default {
        name: 'HomeModuleOne',
        data() {
            return {
                flag_index:'',
                editVisible1:false,
                remarks:'',
                editVisible:false,
                Data_del:false,
                textarea: '',
                total: undefined,
                currentPage: 1,
                pageSize: 20,
                tableData: [],
                data:{
                    id: '',
                    is_checked:'',
                    remarks:''
                },
                data2:{
                    content:''
                }
            };

        },
        created() {

        },
        methods: {
            del_() {
                this.editVisible1 = false
            },
            handleChildrenEdit(index, data) {
                this.editVisible1 = true
                this.data2.content = data.content
            },
            handleChange() {

            },
            changeData_del() {
                this.remarks = ''
                this.data2.content = ''
                this.changeData()
            },
            saveData() {
                this.changeData()
            },
            changeData() {
                this.editVisible = false
                const id = Number(this.data.id)
                this.data.id = id
                this.data.remarks = this.remarks
                changeStatus(this.data).then(res => {
                    if(res.code == 0){
                        this.$message.success(`修改成功`);
                        this.tableData[this.flag_index].remarks = this.data.remarks
                    }else{
                        this.$message.error(`修改失败`);
                    }
                });
            },
            changeStatus($event,data,index) {
                this.editVisible = true,
                this.data.id = Number(data.id),
                this.data.is_checked = $event == true ? 1 : 0
                this.remarks = data.remarks
                this.flag_index = index
            },
            handleCurrentChange(val) {
                this.currentPage = val
                this.getData()
            },
            getData() {
                var that = this
                getMessageBoard({
                    currentPage: that.currentPage,
                    pageSize: that.pageSize
                }).then(res => {
                    console.log(res.data)
                    this.tableData = res.data.data;
                    this.total = Number(res.data.total)
                });
            },
            Edit(data) {

            },
            add_column() {
                this.$router.push({
                    path: '/EditingModuleOne'
                })
            }
        },
        mounted() {
            this.getData()
        },
        filters: {
            timestampToTime(timestamp) {
                if (!timestamp) {
                    return null
                }
                var date = new Date(timestamp);
                var Y = date.getFullYear() + '-';
                var M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
                var D = (date.getDate() < 10 ? '0' + date.getDate() : date.getDate()) + ' ';
                var h = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':';
                var m = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + ':';
                var s = (date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds());
                var strDate = Y + M + D + h + m + s;
                return strDate;
            },
            filterValue(v) {
                return v == 1 ? '是' : '否';
            },
            contentType(i) {
                return i == 1 ? '普通文章' : '图片集';
            }
        }
    }
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
