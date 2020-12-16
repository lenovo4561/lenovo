<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 企业动态模块编辑
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <UploadComponent :fileList="fileList" @PicID="PicID"/>
                <el-form ref="form" :model="form" label-width="80px" style="margin-top: 50px">
                    <el-form-item label="title">
                        <el-input v-model="form.title"></el-input>
                    </el-form-item>
                    <el-form-item label="alt">
                        <el-input v-model="form.alt"></el-input>
                    </el-form-item>
                    <el-form-item label="desc">
                        <el-input v-model="form.desc"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit">表单提交</el-button>
                        <el-button>取消</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%" @close='edit_artcle_del'>
            <VueEditorComponent :proData="proData" :content="contentData" @aaa="adasd" />
        </el-dialog>
    </div>
</template>

<script>
    import { editEnterprisetrendsModuleOne,getEnterprisetrendsModuleOne,addEnterprisetrendsModuleOne } from '../../api/index';
    import UploadComponent from '../common/Upload'
    import VueEditorComponent from '../common/VueEditor'
    import bus from '../common/bus';
    export default {
        name: 'CompanyModuleOne',
        components: {
            UploadComponent,
            VueEditorComponent
        },
        data() {
            return {
                value:'',
                fileList: [],
                contentData: '',
                form: {},
                proData:'',
                editVisible:false,
            };
        },
        methods: {
            PicID(v) {
                this.form.uploadId = v
            },
            select(value){
                this.form.is_link = Number(value)
            },
            getData() {
                getEnterprisetrendsModuleOne().then(res => {
                    if(res.code == 0){
                        this.flag_ = true
                        this.form = res.data.data
                        this.value = res.data.data.is_link == 0 ? '否':'是'
                        this.fileList = [
                            {url:res.data.data.url}
                        ]
                    }
                });
            },
            adasd(v) {
                this.contentData = v;
            },
            onSubmit() {
                if(this.flag_){
                    this.proData = ''
                    this.editVisible = false
                    editEnterprisetrendsModuleOne(this.form).then(res => {
                        if(res.code == 0){
                            this.$message.success(`修改成功`);
                        }else{
                            this.$message.error(`修改失败`);
                        }
                    });
                }else{
                    this.proData = ''
                    this.editVisible = false
                    addEnterprisetrendsModuleOne(this.form).then(res => {
                        if(res.code == 0){
                            this.$message.success(`修改成功`);
                            this.$router.go(-1)
                        }else{
                            this.$message.error(`修改失败`);
                        }
                    });
                }

            },
            edit_artcle_del() {
                this.proData = ''
            },
            edit(data) {
                this.editVisible = true
                this.proData = data
            },
            editTitle(data) {
                this.editVisible = false
                this.form.title = data
            },
            editContent(data) {
                this.editVisible = false
                this.form.content = data
            },
        },
        created() {
            bus.$on('editTitle', this.editTitle);
            bus.$on('editContent', this.editContent);
        },
        mounted() {
            this.getData()
        }
    };
</script>
