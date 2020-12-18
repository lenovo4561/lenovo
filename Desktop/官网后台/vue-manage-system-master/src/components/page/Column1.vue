<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 栏目配置
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-button type="success" style="margin: 10px 0" @click="add_column">添加栏目</el-button>
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
                <el-table-column align="left" prop="name" label="栏目名"></el-table-column>
                <el-table-column align="center" prop="path" label="path"></el-table-column>
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
                <el-table-column align="center" prop="is_show" label="是否开启">
                    <template slot-scope="scope">
                        <el-switch :active-value="1" :inactive-value="0" v-model="scope.row.is_show" @change='changeStatus($event,scope.row,scope.$index)' active-color="#13ce66"></el-switch>
                    </template>
                </el-table-column>
                <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <el-button
                                v-if="scope.row.class_info == 1"
                                type="primary"
                                @click="handleChildrenEdit(scope.$index, scope.row)"
                        >编辑内容(文章)</el-button>
                        <el-button
                                v-else-if="scope.row.class_info == 2"
                                type="primary"
                                @click="handleChildrenEdit(scope.$index, scope.row)"
                        >编辑内容(图片)</el-button>
                        <el-button
                                type="primary"
                                @click="handleEdit(scope.$index, scope.row)"
                        >编辑</el-button>
                        <el-button
                                v-if="scope.row.path"
                                type="success"
                                @click="addChildren(scope.row)"
                        >添加子类</el-button>
                        <el-button
                                v-if="scope.row.path"
                                type="warning"
                                @click="addColumnSEO(scope.row)"
                        >配置SEO</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <!-- 添加弹出框 -->
        <el-dialog title="添加" :visible.sync="editVisible1" @close='del_column' width="30%">
            <el-form ref="form" :model="form" label-width="70px">
                <el-form-item label="栏目名">
                    <el-input v-model="add_column_data.name"></el-input>
                </el-form-item>
                <el-form-item label="path">
                    <el-input v-model="add_column_data.path"></el-input>
                </el-form-item>
                <el-form-item label="是否外链">
                    <el-select v-model="value1" @change="select1" placeholder="请选择">
                        <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="del_column">取 消</el-button>
                <el-button type="primary" @click="add">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%" @close='edit_column_del'>
            <el-form ref="form" :model="formData" label-width="70px">
                <el-form-item label="分类名">
                    <el-input v-model="formData.name"></el-input>
                </el-form-item>
                <el-form-item label="path">
                    <el-input v-model="formData.path"></el-input>
                </el-form-item>
                <el-form-item label="是否外链">
                    <el-select v-model="value" @change="select" placeholder="请选择">
                        <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="edit_column_del">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 子类编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible4" width="30%" @close='edit_children_del'>
            <el-form ref="form" :model="formData_" label-width="70px">
                <el-form-item label="分类名">
                    <el-input v-model="formData_.name"></el-input>
                </el-form-item>
                <el-form-item label="内容类型">
                    <el-select v-model="value4" @change="select4" placeholder="请选择">
                        <el-option
                                v-for="item in options1"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="edit_children_del">取 消</el-button>
                <el-button type="primary" @click="saveChildren">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 添加子类弹出框 -->
        <el-dialog title="添加子类" :visible.sync="editVisible2" width="30%" @close='edit_childrenColumn_del'>
            <el-form ref="form" :model="childrenformData" label-width="70px">
                <el-form-item label="子分类名">
                    <el-input v-model="childrenformData.name"></el-input>
                </el-form-item>
                <el-form-item label="内容类型">
                    <el-select v-model="value2" @change="select2" placeholder="请选择">
                        <el-option
                                v-for="item in options1"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="edit_childrenColumn_del">取 消</el-button>
                <el-button type="primary" @click="saveChildrenEdit">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 添加栏目SEO弹出框 -->
        <el-dialog title="栏目SEO信息" :visible.sync="editVisible3" width="30%" @close='ColumnSEOData_del'>
            <el-form ref="form" :model="ColumnSEOData" label-width="70px">
                <el-form-item label="栏目标题">
                    <el-input v-model="ColumnSEOData.title"></el-input>
                </el-form-item>
                <el-form-item label="栏目关键字">
                    <el-input v-model="ColumnSEOData.keywords"></el-input>
                </el-form-item>
                <el-form-item label="栏目描述">
                    <el-input v-model="ColumnSEOData.description"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="ColumnSEOData_del">取 消</el-button>
                <el-button type="primary" @click="saveColumnSEOData">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import { getData,editColumn,addColumn,getAllColumn,addChildrenColumn,addColumnSEO,EditColumnSEO,editChildren,getSEOMsg} from '../../api/index';
    export default {
        name: 'column',
        data() {
            return {
                flag_:'',
                editVisible1: false,
                value1: '',
                add_column_data:{
                    name:'',
                    path:'',
                    is_link:0
                },

                tableData: [],
                editVisible: false,
                form: {
                    name:'',
                    path:'',
                    is_link:0
                },

                options: [{
                    value: '1',
                    label: '是'
                }, {
                    value: '0',
                    label: '否'
                }],
                options1: [{
                    value: '1',
                    label: '普通文章'
                }, {
                    value: '2',
                    label: '图片集'
                }],
                value: '',
                formData:{
                    id:'',
                    name:'',
                    path:'',
                    is_link:0
                },

                editVisible2: false,
                childrenformData: {
                    parentId:'',
                    name:'',
                    classId:''
                },
                value2: '',


                editVisible4: false,
                formData_: {
                    parentId:'',
                    name:'',
                    classId:''
                },
                value4: '',


                editVisible3: false,
                ColumnSEOData: {
                    moduleId:'',
                    title: '',
                    keywords: '',
                    description: ''
                }
            };

        },
        created() {
            this.getData();
        },
        methods: {
            changeStatus($event,data,index) {
                let id = Number(data.id)
                let is_checked = $event == true ? 1 : 0
                let DATA = {
                    uploadId:id,
                    is_show:is_checked
                }
                if(!data.class_info){
                    editColumn(DATA).then(res => {
                        if(res.code == 0) {
                            this.$message.success(`修改成功`);
                        }else{
                            this.$message.error(`修改失败`);
                        }
                    })
                }else{
                    editChildren(DATA).then(res => {
                        if(res.code == 0) {
                            this.$message.success(`修改成功`);
                        }else{
                            this.$message.error(`修改失败`);
                        }
                    })
                }

            },

            addChildren(item) {
                this.editVisible2 = true
                this.childrenformData.parentId = item.id
            },
            add(){
                addColumn(this.add_column_data).then(res => {
                    this.add_column_data = {
                        name:'',
                        path:'',
                        is_link:''
                    }
                    this.value1 = ''
                    if(res.code == 0) {
                        this.editVisible1 = false;
                        this.getData()
                        this.$message.success(`修改成功`);
                    }else{
                        this.$message.error(`修改失败`);
                    }
                }).catch((e)=>{
                    this.$message.error(`修改失败`);
                });
            },
            select1(value) {
                this.add_column_data.is_link = Number(value)
                this.value1 = value == 1 ? '是' : '否'
            },
            del_column() {
                this.editVisible1 = false
                this.add_column_data = {
                    name:'',
                    path:'',
                    is_link:''
                }
                this.value1 = ''
            },
            add_column() {
                this.editVisible1 = true
                this.value1 = '否'
            },
            select(value) {
                this.formData.is_link = value
            },
            edit_column_del() {
                this.editVisible = false
                this.formData = {
                    name:'',
                    path:'',
                    is_link:''
                }
                this.value1 = ''
            },
            getData() {
                getAllColumn().then(res => {
                    this.tableData = res.data.data;
                });
            },
            // 编辑操作
            handleEdit(index, row) {
                console.log(row);
                if(row.class_info){
                    this.formData_ = {...row}
                    this.editVisible4 = true;
                    this.value4 = row.class_info == 1 ? '普通文章' : '图片集'
                }else{
                    this.formData = {...row}
                    this.editVisible = true;
                    this.value = row.is_link == 1 ? '是' : '否'
                }
            },
            // 子类编辑操作
            handleChildrenEdit(index, row) {
                console.log(row)
                const type = row.class_info
                const id = row.id
                if(type == 1){
                    this.$router.push({
                        path: '/AticleEditing',
                        query: {id}
                    })
                }else{
                    this.$router.push({
                        path: '/PicEditing',
                        query: {id}
                    })
                }
            },
            // 保存编辑
            saveEdit() {
                var that = this
                this.editVisible = false;
                editColumn(this.formData).then(res => {
                    this.formData = {
                        name:'',
                        path:'',
                        is_link:''
                    }
                    console.log(res)
                    if(res.code == 0) {
                        this.$message.success(`修改成功`);
                        that.getData()
                    }else{
                        that.$message.error(`修改失败`);
                    }
                }).catch((e)=>{
                    that.$message.error(`修改失败`);
                });
            },
            edit_column_del() {
                this.editVisible = false
                this.add_column_data = {
                    name:'',
                    path:'',
                    is_link:''
                }
                this.value1 = ''
            },

            edit_children_del() {
                this.editVisible4 = false
                this.formData_ = {
                    parentId:'',
                    name:'',
                    classId:''
                }
                this.value4 = ''
            },
            select4(value) {
                this.formData_.classId = Number(value)
                this.value4 = value == 1 ? '普通文章集' : '图片集'
            },
            saveChildren() {
                var that = this
                this.editVisible4 = false;
                editChildren(this.formData_).then(res => {
                    this.formData_ = {
                        parentId:'',
                        name:'',
                        classId:''
                    }
                    if(res.code == 0) {
                        this.$message.success(`修改成功`);
                        that.getData()
                    }else{
                        if(res.code == 422){
                            that.$message.error(`栏目名存在相同的`);
                        }else{
                            that.$message.error(`修改失败`);
                        }
                    }
                }).catch((e)=>{
                    that.$message.error(`修改失败`);
                });
            },

            edit_childrenColumn_del(){
                this.editVisible2 = false
                this.childrenformData = {
                    parentId:'',
                    name:'',
                    classId:''
                },
                    this.value2 = ''
            },
            select2(value) {
                this.childrenformData.classId = Number(value)
                this.value2 = value == 1 ? '普通文章' : '图片集'
            },
            saveChildrenEdit() {
                var that = this
                this.editVisible2 = false;
                addChildrenColumn(this.childrenformData).then(res => {
                    this.childrenformData = {
                        parentId:'',
                        name:'',
                        classId:''
                    }
                    if(res.code == 0) {
                        this.$message.success(`修改成功`);
                        that.getData()
                    }else{
                        if(res.code == 422){
                            that.$message.error(`栏目名存在相同的`);
                        }else{
                            that.$message.error(`修改失败`);
                        }

                    }
                }).catch((e)=>{
                    that.$message.error(`修改失败`);
                });
            },

            addColumnSEO(data) {
                this.editVisible3 = true;
                getSEOMsg({id:data.id}).then(res => {
                    if(res.code == 0){
                        this.ColumnSEOData.title = res.data.data.title
                        this.ColumnSEOData.keywords = res.data.data.keywords
                        this.ColumnSEOData.description = res.data.data.description
                        this.flag_ = true
                    }
                });
                this.ColumnSEOData.moduleId = data.id
            },
            ColumnSEOData_del(){
                this.editVisible3 = false
                this.ColumnSEOData = {
                    moduleId:'',
                    title: '',
                    keywords: '',
                    description: ''
                }
                this.flag_ = ''
            },
            saveColumnSEOData(){
                console.log(this.ColumnSEOData)
                if(this.flag_){
                    EditColumnSEO(this.ColumnSEOData).then(res => {
                        this.editVisible3 = false;
                        this.flag_ = ''
                        this.ColumnSEOData = {
                            moduleId:'',
                            title: '',
                            keywords: '',
                            description: ''
                        }
                        if(res.code == 0){
                            this.$message.success(`修改成功`);
                        }else{
                            this.$message.error(`修改失败`);
                        }
                    });
                }else{
                    addColumnSEO(this.ColumnSEOData).then(res => {
                        this.editVisible3 = false
                        this.flag_ = ''
                        this.ColumnSEOData = {
                            moduleId:'',
                            title: '',
                            keywords: '',
                            description: ''
                        }
                        if(res.code == 0){
                            this.$message.success(`添加成功`);
                        }else{
                            this.$message.error(`添加失败`);
                        }
                    });
                }
            }


        },
        mounted() {

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
