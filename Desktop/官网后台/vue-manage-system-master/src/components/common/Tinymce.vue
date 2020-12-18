<template>
    <div class="tinymce-editor">
        <editor v-model="myValue" :init="init" :disabled="disabled" @onClick="onClick"></editor>
    </div>
</template>
<script>
    import tinymce from "tinymce/tinymce";
    import Editor from "@tinymce/tinymce-vue";
    import "tinymce/themes/silver";
    // 编辑器插件plugins
    // 更多插件参考：https://www.tiny.cloud/docs/plugins/
    import "tinymce/plugins/lists";
    import "tinymce/plugins/image"; // 插入上传图片插件
    import "tinymce/plugins/imagetools";
    import "tinymce/plugins/table"; // 插入表格插件
    import "tinymce/plugins/lists"; // 列表插件
    import "tinymce/plugins/emoticons"; //表情插件
    import "tinymce/plugins/link"; //插入链接
    import "tinymce/plugins/fullscreen";
    import "tinymce/plugins/anchor";
    // import "tinymce/plugins/autosave"
    import "tinymce/plugins/autoresize"; //内容自适应插件
    import {getUrl2} from '../utils/request.js'
    export default {
        components: {
            Editor
        },
        props: {
            value: {
                type: String,
                default: ""
            },
            // 基本路径，默认为空根目录，如果你的项目发布后的地址为目录形式，
            // 即abc.com/tinymce，baseUrl需要配置成tinymce，不然发布后资源会找不到
            baseUrl: {
                type: String,
                default: ""
            },
            disabled: {
                type: Boolean,
                default: false
            },
            plugins: {
                type: [String, Array],
                default:
                    "lists  image imagetools   link  fullscreen anchor autoresize"
            },
            toolbar: {
                type: [String, Array],
                default:
                    "bold italic forecolor  backcolor | styleselect|  bullist numlist  | lists image link   | removeformat|fullscreen"
            }
        },
        data() {
            return {
                init: {
                    language_url: "/tinymce/langs/zh_CN.js",
                    language: "zh_CN",
                    skin_url: "/tinymce/skins/ui/oxide",
                    emoticons_database_url: "/tinymce/emoticons/js/emojis.js",
                    content_css: "/tinymce/skins/content/default/content.min.css",
                    // skin_url: `${this.baseUrl}/tinymce/skins/ui/oxide-dark`, // 暗色系
                    // content_css: `${this.baseUrl}/tinymce/skins/content/dark/content.css`, // 暗色系
                    statusbar: false, // 隐藏编辑器底部的状态栏
                    selector: "textarea", // change this value according to your HTML
                    plugins: this.plugins,
                    min_height: 240,
                    toolbar: this.toolbar,
                    branding: false,
                    menubar: false,
                    // 此处为图片上传处理函数，这个直接用了base64的图片形式上传图片，
                    // 如需ajax上传可参考https://www.tiny.cloud/docs/configure/file-image-upload/#images_upload_handler
                    images_upload_handler: (blobInfo, success, failure) => {
                        //const img = "data:image/jpeg;base64," + blobInfo.base64();
                        // success(img);
                        var xhr, formData;
                        xhr = new XMLHttpRequest();
                        xhr.withCredentials = false;
                        xhr.open("POST", `${getUrl2()}/comment/uploadFtp`);
                        xhr.setRequestHeader("Authorization",localStorage.getItem("Authorization"));  //设置请求头
                        xhr.onload = function() {
                            var json;
                            if (xhr.status != 200) {
                                failure("HTTP Error: " + xhr.status);
                                return;
                            }
                            json = JSON.parse(xhr.responseText);
                            if (!json || typeof json.object!= "string") {
                                failure("Invalid JSON: " + xhr.responseText);
                                return;
                            }
                            success(json.object);
                        };
                        formData = new FormData();
                        formData.append("file", blobInfo.blob(), blobInfo.filename());
                        xhr.send(formData);
                    }
                },
                myValue: this.value
            };
        },
        mounted() {
            tinymce.init({});
        },
        methods: {
            // 添加相关的事件，可用的事件参照文档=> https://github.com/tinymce/tinymce-vue => All available events
            // 需要什么事件可以自己增加
            onClick(e) {
                this.$emit("onClick", e, tinymce);
            },
            // 可以添加一些自己的自定义事件，如清空内容
            clear() {
                this.myValue = "";
            },
            onChage(e) {},
            async uploadImg(FormData) {
                let res = await this.$api2.upload_img(FormData);
            }
        },
        watch: {
            value(newValue) {
                this.myValue = newValue;
            },
            myValue(newValue) {
                this.$emit("input", newValue);
            }
        }
    };
</script>
