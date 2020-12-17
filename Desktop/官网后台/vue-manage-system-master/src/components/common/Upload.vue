<template>
    <div class="upload-wrapper">
        <div class="c-box">
            <span class="c-label">上传图片</span>
            <div class="upload-box" @click="handleClick">
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                <input type="file" ref="myFile" hidden @change="handleChange">
            </div>
        </div>
        <div class="c-box" @click="handleClick">
            <span class="c-label">预览区域</span>
            <div class="upload-img-preview">
                <img class="" :src="imgSrc" alt="">
            </div>
        </div>
    </div>
</template>

<script>
    import { uploadImg } from '@/api/upload';
    export default {
        name: 'upload',
        props: {
            fileList: {
                type: Array,
                default: [],
            },
        },
        data() {
            return {
                importHeaders: {Authorization: `Bearer ${localStorage.token}`},
                cSrc: '', // 组件重新上传临时路径
                articleData:{
                    title: "",
                    content: "",
                    seo_title: "",
                    seo_keywords: "",
                    seo_description: "",
                    uploadId: undefined
                }
            };
        },
        computed: {
            imgSrc() {
                if (this.cSrc) {
                    return this.cSrc;
                }
                const fileList = this.fileList;
                return this.fileList[0] ? fileList[0].url : '';
            },
        },
        methods:{
            handleClick() {
                this.$refs.myFile.click();
            },
            async handleChange(e) {
                const files = e.target.files;
                const file = files[0];
                const result = await uploadImg(file);
                if (result.code === 0) {
                    this.$emit('PicID', result.data.id);
                    this.articleData = result.data.id;
                    this.$message.success('图片上传成功');
                    this.cSrc = result.data.url;
                } else {
                    this.$message.error('图片上传失败');
                }
            },
            UploadOK(res) {
                this.$emit('PicID', res.data.id);
                this.articleData = res.data.id
                this.$message.success('图片上传成功')
            },
        },
        mounted(){
            console.log(this.fileList);
        }
    }
</script>

<style scoped>
    .upload-wrapper {
        /*display: flex;*/
        position: relative;
    }
    .upload-box {
        width: 360px;
        height: 180px;
        background-color: #fff;
        border: 1px dashed #ccc;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        cursor: pointer;
    }
    .upload-box em {
        color: #409eff;
    }
    .upload-box .el-icon-upload {
        font-size: 67px;
        color: #C0C4CC;
        margin-bottom: 16px;
        line-height: 50px;
    }
    .c-box {
        display: flex;
        margin-top: 10px;
        flex-direction: row;
        cursor: pointer;
        overflow: hidden;
    }
    .c-box span.c-label {
        display: inline-block;
        font-size: 14px;
        width: 80px;
        text-align: right;
        line-height: 32px;
        padding-right: 12px;
        box-sizing: border-box;
    }
    .c-box .upload-img-preview {
        flex: 1;
    }
    .upload-img-preview img {
        width: 100%;
    }
</style>
