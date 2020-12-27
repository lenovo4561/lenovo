<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 联系我们
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <el-form ref="form" :model="form" label-width="80px" style="margin-top: 50px">
                    <el-form-item label="标题" >
                        <div style="display: flex;justify-content: space-between">
                            <el-input v-html="form.title" disabled></el-input>
                            <el-button style="height: 32px" type="primary" @click="edit('title')">编辑</el-button>
                        </div>
                    </el-form-item>
                    <el-form-item label="描述">
                        <div style="display: flex;justify-content: space-between">
                            <el-input v-html="form.desc" disabled></el-input>
                            <el-button style="height: 32px" type="primary" @click="edit('desc')">编辑</el-button>
                        </div>
                    </el-form-item>
                    <el-form-item label="纬度">
                        <el-input v-model="form.lat"></el-input>
                    </el-form-item>
                    <el-form-item label="经度">
                        <el-input v-model="form.lon"></el-input>
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
import { editArticleByparentId,editcontactus,addArticleByparentId,getcontactus } from '../../api/index';
import UploadComponent from '../common/Upload'
import VueEditorComponent2 from '../common/VueEditor2'
import bus from '../common/bus';
export default {
    name: 'ContactUs',
    components: {
        UploadComponent,
        VueEditorComponent2
    },
    data() {
        return {
            flag_:'',
            id:'',
            contentData: '',
            form: {

            },
            proData:'',
            editVisible:false,

        };
    },
    methods: {
        adasd(val) {
            if (this.formAttr.indexOf('.') !== -1) {
                const splitArr = this.formAttr.split('.');
                this.form[splitArr[0]][splitArr[1]][splitArr[2]] = val;
            } else {
                this.form[this.formAttr] = val;
            }
            this.editVisible = false
        },
        PicID(v) {
            this.form.uploadId = v
        },
        onSubmit() {
            const lon = Number(this.form.lon)
            const lat = Number(this.form.lat)
            this.form.lon = lon
            this.form.lat = lat
            editcontactus(this.form).then(res => {
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
            this.form.desc = data
        },
        getData() {
            getcontactus().then(res => {
                if(res.code == 0){
                    this.form = res.data.data
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
