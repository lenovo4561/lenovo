<template>
    <div>
        <div class="container" style="margin-bottom: 50px">
            <el-upload
                    :headers="importHeaders"
                    :on-success='UploadOK'
                    :on-error='UploadError'
                    :limit='1'
                    class="upload-demo"
                    action="/upload"
                    :on-preview="handlePreview"
                    :on-remove="handleRemove"
                    :file-list="fileList"
                    list-type="picture">
                <el-button size="small" type="primary">上传图片</el-button>
<!--                <div slot="tip" class="el-upload__tip">jpg/png files with a size less than 500kb</div>-->
            </el-upload>
        </div>
    </div>
</template>

<script>
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
            // fileList: [{name: '', url: ''}],
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
    methods:{
        UploadOK(res) {
            this.$emit('PicID', res.data.id);
            this.articleData = res.data.id
            this.$message.success('图片上传成功')
        },
        UploadError() {
            this.$message.error('图片上传失败')
        },
        handleRemove(file, fileList) {
            // console.log(file, fileList);
        },
        handlePreview(file) {
            // console.log(file);
        }
    },
    created(){

    }
}
</script>

<style scoped>

</style>
