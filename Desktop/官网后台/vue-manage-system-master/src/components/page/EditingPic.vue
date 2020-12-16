<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 图片编辑
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <UploadComponent :fileList="fileList" @PicID="PicID"/>
                <el-form ref="form" :model="form" label-width="80px" style="margin-top: 50px">
                    <el-form-item label="图片标题" >
                        <div style="display: flex;justify-content: space-between">
                            <el-input v-html="form.title" disabled></el-input>
                            <el-button style="height: 32px" type="primary" @click="edit('title')">编辑</el-button>
                        </div>
                    </el-form-item>
                    <el-form-item label="图片desc">
                        <el-input v-model="form.desc"></el-input>
                    </el-form-item>
                    <el-form-item label="图片alt">
                        <el-input v-model="form.alt"></el-input>
                    </el-form-item>
                    <el-form-item label="图片宽度">
                        <el-input v-model="form.width"></el-input>
                    </el-form-item>
                    <el-form-item label="图片高度">
                        <el-input v-model="form.height"></el-input>
                    </el-form-item>
                    <el-form-item label="图片path">
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
import { editArticleByparentId, editPicById, getPicById,addPicById } from '../../api/index';
import UploadComponent from '../common/Upload'
import VueEditorComponent from '../common/VueEditor'
import bus from '../common/bus';
export default {
    name: 'EditingPic',
    components: {
        UploadComponent,
        VueEditorComponent
    },
    data() {
        return {
            flag_:'',
            value:'',
            contentData: '',
            fileList:[],
            form: {
                alt: "",
                desc: "",
                height: "",
                is_link: null,
                path: "",
                status: 0,
                title: "",
                url: "",
                width: "",
                uploadId: undefined
            },
            proData:'',
            editVisible:false,
            options: [{
                value: '1',
                label: '是'
            }, {
                value: '0',
                label: '否'
            }],
        };
    },
    methods: {
        PicID(v) {
            this.form.uploadId = v
        },
        select(value){
            this.form.is_link = value
        },
        adasd(v) {
            this.contentData = v;
        },
        onSubmit() {
            if(this.flag_){
                this.proData = ''
                this.editVisible = false
                const form = {
                    ...this.form,
                    id:this.id
                }
                editPicById(form).then(res => {
                    if(res.code == 0){
                        this.$message.success(`修改成功`);
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
                addPicById(form).then(res => {
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
        getData() {
            getPicById({ id: this.id }).then(res => {
                if (res.code == 0) {
                    this.flag_ = true
                    this.form = res.data.data
                    this.value = res.data.data.is_link == 0 ? '否':'是'
                    this.fileList = [
                        {url:res.data.data.url}
                    ]
                }
            });
        }
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
