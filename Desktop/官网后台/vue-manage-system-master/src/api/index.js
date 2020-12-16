import request from '../utils/request';

export const Login = query => {
    return request({
        url: '/users',
        method: 'get',
        params: query
    });
};

export const getData = query => {
    return request({
        url: '/bannerone',
        method: 'get',
        params: query
    });
};

export const editData = query => {
    return request({
        url: `/bannerone/${query.id}`,
        method: 'put',
        data: query
    });
};

export const addColumn = query => {
    return request({
        url: `/module`,
        method: 'post',
        data: query
    });
};

export const getColumn = query => {
    return request({
        url: `/module`,
        method: 'get',
    });
};

export const editColumn = query => {
    return request({
        url: `/module/${query.uploadId}`,
        method: 'put',
        data: query
    });
};

export const addChildrenColumn = query => {  //添加子分类
    return request({
        url: `/module/class`,
        method: 'post',
        data: query
    });
};

export const getAllColumn = query => {  //获取所有分类子分类
    return request({
        url: `/module/class`,
        method: 'get'
    });
};

export const getAllArticle = query => {  //获取所有文章
    return request({
        url: `/articletype`,
        method: 'get'
    });
};

export const getAllArticleByparentId = query => {  //根据子栏目id获取文章集
    return request({
        url: `/module/class/${query.id}/article?id=${query.id}`,
        method: 'get',
    });
};

export const getArticleById = query => {  //获取一篇文章集
    return request({
        url: `/articletype/${query.id}`,
        method: 'get',
    });
};

export const getPicById = query => {  //获取一个图片集
    return request({
        url: `/imgtype/${query.id}`,
        method: 'get',
    });
};

export const addPicById = query => {  //添加一个图片集
    return request({
        url: `/imgtype?moduleId=${query.moduleId}`,
        method: 'post',
        data: query
    });
};

export const editPicById = query => {  //修改一个图片集
    return request({
        url: `/imgtype/${query.id}`,
        method: 'put',
        data: query
    });
};


export const addArticleByparentId = query => {  //添加文章
    return request({
        url: `/articletype?moduleId=${query.moduleId}`,
        method: 'post',
        data: query
    });
};

export const editArticleByparentId = query => {  //修改文章
    return request({
        url: `/articletype/${query.id}`,
        method: 'put',
        data: query
    });
};

export const getAllPicByparentId = query => {  //根据子栏目id获取图片集
    return request({
        url: `/module/class/${query.id}/img?id=${query.id}`,
        method: 'get',
    });
};

export const editChildren = query => {  //编辑子类
    return request({
        url: `/module/class/${query.id}`,
        method: 'put',
        data: query
    });
};

export const getAllPic = query => {  //获取所有图片
    return request({
        url: `/imgtype`,
        method: 'get'
    });
};

export const addColumnSEO = query => {  //添加栏目SEO信息
    return request({
        url: `/moduleseo?moduleId=${query.moduleId}`,
        method: 'post',
        data: query
    });
};

export const EditColumnSEO = query => {  //修改栏目SEO信息
    return request({
        url: `/moduleseo/${query.moduleId}`,
        method: 'put',
        data: query
    });
};

export const getSEOMsg = query => {  //获取SEO信息
    return request({
        url: `/moduleseo/${query.id}`,
        method: 'get',
        params: query
    });
};

export const getModuleOne = query => {  //首页模块一
    return request({
        url: `/home/module1`,
        method: 'get'
    });
};

export const addModuleOne = query => {  //添加首页模块一
    return request({
        url: `/home/module1`,
        method: 'post',
        data: query
    });
};

export const editModuleOne = query => {  //修改首页模块一
    return request({
        url: `/home/module1/${query.id}`,
        method: 'put',
        data: query
    });
};

export const getModuleOneById = query => {  //首页模块一查询
    return request({
        url: `/home/module1/${query.id}`,
        method: 'get'
    });
};

export const getModuleTwo = query => {  //首页模块二获取
    return request({
        url: `/home/module2`,
        method: 'get'
    });
};

export const editModuleTwo = query => {  //首页模块二获取
    return request({
        url: `/home/module2`,
        method: 'put',
        data: query
    });
};


export const getAboutModuleOne = query => {  //关于模块一获取
    return request({
        url: `/about/module1`,
        method: 'get'
    });
};

export const editAboutModuleOne = query => {  //关于模块一修改
    return request({
        url: `/about/module1`,
        method: 'put',
        data: query
    });
};

export const getAboutModuleTwo = query => {  //关于模块二获取
    return request({
        url: `/about/module2`,
        method: 'get'
    });
};


export const editAboutModuleTwo = query => {  //关于模块二修改
    return request({
        url: `/about/module2`,
        method: 'put',
        data: query
    });
};

export const getMessageBoard = query => {  //获取留言列表
    return request({
        url: `/messageboard`,
        method: 'get'
    });
};


export const getcontactus = query => {  //获取联系我们
    return request({
        url: `/contactus/module2`,
        method: 'get'
    });
};

export const editcontactus = query => {  //修改联系我们
    return request({
        url: `/contactus/module2`,
        method: 'put',
        data:query
    });
};
export const getProductModuleOne = query => {  //产品分类模块
    return request({
        url: `/product/module1`,
        method: 'get'
    });
};

export const editProductModuleOne = query => {  //修改产品分类模块
    return request({
        url: `/product/module1`,
        method: 'put',
        data:query
    });
};

export const addProductModuleOne = query => {  //添加产品分类模块
    return request({
        url: `/product/module1`,
        method: 'post',
        data:query
    });
};


export const getStyleModuleOne = query => {  //风格展示模块
    return request({
        url: `/style/module1`,
        method: 'get'
    });
};

export const editStyleModuleOne = query => {  //风格展示模块
    return request({
        url: `/style/module1`,
        method: 'put',
        data:query
    });
};

export const addStyleModuleOne = query => {  //风格展示模块
    return request({
        url: `/style/module1`,
        method: 'post',
        data:query
    });
};

export const getEnterprisetrendsModuleOne = query => {  //企业动态模块
    return request({
        url: `/enterprisetrends/module1`,
        method: 'get'
    });
};

export const editEnterprisetrendsModuleOne = query => {  //企业动态模块
    return request({
        url: `/enterprisetrends/module1`,
        method: 'put',
        data:query
    });
};

export const addEnterprisetrendsModuleOne = query => {  //企业动态模块
    return request({
        url: `/enterprisetrends/module1`,
        method: 'post',
        data:query
    });
};

