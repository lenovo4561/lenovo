<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 文章编辑
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <p style="font-size:12px;line-height:30px;color:red;">Tips : 建议图片大小: 225px * 130px</p>
                <UploadComponent :fileList="fileList" @PicID="PicID"/>
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
import { editArticleByparentId,getArticleById,addArticleByparentId } from '../../api/index';
import UploadComponent from '../common/Upload'
import VueEditorComponent2 from '../common/VueEditor2'
import bus from '../common/bus';
export default {
    name: 'EditingAticle',
    components: {
        UploadComponent,
        VueEditorComponent2,
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
            formAttr: '',
        };
    },
    methods: {
        PicID(v) {
            this.form.uploadId = v
        },
        adasd(val) {
            if (this.formAttr.indexOf('.') !== -1) {
                const splitArr = this.formAttr.split('.');
                this.form[splitArr[0]][splitArr[1]][splitArr[2]] = val;
            } else {
                this.form[this.formAttr] = val;
            }
            this.editVisible = false
            // this.contentData = info;
        },
        onSubmit() {
            if(this.flag_){
                this.proData = ''
                this.editVisible = false
                const form = {
                    ...this.form,
                    id:this.id
                }
                editArticleByparentId(form).then(res => {
                    if(res.code == 0){
                        this.$message.success(`修改成功`);
                        this.getData()
                    }else{
                        this.$message.error(`修改失败`);
                    }
                });
            }else{
                this.proData = ''
                this.editVisible = false
                const form = {
                    ...this.form,
                    id:this.id
                }
                addArticleByparentId(form).then(res => {
                    if(res.code == 0){
                        this.$message.success(`添加成功`);
                        this.$router.go(-1)
                    }else{
                        this.$message.error(`添加失败`);
                    }
                });
            }
        },
        edit_artcle_del() {
            this.proData = ''
        },
        edit(data) {
            let splitArr;
            if (data.indexOf('.') !== -1) {
                splitArr = data.split('.');
                this.contentData = this.form[splitArr[0]][splitArr[1]][splitArr[2]];
            } else {
                this.contentData = this.form[data];
            }
            console.log(splitArr);
            this.formAttr = data;
            this.proData = data
            this.editVisible = true
        },
        editTitle(data) {
            this.editVisible = false
            this.form.title = data
        },
        editContent(data) {
            this.editVisible = false
            this.form.content = data
        },
        getData() {
            getArticleById({id:this.id}).then(res => {
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
        if(this.$route.query){
            this.id = Number(this.$route.query.id)
            this.form.moduleId = Number(this.$route.query.parent_id)
        }
        if(this.id){
            this.getData()
        }
    }
};
</script>
