<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 轮播图配置
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-table
                :data="tableData"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
            >
                <el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
                <el-table-column prop="alt" label="banner描述" width="355"></el-table-column>
                <el-table-column label="是否外链" width="155">
                    <template slot-scope="scope">{{scope.row.isLink}}</template>
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
                <el-table-column prop="path" label="path" width="155"></el-table-column>

                <el-table-column prop="url" label="url"></el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-edit"
                            @click="handleEdit(scope.$index, scope.row)"
                        >编辑</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="32%">
            <el-form ref="form" :model="form" label-width="70px">
                <el-form-item label="图片描述">
                    <el-input v-model="form.alt"></el-input>
                </el-form-item>
                <el-form-item label="path">
                    <el-input v-model="form.path"></el-input>
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
                <el-form-item label="上传图片">
                    <el-upload
                            ref="upload"
                            class="upload-demo"
                            action="string"
                            accept="image/jpeg,image/png,image/jpg"
                            :before-upload="onBeforeUploadImage"
                            :http-request="UploadImage"
                            :on-change="fileChange"
                            :file-list="fileList"
                            list-type="picture">
                        <el-button size="small" type="primary">Click to upload</el-button>
                        <div slot="tip" class="el-upload__tip">jpg/png files with a size less than 500kb</div>
                    </el-upload>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="del">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { getData,editData} from '../../api/index';
export default {
    name: 'basetable',
    data() {
        return {
            tableData: [],
            delList: [],
            editVisible: false,
            form: {},

            options: [{
                value: '1',
                label: '是'
            }, {
                value: '0',
                label: '否'
            }],
            value: '',
            fileList: [{name: '', url: ''}],
            formData:{
                id:'',
                alt:'',
                path:'',
                isLink:''
            }
        };

    },
    created() {
        this.getData();
    },
    methods: {
        select(value) {
            this.formData.isLink = value
        },
        del() {
            this.editVisible = false
            this.formData = new FormData()
        },
        onBeforeUploadImage(file) {
            const isIMAGE = file.type === 'image/jpeg' || 'image/jpg' || 'image/png'
            const isLt1M = file.size / 1024 / 1024 < 1
            if (!isIMAGE) {
                this.$message.error('上传文件只能是图片格式!')
            }
            if (!isLt1M) {
                this.$message.error('上传文件大小不能超过 1MB!')
            }
            return isIMAGE && isLt1M
        },
        UploadImage(param){
            this.formData.append('file', param.file)
        },
        fileChange(file){
            this.$refs.upload.clearFiles() //清除文件对象
            this.logo = file.raw // 取出上传文件的对象，在其它地方也可以使用
            this.fileList = [{name: file.name, url: file.url}] // 重新手动赋值filstList， 免得自定义上传成功了, 而fileList并没有动态改变， 这样每次都是上传一个对象
        },
        // 获取 easy-mock 的模拟数据
        getData() {
            getData().then(res => {
                console.log(res);
                this.tableData = res.data.data;
            });
        },
        // 删除操作
        handleDelete(index, row) {
            // 二次确认删除
            this.$confirm('确定要删除吗？', '提示', {
                type: 'warning'
            })
                .then(() => {
                    this.$message.success('删除成功');
                    this.tableData.splice(index, 1);
                })
                .catch(() => {});
        },
        // 编辑操作
        handleEdit(index, row) {
            this.idx = index;
            this.form = row;
            this.fileList=[{name: row.alt, url: row.url}],
            this.editVisible = true;
            this.value = row.isLink == 1 ? '是' : '否'
        },
        // 保存编辑
        saveEdit() {
            var that = this
            this.editVisible = false;
            this.formData.append('alt', this.form.alt)
            this.formData.append('path', this.form.path)
            this.formData.append('isLink', this.form.isLink)
            this.formData.append('id', Number(this.form.id))
            console.log(this.form)
            console.log(this.formData)
            editData(this.formData).then(res => {
                console.log(res)
                if(res.code == 0) {
                    this.$message.success(`修改成功`);
                    that.formData = new FormData()
                    that.getData()
                }else{
                    that.$message.error(`修改失败`);
                }
            }).catch((e)=>{
                that.$message.error(`修改失败`);
                that.formData = new FormData()
            });
        },
    },
    mounted() {
        this.formData = new FormData()
    }
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
