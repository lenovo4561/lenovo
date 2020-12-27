<template>
    <div>
        <div class="container">
            <div class="plugins-tips" style="text-align: center">
                编辑内容
            </div>
            <TinymceComponent ref="myTinymce" v-model="innerContent" :height="300"></TinymceComponent>
            <el-button class="editor-btn" style="width: 100%;text-align: center" type="primary" @click="submit">提交</el-button>
        </div>
    </div>
</template>

<script>
    import bus from '../common/bus';
    import TinymceComponent from '../common/Tinymce/index'
    export default {
        name: 'editor',
        props:{
            index_:{
                type: String | Number,
                default: '',
            },
            proData: {
                type: String,
                default: '',
            },
            content: {
                type: String,
                default: '',
            },
        },
        data: function(){
            return {
                editorOption: {
                    placeholder: 'Hello World'
                },
                innerContent: this.content,
                currentValue: '',
            }
        },
        watch: {
            content(val) {
                this.$refs.myTinymce.setHashchange(false);
                this.innerContent = val
            },
            innerContent(val) {
                this.currentValue = val;
            },
        },

        computed: {
          computedContent: {
              get () {
                  return this.content
              },
              set (newVal) {
                  this.currentValue = newVal;
                // this.$emit('aaa', newVal);
              },
          },
        },
        components: {
            TinymceComponent
        },
        methods: {
            onEditorChange({ editor, html, text }) {
                this.content = html;
            },
            submit(){
                this.$emit('aaa', this.currentValue);
                // if(this.proData == 'title'){
                //     bus.$emit('editTitle',this.content);
                // }else if(this.proData == 'content'){
                //     bus.$emit('editContent',this.content);
                // }else if(this.proData == 'name'){
                //     bus.$emit('editName',{
                //         content:this.content,
                //         index:this.index_
                //     });
                // }else if(this.proData == 'value'){
                //     bus.$emit('editValue',{
                //         content:this.content,
                //         index:this.index_
                //     });
                // }
                // if(this.proData == 'name'){
                //     bus.$emit('editName',{
                //         content:this.content,
                //         index:this.index_
                //     });
                // }else if(this.proData == 'value'){
                //     bus.$emit('editValue',{
                //         content:this.content,
                //         index:this.index_
                //     });
                // }
            }
        },
    }
</script>
<style scoped>
    .editor-btn{
        margin-top: 20px;
    }
</style>
