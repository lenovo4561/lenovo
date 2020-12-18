<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 首页模块二
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <UploadComponent :fileList="fileList" @PicID="PicID"/>
                <el-form ref="form" :model="form" label-width="80px" style="margin-top: 50px">
                    <el-form-item label="文章标题" label-width="100px">
                        <div style="display: flex;justify-content: space-between">
                            <el-input v-html="form.title" disabled></el-input>
                            <el-button style="height: 32px" type="primary" @click="edit('title')">编辑</el-button>
                        </div>
                    </el-form-item>
                    <el-form-item label="文章内容" label-width="100px">
                        <div style="display: flex;justify-content: space-between">
                            <el-input v-html="form.desc" disabled></el-input>
                            <el-button style="height: 32px" type="primary" @click="edit('content')">编辑</el-button>
                        </div>
                    </el-form-item>
                    <el-form-item label="图片关键词" label-width="100px">
                        <el-input v-model="form.alt"></el-input>
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
    import { getModuleTwo,editModuleTwo } from '../../api/index';
    import UploadComponent from '../common/Upload'
    import VueEditorComponent from '../common/VueEditor'
    import bus from '../common/bus';
    export default {
        name: 'HomeModuleTwo',
        components: {
            UploadComponent,
            VueEditorComponent,
        },
        data() {
            return {
                flag_:'',
                fileList:[],
                id:'',
                contentData: '',
                form: {

                },
                proData:'',
                editVisible:false,

            };
        },
        methods: {
            PicID(v) {
                this.form.uploadId = v
            },
            adasd(v) {
                this.contentData = v;
            },
            onSubmit() {
                editModuleTwo(this.form).then(res => {
                    if(res.code == 0){
                        this.$message.success(`修改成功`);
                    }else{
                        this.$message.error(`修改失败`);
                    }
                });
            },
            edit_artcle_del() {
                this.proData = ''
            },
            edit(data) {
                if(data == 'title'){
                    this.contentData = this.form.title;
                }else{
                    this.contentData = this.form.desc;
                }
                this.editVisible = true
                this.proData = data
            },
            editTitle(data) {
                this.editVisible = false
                this.form.title = data
            },
            editContent(data) {
                this.editVisible = false
                this.form.desc = data
            },
            getData() {
                getModuleTwo().then(res => {
                    if(res.code == 0){
                        this.flag_ = true
                        this.form = res.data.data
                        this.fileList = [
                            {url:res.data.data.url}
                        ]
                    }
                });
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
