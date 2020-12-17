/**
 * Author zifer
 * Date 2020-12-17 11:19
 * Description 文件说明
 * */
import request from '../utils/request';

export function uploadImg(file) {
    const formData = new FormData();
    formData.append('file', file);
    return request.post('/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
}
