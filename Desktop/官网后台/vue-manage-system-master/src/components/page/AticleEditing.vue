<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 文章集
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-button v-if="id" type="success" style="margin: 10px 0" @click="add_article">添加</el-button>
            <el-table
                :data="tableData"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
            >
                <el-table-column type="index" label="序号" width="55" align="center"></el-table-column>
                <el-table-column prop="title" align="center" label="文章标题">
                    <template slot-scope="scope">
<!--                        <div v-html="scope.row.title"></div>-->
                        <div>{{scope.row.title | zenze(scope.row.title) | ellipsis}}</div>
                    </template>
                </el-table-column>
                <el-table-column prop="content" align="center" label="文章内容" width="455">
                    <template slot-scope="scope">
<!--                        <div v-html="scope.row.content"></div>-->
                        <div>{{scope.row.content | zenze(scope.row.content) | ellipsis}}</div>
                    </template>
                </el-table-column>
                <el-table-column prop="parent_name" align="center" label="所属栏目"></el-table-column>
                <el-table-column prop="seo_title" label="SEO标题"></el-table-column>
                <el-table-column prop="seo_keywords" label="SEO关键词"></el-table-column>
                <el-table-column prop="seo_description" label="SEO描述"></el-table-column>
                <el-table-column label="缩略图" align="center" width="155">
                    <template slot-scope="scope">
                        <el-image
                            class="table-td-thumb"
                            :src="scope.row.url"
                            :preview-src-list="[scope.row.url]"
                        ></el-image>
                    </template>
                </el-table-column>
                <el-table-column prop="created_at" align="center" label="创建时间">
                    <template slot-scope="scope">
                        {{ scope.row.created_at | timestampToTime(scope.row.created_at) }}
                    </template>
                </el-table-column>
                <el-table-column prop="updated_at" align="center" label="更新时间">
                    <template slot-scope="scope">
                        {{ scope.row.updated_at | timestampToTime(scope.row.updated_at) }}
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-edit"
                            @click="handleEdit(scope.$index, scope.row)"
                        >编辑</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <el-pagination
                :hide-on-single-page="total <= 20"
                style="margin-top: 20px"
                background
                layout="prev, pager, next"
                :page-size="20"
                @current-change="handleCurrentChange"
                :total="total">
        </el-pagination>
    </div>
</template>

<script>
import { getAllArticle,getAllArticleByparentId } from '../../api/index';
export default {
    name: 'AticleEditing',
    data() {
        return {
            total: undefined,
            currentPage: 1,
            pageSize: 20,
            id:'',
            tableData: [],
            editVisible: false,
            value: '',
        };

    },
    created() {

    },
    methods: {
        handleCurrentChange(val) {
            this.currentPage = val
            this.getData()
        },
        add_article(){
          this.$router.push({
              path:'/EditingArticle',
              query:{parent_id:this.id}
          })
        },
        del() {
            this.editVisible = false
        },
        getData() {
            getAllArticle({
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
                path: '/EditingArticle',
                query: data
            })
        },
    },
    mounted() {
        const id = this.$route.query.id
        if(id){
            this.id = id
            getAllArticleByparentId({id}).then(res => {
                console.log(res);
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
            return v.replace(/<[^>]*>|<\/[^>]*>/gm, "");
        }
    },
};
</script>

<style scoped>
.el-tooltip__popper{
    max-width: 400px
}
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
