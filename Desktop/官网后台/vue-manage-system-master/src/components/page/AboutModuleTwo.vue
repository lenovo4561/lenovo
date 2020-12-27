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
                <el-form ref="form" :model="form" label-width="80px" style="margin-top: 50px">
                    <el-form-item label="文章标题" >
                        <div style="display: flex;justify-content: space-between">
                            <el-input v-html="form.title" disabled></el-input>
                            <el-button style="height: 32px" type="primary" @click="edit('title')">编辑</el-button>
                        </div>
                    </el-form-item>
                    <el-form-item label="文章内容">
                        <div style="display: flex;justify-content: space-between">
                            <el-input v-html="form.desc" disabled></el-input>
                            <el-button style="height: 32px" type="primary" @click="edit('desc')">编辑</el-button>
                        </div>
                    </el-form-item>
                    <template v-for='(item, index) in form.items'>
                        <el-form-item label="items">
                            <div style="display: flex;justify-content: space-between">
                                <el-input v-html="item.name" disabled></el-input>
                                <el-button style="height: 32px" type="primary" @click="edit(`items.${index}.name`, 1)">编辑</el-button>
                            </div>
                            <br>
                            <div style="display: flex;justify-content: space-between">
                                <el-input v-html="item.value" disabled></el-input>
                                <el-button style="height: 32px" type="primary" @click="edit(`items.${index}.value`)">编辑</el-button>
                            </div>
                        </el-form-item>
                    </template>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit">表单提交</el-button>
                        <el-button>取消</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="35%" @close='edit_artcle_del'>
            <VueEditorComponent2 :proData="proData" :content="contentData" :index_='index_' @aaa="adasd" />
        </el-dialog>
    </div>
</template>

<script>
    import { editAboutModuleOne,getAboutModuleTwo,editAboutModuleTwo } from '../../api/index';
    import VueEditorComponent2 from '../common/VueEditor2'
    import bus from '../common/bus';
    export default {
        name: 'AboutModuleOne',
        components: {
            VueEditorComponent2,
        },
        data() {
            return {
                index_:'',
                value:'',
                fileList: [],
                contentData: '',
                form: {},
                proData:'',
                editVisible:false,
                formAttr: '',
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
                // this.contentData = info;
            },
            changeValue(a,b) {
                this.form.items[b].value = a
            },
            changeName(a,b){
                this.form.items[b].name = a
            },
            getData() {
                getAboutModuleTwo().then(res => {
                    if(res.code == 0){
                        this.form = res.data.data
                    }
                });
            },
            onSubmit() {
                editAboutModuleTwo(this.form).then(res => {
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
                // if(data == 'title'){
                //     this.contentData = this.form.title;
                // }else if(data == 'content'){
                //     this.contentData = this.form.desc;
                // }else if(data == 'name'){
                //     this.contentData = this.form.items[index].name;
                //     this.index_ = index
                // }else if(data == 'value'){
                //     this.index_ = index
                //     this.contentData = this.form.items[index].value;
                // }
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
            editName(data) {
                const index = String(data.index)
                const content = data.content
                this.editVisible = false
                this.form.items[index].name = content
            },
            editValue(data) {
                const index = String(data.index)
                const content = data.content
                this.editVisible = false
                this.form.items[index].value = content
            }
        },
        created() {
            bus.$on('editTitle', this.editTitle);
            bus.$on('editContent', this.editContent);
            bus.$on('editName', this.editName);
            bus.$on('editValue', this.editValue);
        },
        mounted() {
            this.getData()
        }
    };
</script>
