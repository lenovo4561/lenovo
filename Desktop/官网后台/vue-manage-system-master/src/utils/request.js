import axios from 'axios';
import { MessageBox, Message } from 'element-ui'
import router from '../router/index'
let baseURL = 'http://192.168.124.6:8989/';
if (process.env.NODE_ENV === 'production') {
    baseURL = 'http://47.107.153.105:8989/';
}
const service = axios.create({
    baseURL,
    // process.env.NODE_ENV === 'development' 来判断是否开发环境
    // easy-mock服务挂了，暂时不使用了
    // baseURL: 'https://www.easy-mock.com/mock/592501a391470c0ac1fab128',
    timeout: 5000
});

service.interceptors.request.use(
    config => {
        if (localStorage.token) {
            config.headers['Authorization'] = `Bearer ${localStorage.token}`
        }
        return config;
    },
    error => {
        console.log(error);
        return Promise.reject();
    }
);

service.interceptors.response.use(
    response => {
        if (response.status === 200) {
            if(response.data.code == 0){
                return response.data;
            }else if(response.data.code == 401){
                MessageBox.confirm('登录过期,请重新登录!', {
                    confirmButtonText: '登录',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    localStorage.clear()
                    router.push({ path: '/login' })
                })
            }
        } else {
            Promise.reject();
        }
    },
    error => {
        console.log(error);
        return Promise.reject();
    }
);

export default service;
