<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 模块编辑二
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <UploadComponent />
                <el-form ref="form" :model="form" label-width="80px" style="margin-top: 50px">
                    <el-form-item label="文章标题" >
                        <div style="display: flex;justify-content: space-between">
                            <el-input v-html="form.title" disabled></el-input>
                            <el-button style="height: 32px" type="primary" @click="edit('title')">编辑</el-button>
                        </div>
                    </el-form-item>
                    <el-form-item label="文章内容">
                        <div style="display: flex;justify-content: space-between">
                            <el-input v-html="form.content" disabled></el-input>
                            <el-button style="height: 32px" type="primary" @click="edit('content')">编辑</el-button>
                        </div>
                    </el-form-item>
                    <el-form-item label="seo标题">
                        <el-input v-model="form.seo_title"></el-input>
                    </el-form-item>
                    <el-form-item label="seo关键词">
                        <el-input v-model="form.seo_keywords"></el-input>
                    </el-form-item>
                    <el-form-item label="seo描述">
                        <el-input type="textarea" rows="5" v-model="form.seo_description"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit">表单提交</el-button>
                        <el-button>取消</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="35%" @close='edit_artcle_del'>
            <VueEditorComponent2 :proData="proData" :content="contentData" @aaa="adasd" />
        </el-dialog>
    </div>
</template>

<script>
import { editArticleByparentId } from '../../api/index';
import UploadComponent from '../common/Upload'
import VueEditorComponent2 from '../common/VueEditor2'
import bus from '../common/bus';
export default {
    name: 'EditingModuleTwo',
    components: {
        UploadComponent,
        VueEditorComponent2
    },
    data() {
        return {
            contentData: '',
            form: {
                title: '',
                content: '',
                seo_title: '',
                seo_keywords: '',
                seo_description: '',
                uploadId: undefined
            },
            proData:'',
            editVisible:false,

        };
    },
    methods: {
        adasd(v) {
            this.contentData = v;
        },
        onSubmit() {
            this.proData = ''
            this.editVisible = false
            editArticleByparentId(this.form).then(res => {
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
        this.form.uploadId = Number(this.$route.query.id)
    }
};
</script>
