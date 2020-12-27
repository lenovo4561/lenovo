<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 轮播图配置
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-button type="success" style="margin: 10px 0" @click="add_column">添加</el-button>
            <el-table
                    :data="tableData"
                    border
                    row-key="id"
                    class="table"
                    ref="multipleTable"
                    header-cell-class-name="table-header"
                    :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
            >
                <el-table-column type="index" label="序号" width="55" align="center"></el-table-column>
                <el-table-column align="center" prop="alt" label="描述"></el-table-column>
                <el-table-column align="center" prop="path" label="path"></el-table-column>
                <el-table-column prop="sort" label="排序" width="100" align="center">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.sort"></el-input>
                    </template>
                </el-table-column>
                <el-table-column label="是否外链" align="center">
                    <template slot-scope="scope">{{scope.row.is_link | filterValue(scope.row.is_link)}}</template>
                </el-table-column>
                <el-table-column label="banner图" align="center" width="155">
                    <template slot-scope="scope">
                        <el-image
                                @click.stop="handleClickItem"
                                class="table-td-thumb"
                                :src="scope.row.url"
                                :preview-src-list="[scope.row.url]"
                        ></el-image>
                    </template>
                </el-table-column>
                <el-table-column align="center" prop="is_checked" label="开启状态">
                    <template slot-scope="scope">
                        <el-switch :active-value="1" :inactive-value="0" v-model="scope.row.is_show" @change='changeStatus($event,scope.row,scope.$index)' active-color="#13ce66"></el-switch>
                    </template>
                </el-table-column>
                <el-table-column align="center" prop="created_at" label="创建时间">
                    <template slot-scope="scope">
                        {{ scope.row.created_at | timestampToTime(scope.row.created_at) }}
                    </template>
                </el-table-column>
                <el-table-column align="center" prop="updated_at" label="更新时间">
                    <template slot-scope="scope">
                        {{ scope.row.updated_at | timestampToTime(scope.row.updated_at) }}
                    </template>
                </el-table-column>
                <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <el-button
                                v-if="scope.row.path"
                                type="warning"
                                @click="Edit(scope.row)"
                        >编辑</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-button
                    style="margin-top: 20px"
                    type="success"
                    @click="UpdateSort"
            >更新排序</el-button>
        </div>
    </div>
</template>

<script>
    import { getJoinUsModuleTwo, addModuleOne, editJoinModuleTwo, JoinUsBannerSort } from '../../api/index';
    export default {
        name: 'JoinUsModuleTwo',
        data() {
            return {
                tableData: [],
                data:{}
            };

        },
        created() {

        },
        methods: {
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
            UpdateSort(){
                const list = []
                this.tableData.forEach((item)=>{
                    const Data = {
                        id:item.id,
                        sort:item.sort
                    }
                    list.push(Data)
                })
                JoinUsBannerSort({list}).then(res => {
                    if(res.code == 0) {
                        this.$message.success(`更新成功`);
                    }else{
                        this.$message.error(`更新失败`);
                    }
                })
            },
            changeStatus($event,data,index) {
                this.data = {
                    id:Number(data.id),
                    is_show: $event == true ? 1 : 0
                }
                editJoinModuleTwo(this.data).then(res => {
                    if(res.code == 0){
                        this.$message.success(`修改成功`);
                    }
                });

            },
            getData() {
                getJoinUsModuleTwo().then(res => {
                    this.tableData = res.data.data;
                });
            },
            Edit(data){
                const id = data.id
                this.$router.push({
                    path: '/EditingJoinUsModule',
                    query:{id}
                })
            },
            add_column(){
                this.$router.push({
                    path: '/EditingJoinUsModule'
                })
            }
        },
        mounted() {
            this.getData()
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
