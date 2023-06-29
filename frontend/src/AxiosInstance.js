import axios from "axios";

const BackendUrl = 'http://localhost/api/';
const mediaUrl = 'http://localhost/media/';

const axiosInstance = axios.create({
    baseURL : BackendUrl,
    timeout : 10000,
    withCredentials:true,
    headers :{
        'Content-Type' : 'application/json',
        accept : 'application/json',
        "Access-Control-Allow-Origin":"*",
        'Access-Control-Allow-Credentials':true
    }
})

export default axiosInstance
export {mediaUrl};