<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 图片集
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-button v-if="id" type="success" style="margin: 10px 0" @click="add_Pic">添加</el-button>
            <el-table
                :data="tableData"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
            >
                <el-table-column type="index" :index="indexMethod" label="序号" align="center"></el-table-column>
                <el-table-column prop="title" label="图片标题">
                    <template slot-scope="scope">
                        <!--                        <div v-html="scope.row.title"></div>-->
                        <div>{{scope.row.title | zenze(scope.row.title) | ellipsis}}</div>
                    </template>
                </el-table-column>
                <el-table-column prop="parent_name" label="所属栏目"></el-table-column>
                <el-table-column prop="alt" label="图片关键词"></el-table-column>
                <el-table-column prop="desc" label="图片描述"></el-table-column>
                <el-table-column label="是否外链">
                    <template slot-scope="scope">
                        {{scope.row.isLink | filterValue(scope.row.isLink)}}
                    </template>
                </el-table-column>
                <el-table-column label="图片" align="center">
                    <template slot-scope="scope">
                        <el-image
                            @click.stop="handleClickItem"
                            class="table-td-thumb"
                            :src="scope.row.url"
                            :preview-src-list="[scope.row.url]"
                        ></el-image>
                    </template>
                </el-table-column>
                <el-table-column prop="path" label="path"></el-table-column>
                <el-table-column prop="width" label="宽度"></el-table-column>
                <el-table-column prop="height" label="高度"></el-table-column>
                <el-table-column prop="created_at" label="创建时间">
                    <template slot-scope="scope">
                        {{ scope.row.created_at | timestampToTime(scope.row.created_at) }}
                    </template>
                </el-table-column>
                <el-table-column prop="updated_at" label="更新时间">
                    <template slot-scope="scope">
                        {{ scope.row.updated_at | timestampToTime(scope.row.updated_at) }}
                    </template>
                </el-table-column>
                <el-table-column prop="url" label="url"></el-table-column>
                <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-edit"
                            @click="handleEdit(scope.$index, scope.row)"
                        >编辑</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                    v-if="total > 20"
                    :hide-on-single-page="total < 20"
                    style="margin-top: 20px"
                    background
                    layout="prev, pager, next"
                    :page-size="20"
                    @current-change="handleCurrentChange"
                    :total="total">
            </el-pagination>
        </div>
    </div>
</template>

<script>
    import { getAllPic, getAllPicByparentId } from '../../api/index';
export default {
    name: 'PicEditing',
    data() {
        return {
            total:undefined,
            currentPage: 1,
            pageSize: 20,
            id:'',
            tableData: [],
            delList: [],
            editVisible: false,
            form: {},

            options: [{
                value: '1',
                label: '是'
            }, {
                value: '0',
                label: '否'
            }],
            value: '',
            fileList: [{name: '', url: ''}],
            formData:{
                id:'',
                alt:'',
                path:'',
                isLink:''
            }
        };

    },
    created() {

    },
    methods: {
        indexMethod(index) {
            index = (index + 1) + (this.currentPage - 1) * this.pageSize
            return index
        },
        handleClickItem(){
            // 获取遮罩层dom
            setTimeout(()=>{
                let domImageMask = document.querySelector(".el-image-viewer__mask");
                if (!domImageMask) {
                    return;
                }
                domImageMask.addEventListener("click", () => {
                    // 点击遮罩层时调用关闭按钮的 click 事件
                    document.querySelector(".el-image-viewer__close").click();
                });
            },0)
        },
        handleCurrentChange(val) {
            this.currentPage = val
            this.getData()
        },
        add_Pic(){
            this.$router.push({
                path:'/EditingPic',
                query:{parent_id:this.id}
            })
        },
        select(value) {
            this.formData.isLink = value
        },
        del() {
            this.editVisible = false
            this.formData = new FormData()
        },
        getData() {
            getAllPic({
                currentPage:this.currentPage,
                pageSize: this.pageSize,
            }).then(res => {
                console.log(res);
                this.tableData = res.data.data;
                this.total = res.data.total
            });
        },
        // 编辑操作
        handleEdit(index, row) {
            const data = {
                id : row.id,
                parent_id : row.parent_id
            }
            this.$router.push({
                path: '/EditingPic',
                query: data
            })
        },
    },
    mounted() {
        const id = this.$route.query.id
        if(id){
            this.id = id
            getAllPicByparentId({id}).then(res => {
                this.tableData = res.data.data;
            });
        }else{
            this.getData();
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
        },
        ellipsis(value) {
            if (!value) return "";
            if (value.length > 80) {
                return value.slice(0, 80) + "...";
            }
            return value;
        },
        zenze(v) {
            return v.replace(/<[^>]*>|<\/[^>]*>/gm, "").replace(/&nbsp;/gm, "");
        }
    },
};
</script>

<style scoped>
.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 300px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.mr10 {
    margin-right: 10px;
}
.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}
</style>
