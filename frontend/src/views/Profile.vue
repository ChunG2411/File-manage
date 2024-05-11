<script setup>
import Header from '../components/header.vue'
import Store from '../utils/store.js'
import { formatDate, formatSize } from '../utils/functions.js'

import { reactive, ref } from 'vue'
import axios from 'axios'


const store = Store()

const tab_active = ref('')
const preveiw_image = ref(null)
const request = ref(null)
const request_page = ref('')

const modify_form = reactive({
    fullname: '',
    avatar: '',
    email: '',
    old_pass: '',
    password: ''
})
const error = reactive({
    fullname: '',
    email: '',
    old_pass: '',
    password: ''
})


async function getProfile() {
    store.loading = true

    await axios.get(`${store.api}/api/my-profile`, store.header)
        .then(response => {
            store.profile = response.data
            preveiw_image.value = store.api + response.data.avatar
            modify_form.fullname = response.data.fullname
            modify_form.email = response.data.email.split('@')[0]
            
            store.loading = false
        })
        .catch(_ => {
            store.loading = false
            store.toast = {
                title: 'error',
                content: 'Vui lòng tải lại trang'
            }
        })
}
getProfile()

async function getLimit() {
    store.loading = true

    await axios.get(`${store.api}/api/limit`, store.header)
        .then(response => {
            store.limit = response.data
            store.loading = false
        })
        .catch(_ => {
            store.loading = false
            store.toast = {
                title: 'error',
                content: 'Vui lòng tải lại trang'
            }
        })
}

getLimit()


function activeTab(id) {
    const tabs = document.querySelectorAll('.tab-item')

    tabs.forEach(tab => {
        if (tab.id == id) {
            tab.classList.add('select-item')
            tab_active.value = id
        }
        else{
            tab.classList.remove('select-item')
        }
    })
    if (id=='2') {
        getRequest()
    }
}

function uploadImage (e) {
    try {
        modify_form.avatar = e.target.files[0]
        preveiw_image.value = URL.createObjectURL(modify_form.avatar)
    } catch {
        modify_form.avatar = ''
        preveiw_image.value = store.api + store.profile.avatar
    }
}

function cancelInfor() {
    modify_form.fullname = store.profile.fullname
    modify_form.email = store.profile.email.split('@')[0]
    modify_form.avatar = ''
    preveiw_image.value = store.api + store.profile.avatar
    error.email = ''
    error.fullname = ''
}

function cancelPass() {
    modify_form.old_pass = ''
    modify_form.password = ''
    error.old_pass = ''
    error.password = ''
}

function submitInfor() {
    error.email = ''
    error.fullname = ''

    const form = new FormData()
    if (modify_form.email + '@gmail.com' != store.profile.email) {
        if (modify_form.email == '') {
            error.email = 'Nhập email'
            return
        }
        else if (!checkEmail()) {
            return
        }
        form.append('email', modify_form.email + '@gmail.com')
    }
    if (modify_form.fullname != store.profile.fullname) {
        if (modify_form.fullname == '') {
            error.fullname = 'Nhập tên'
            return
        }
        form.append('fullname', modify_form.fullname)
    }
    if (modify_form.avatar) {
        form.append('avatar', modify_form.avatar)
    }
    
    store.loading = true
    axios.put(`${store.api}/api/my-profile`, form, store.header)
        .then(response => {
            store.profile = response.data
            preveiw_image.value = store.api + response.data.avatar
            modify_form.fullname = response.data.fullname
            modify_form.email = response.data.email.split('@')[0]
            modify_form.avatar = ''
            
            store.loading = false
        })
        .catch(_ => {
            store.loading = false
            store.toast = {
                title: 'error',
                content: 'Vui lòng tải lại trang'
            }
        })
}

function submitPass() {
    error.old_pass = ''
    error.password = ''

    const form = new FormData()
    if (modify_form.password == '') {
        error.password = 'Nhập mật khẩu'
        return
    }
    if (modify_form.old_pass == '') {
        error.old_pass = 'Nhập mật khẩu cũ'
        return
    }
    form.append('old_pass', modify_form.old_pass)
    form.append('password', modify_form.password)
    
    store.loading = true
    axios.put(`${store.api}/api/my-profile`, form, store.header)
        .then(response => {
            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Đổi mật khẩu thành công'
            }
        })
        .catch(error => {
            store.loading = false
            store.toast = {
                title: 'error',
                content: error.response.data
            }
        })
}

function checkEmail() {
    let status = true
    axios.get(`${store.api}/api/email?email=${modify_form.email}`)
        .catch(e => {
            error.email = e.response.data
            status = false
        })
    return status
}

function getType() {
    if (store.profile.type == '0') {
        return 'quản trị'
    }
    else {
        return 'người dùng'
    }
}

function upgrade() {
    store.loading = true

    axios.patch(`${store.api}/api/my-profile`, {}, store.header)
        .then(response => {
            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Đã gửi yêu cầu'
            }
        })
        .catch(error => {
            store.loading = false
            store.toast = {
                title: 'error',
                content: error.response.data
            }
        })
}

function getRequest() {
    store.loading = true

    axios.get(`${store.api}/api/request?page=${request_page.value}`, store.header)
        .then(response => {
            store.loading = false
            request.value = response.data
        })
        .catch(error => {
            store.loading = false
            store.toast = {
                title: 'error',
                content: 'Vui lòng tải lại trang'
            }
        })
}

function accept(id) {
    store.loading = true

    axios.patch(`${store.api}/api/request/${id}`, {}, store.header)
        .then(response => {
            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Đã chấp thuận'
            }
            getRequest()
        })
        .catch(error => {
            store.loading = false
            store.toast = {
                title: 'error',
                content: 'Vui lòng tải lại trang'
            }
        })
}

function reject(id) {
    store.loading = true

    axios.delete(`${store.api}/api/request/${id}`, store.header)
        .then(response => {
            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Đã từ chối'
            }
            getRequest()
        })
        .catch(error => {
            store.loading = false
            store.toast = {
                title: 'error',
                content: 'Vui lòng tải lại trang'
            }
        })
}

function getPage(url) {
    if (url.includes('=')) {
        const page = url.split('=').at(-1)
        request_page.value = page
    }
    else{
        request_page.value = ''
    }
    getRequest()
}

</script>

<template>
    <Header />
    <div class="main-content">
        <div class="profile">
            <div class="d-flex flex-column align-items-center gap-2 mb-4 mt-2">
                <div class="profile-img rec-150">
                    <img :src="store.api + store.profile.avatar"/>
                </div>
                <div class="text-center">
                    <p class="fs-7">{{ store.profile.email }}</p>
                    <h5>{{ store.profile.fullname }}</h5>
                </div>
            </div>
            <div>
                <div class="profile-tab">
                    <p class="tab-item" id='1' @click="activeTab('1')">Chỉnh sửa</p>
                    <p class="tab-item" id='2' @click="activeTab('2')" v-if="store.profile.type=='0'">Yêu cầu</p>
                    <p  class="tab-item" id='3' @click="activeTab('3')" v-else>Nâng cấp</p>
                    <p class="tab-item" id='4' @click="activeTab('4')">Đổi mật khẩu</p>
                </div>
                <div class="p-2">

                    <!-- -------------------------------------infor tab------------------------------------ -->
                    <div v-if="tab_active=='1'">
                        <div class="w-100 d-flex justify-content-center align-items-center mt-3 mb-2 position-relative">
                            <div class="profile-img rec-100">
                                <img :src="preveiw_image"/>
                            </div>
                            <input type="file" accept="image/*" id="image-upload" style="display:none;" @change="uploadImage"/>
                            <label for="image-upload" class="icon rec-30 label-upload">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <g transform="translate(2 3)">
                                        <path d="M20 16a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V5c0-1.1.9-2 2-2h3l2-3h6l2 3h3a2 2 0 0 1 2 2v11z"/>
                                        <circle cx="10" cy="10" r="4"/>
                                    </g>
                                </svg>
                            </label>
                        </div>
                        <div class="d-flex align-items-center mb-2">
                            <p class="w-25">Tên</p>
                            <div class="w-75">
                                <input type="text" class="form-control mt-2" :class="error.fullname ? 'input-error' : ''" placeholder="Tên" @keyup="error.fullname=''" v-model="modify_form.fullname">
                                <p class="fs-7 text-danger ms-2" v-if="error.fullname">{{ error.fullname }}</p>
                            </div>
                        </div>
                        <div class="d-flex align-items-center">
                            <p class="w-25">Email</p>
                            <div class="w-75">
                                <div class="input-group w-100">
                                    <input type="text" class="form-control" :class="error.email ? 'input-error' : ''" placeholder="Email" @keyup="error.email=''" v-model="modify_form.email">
                                    <div class="input-group-append">
                                        <span class="input-group-text">@gmail.com</span>
                                    </div>
                                </div>
                                <p class="fs-7 text-danger ms-2" v-if="error.email">{{ error.email }}</p>                              
                            </div>
                        </div>
                        <div class="d-flex gap-2 justify-content-end mt-3">
                            <button class="btn btn-outline-danger" @click="cancelInfor">Huỷ</button>
                            <button class="btn btn-primary" @click="submitInfor">Xác nhận</button>
                        </div>
                    </div>

                    <!-- -------------------------------------store tab------------------------------------ -->
                    <div v-if="tab_active=='3'">
                        <p>Tài khoản của bạn là tài khoản {{ getType() }}</p>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col"></th>
                                    <th scope="col">Tối đa</th>
                                    <th scope="col">Đã dùng</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <th scope="row">Dung lượng</th>
                                    <td>{{ formatSize(store.profile.store) }}</td>
                                    <td>{{ formatSize(store.limit.store) }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">Tải lên</th>
                                    <td>{{ store.profile.limit_upload }}</td>
                                    <td>{{ store.limit.upload }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">Tải xuống</th>
                                    <td>{{ store.profile.limit_download }}</td>
                                    <td>{{ store.limit.download }}</td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="d-flex gap-2 justify-content-end mt-3">
                            <button class="btn btn-primary" @click="upgrade" v-if="store.profile.type=='1'">Nâng cấp</button>
                        </div>
                    </div>

                    <div v-if="tab_active=='2'">
                        <div class="table-responsive">
                            <table class="table m-0">
                                <thead>
                                    <tr>
                                        <th scope="col">Email</th>
                                        <th scope="col">Thời gian</th>
                                        <th scope="col">Tình trạng</th>
                                        <th scope="col">Hành động</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="i in request?.results">
                                        <td>{{ i.profile.email }}</td>
                                        <td>{{ formatDate(i.created_at) }}</td>
                                        <td>
                                            <p class="bg-red fs-7" v-if="i.status=='2'">Từ chối</p>
                                            <p class="bg-green fs-7" v-if="i.status=='1'">Chấp thuận</p>
                                            <p class="bg-gray fs-7" v-if="i.status=='0'">Chờ xử lý</p>
                                        </td>
                                        <td class="d-flex align-items-center gap-2" v-if="i.status == '0'">
                                            <div class="icon rec-30" @click="accept(i.id)">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                                                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                    <polyline points="20 6 9 17 4 12"></polyline>
                                                </svg>
                                            </div>
                                            <div class="icon rec-30" @click="reject(i.id)">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                                                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                    <line x1="18" y1="6" x2="6" y2="18"></line>
                                                    <line x1="6" y1="6" x2="18" y2="18"></line>
                                                </svg>
                                            </div>  
                                        </td>
                                        <td v-else></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="w-100 d-flex justify-content-end gap-2">
                            <button v-if="request?.previous" @click="getPage(request.previous)">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M15 18l-6-6 6-6"/>
                                </svg>
                                <p>Trước đó</p>
                            </button>
                            <button v-if="request?.next" @click="getPage(request.next)">
                                <p>Tiếp theo</p>
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M9 18l6-6-6-6"/>
                                </svg>
                            </button>
                        </div>
                    </div>

                    <!-- -------------------------------------password tab------------------------------------ -->
                    <div v-if="tab_active=='4'">
                        <div class="d-flex align-items-center mb-2">
                            <p class="w-25">Mật khẩu cũ</p>
                            <div class="w-75">
                                <input type="text" class="form-control mt-2" :class="error.old_pass ? 'input-error' : ''" placeholder="Mật khẩu cũ" @keyup="error.old_pass=''" v-model="modify_form.old_pass">
                                <p class="fs-7 text-danger ms-2" v-if="error.old_pass">{{ error.old_pass }}</p>
                            </div>
                        </div>
                        <div class="d-flex align-items-center mb-2">
                            <p class="w-25">Mật khẩu mới</p>
                            <div class="w-75">
                                <input type="text" class="form-control mt-2" :class="error.password ? 'input-error' : ''" placeholder="Mật khẩu mới" @keyup="error.password=''" v-model="modify_form.password">
                                <p class="fs-7 text-danger ms-2" v-if="error.password">{{ error.password }}</p>
                            </div>
                        </div>
                        <div class="d-flex gap-2 justify-content-end mt-3">
                            <button class="btn btn-outline-danger" @click="cancelPass">Huỷ</button>
                            <button class="btn btn-primary" @click="submitPass">Xác nhận</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.main-content {
    width: 100%;
    height: 100%;
    padding: 10px;
    overflow: hidden;
    display: grid;
    place-items: center;
}

.profile {
    background-color: var(--card_color);
    border-radius: 10px;
    padding: 10px;
    margin-top: 50px;
    width: 70%;
    height: calc(100% - 50px);
    border: 1px solid var(--card_border_color);
}

.profile-tab {
    width: 100%;
    display: flex;
    align-items: center;
    border-bottom: 1px solid var(--card_border_color);
}

.tab-item {
    padding: 5px 15px;
    cursor: pointer;
}

.tab-item:hover {
    background-color: var(--hover_color);
}

.select-item {
    color: var(--active_text_color);
    border-bottom: 3px solid var(--active_border_color);
}

.label-upload {
    position: absolute;
    z-index: 30;
    background-color: var(--hover_color);
    opacity: 0.8;
}

.table-responsive {
    max-height:300px;
}

.table-responsive thead th {
    position: sticky;
    top: 0;
    z-index: 1;
}

</style>