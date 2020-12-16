<template>
    <div>
        <div class="container">
            <div class="plugins-tips" style="text-align: center">
                编辑内容
            </div>
            <quill-editor ref="myTextEditor" v-model="computedContent" :options="editorOption"></quill-editor>
            <el-button class="editor-btn" style="width: 100%;text-align: center" type="primary" @click="submit">提交</el-button>
        </div>
    </div>
</template>

<script>
    import bus from '../common/bus';
    import 'quill/dist/quill.core.css';
    import 'quill/dist/quill.snow.css';
    import 'quill/dist/quill.bubble.css';
    import { quillEditor } from 'vue-quill-editor';
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
                }
            }
        },
        computed: {
          computedContent: {
              get () {
                  return this.content
              },
              set (newVal) {
                this.$emit('aaa', newVal);
              },
          },
        },
        components: {
            quillEditor
        },
        methods: {
            onEditorChange({ editor, html, text }) {
                this.content = html;
            },
            submit(){
                if(this.proData == 'title'){
                    bus.$emit('editTitle',this.content);
                }else if(this.proData == 'content'){
                    bus.$emit('editContent',this.content);
                }else if(this.proData == 'name'){
                    bus.$emit('editName',{
                        content:this.content,
                        index:this.index_
                    });
                }else if(this.proData == 'value'){
                    bus.$emit('editValue',{
                        content:this.content,
                        index:this.index_
                    });
                }
            }
        }
    }
</script>
<style scoped>
    .editor-btn{
        margin-top: 20px;
    }
</style>
