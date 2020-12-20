<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 模块编辑
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <p style="font-size:12px;line-height:30px;color:red;">Tips : 建议图片大小: 1920px * 900px</p>
                <UploadComponent :fileList="fileList" @PicID="PicID"/>
                <el-form ref="form" :model="form" label-width="100px" style="margin-top: 50px">
                    <el-form-item label="关键词描述" label-width="100px">
                        <el-input v-model="form.alt"></el-input>
                    </el-form-item>
                    <el-form-item label="图片路径" label-width="100px">
                        <el-input v-model="form.path"></el-input>
                    </el-form-item>
                    <el-form-item label="是否外链" label-width="100px">
                        <el-select v-model="value" @change="select" placeholder="请选择">
                            <el-option
                                    v-for="item in options"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
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
import { editArticleByparentId, getArticleById, getModuleOneById,addModuleOne,editModuleOne } from '../../api/index';
import UploadComponent from '../common/Upload'
import VueEditorComponent2 from '../common/VueEditor2'
import bus from '../common/bus';
export default {
    name: 'EditingModuleOne',
    components: {
        UploadComponent,
        VueEditorComponent2
    },
    data() {
        return {
            value:'',
            options: [{
                value: '1',
                label: '是'
            }, {
                value: '0',
                label: '否'
            }],
            flag_:'',
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
            getModuleOneById({id:this.form.id}).then(res => {
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
                editModuleOne(this.form).then(res => {
                    if(res.code == 0){
                        this.$message.success(`修改成功`);
                    }else{
                        this.$message.error(`修改失败`);
                    }
                });
            }else{
                this.proData = ''
                this.editVisible = false
                addModuleOne(this.form).then(res => {
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
        this.form.id = Number(this.$route.query.id)
        if(this.form.id){
            this.getData()
        }
    }
};
</script>
