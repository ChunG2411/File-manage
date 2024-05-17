<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

import Store from '../utils/store.js'
import { checkError } from '../utils/functions.js'


const store = Store()
const router = useRouter()

const tab = ref(true)
const show_pw = ref(false)
const captcha = ref([])

const form_signup = reactive({
    email: '',
    pass: '',
    repass: '',
    captcha: '',
    code: ''
})
const form_signin = reactive({
    email: '',
    pass: ''
})
const error = reactive({
    email: '',
    pass: '',
    captcha: '',
    code: ''
})


function get_captcha() {
    captcha.value = []
    for (let i = 0; i < 6; i++) {
        const number = Math.floor((Math.random() * (122 - 97 + 1)) + 97)
        captcha.value.push(String.fromCharCode(number))
    }
}

function checkValidate() {
    let status = true
    error.email = ''
    error.pass = ''
    error.captcha = ''
    error.code = ''

    if (!form_signup.code) {
        error.code = "Nhập mã xác thực email"
        status = false
    }
    if (form_signup.pass != form_signup.repass) {
        error.pass = "Mật khẩu không khớp"
        status = false
    }
    if (form_signup.captcha != captcha.value.join('')) {
        error.captcha = "Mã xác nhận không chính xác"
        form_signup.captcha = ''
        status = false
    }

    axios.get(`${store.api}/api/email?email=${form_signup.email}`)
        .catch(e => {
            error.email = e.response.data
            status = false
        })

    return status
}

async function sendCode() {
    let status = true

    if (form_signup.email == '') {
        error.email = "Nhập email"
        return
    }

    await axios.get(`${store.api}/api/email?email=${form_signup.email}`)
        .catch(e => {
            error.email = e.response.data
            status = false
        })
    
    if (status) {
        const form = new FormData()
        form.append('email', form_signup.email)

        axios.post(`${store.api}/api/get-code`, form)
            .then(response => {
                store.toast = {
                    title: 'success',
                    content: 'Mã xác thực được gửi đến email của bạn'
                }
            })
            .catch(error => {
                checkError(error)
            })        
    }
}

function Signin() {
    store.loading = true

    const form = new FormData()
    form.append('username_email', form_signin.email)
    form.append('password', form_signin.pass)

    axios.post(`${store.api}/api/login`, form)
        .then(response => {
            localStorage.setItem('token', response.data.access_token)
            store.header.headers.Authorization = `Bearer ${response.data.access_token}`
            store.is_login = true

            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Đăng nhập thành công'
            }
            
            if (store.pre_router) {
                router.push({ path: store.pre_router })
            }
            else {
                router.push({ path: '/' })
            }
        })
        .catch(error => {
            checkError(error)
        })
}

function Signup() {
    store.loading = true
    if (!checkValidate()) {
        store.loading = false
        store.toast = {
            title: 'error',
            content: 'Vui lòng kiểm tra lại thông tin'
        }
    }
    else {
        const form = new FormData()
        form.append('email', form_signup.email + '@gmail.com')
        form.append('username', form_signup.email)
        form.append('password', form_signup.pass)
        form.append('code', form_signup.code)

        axios.post(`${store.api}/api/register`, form)
            .then(_ => {
                store.loading = false
                store.toast = {
                    title: 'success',
                    content: 'Đăng ký tài khoản thành công'
                }
                tab.value = true
            })
            .catch(error => {
                checkError(error)
            })
    }
}

</script>

<template>
    <div class="auth">
        <div class="auth-card">
            <div>
                <h1>Chào mừng đến với</h1>
                <div class="d-flex gap-3 align-items-center mt-3 ms-3">
                    <div class="logo rec-100">
                        <img src="../assets/image/logo.png">
                    </div>
                    <h2 class="font-weight-bold">Drive</h2>
                </div>
            </div>

            <!-- -----------------signin----------------------- -->
            <form class="text-center" @submit.prevent="Signin" v-if="tab">
                <h3>Đăng nhập</h3>
                <div class="d-flex flex-column gap-2 mt-3 mb-3">
                    <input type="text" class="form-control" placeholder="Tên tài khoản hoặc Email"
                        v-model="form_signin.email" required>
                    <input :type="show_pw ? 'text' : 'password'" class="form-control" placeholder="Mật khẩu"
                        v-model="form_signin.pass" required>
                    <div class="d-flex gap-2 align-items-center ms-1">
                        <input type="checkbox" id="show_pw" v-model="show_pw">
                        <label class="fs-7" for="show_pw">Hiển thị mật khẩu</label>
                    </div>
                </div>
                <button type="submit" class="btn btn-primary">Đăng nhập</button>
                <div class="d-flex gap-1 justify-content-center align-items-center mt-2">
                    <p class="fs-7">Chưa có tài khoản:</p>
                    <b class="pointer fs-7" @click="tab = false; get_captcha()">Đăng ký</b>
                </div>
            </form>

            <!-- -----------------signup----------------------- -->
            <form class="text-center" @submit.prevent="Signup" v-else>
                <h3>Tạo tài khoản</h3>
                <div class="d-flex flex-column mt-3 mb-3">
                    <div class="input-group">
                        <input type="text" class="form-control" :class="error.email ? 'input-error' : ''" placeholder="Email"
                            v-model="form_signup.email" @keyup="error.email=''" required>
                        <div class="input-group-append">
                            <span class="input-group-text">@gmail.com</span>
                        </div>
                    </div>
                    <p class="fs-7 text-danger ms-2" v-if="error.email">{{ error.email }}</p>

                    <div class="d-flex gap-2 align-items-center mt-2">
                        <input type="text" class="form-control" placeholder="Mã xác thực email"
                            v-model="form_signup.code" required>
                        <button type="button" @click="sendCode">Gửi mã</button>
                    </div>
                    <p class="fs-7 text-danger ms-2" v-if="error.code">{{ error.code }}</p>

                    <input type="text" class="form-control mt-2" :class="error.pass ? 'input-error' : ''" placeholder="Mật khẩu"
                        v-model="form_signup.pass" @keyup="error.pass=''" required>
                    <input type="text" class="form-control mt-2" :class="error.pass ? 'input-error' : ''" placeholder="Nhập lại mật khẩu"
                        v-model="form_signup.repass" @keyup="error.pass=''" required>
                    <p class="fs-7 text-danger ms-2" v-if="error.pass">{{ error.pass }}</p>

                    <div class="d-flex gap-2 align-items-center mt-2">
                        <input type="text" class="form-control" :class="error.captcha ? 'input-error' : ''" placeholder="Mã Captcha"
                            v-model="form_signup.captcha" @keyup="error.captcha=''" required>
                        <div class="position-relative d-flex align-items-center">
                            <input type="text" class="form-control" :value="captcha.join('')" disabled readonly>
                            <div class="icon rec-30 position-absolute" style="right: 3px" @click="get_captcha">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                    fill="none" stroke="#000000" stroke-width="2" stroke-linecap="square"
                                    stroke-linejoin="round">
                                    <path d="M2.5 2v6h6M2.66 15.57a10 10 0 1 0 .57-8.38" />
                                </svg>
                            </div>
                        </div>
                    </div>
                    <p class="fs-7 text-danger ms-2" v-if="error.captcha">{{ error.captcha }}</p>

                </div>
                <button type="submit" class="btn btn-primary">Đăng ký</button>
                <div class="d-flex gap-1 justify-content-center align-items-center mt-2">
                    <p class="fs-7">Đã có tài khoản:</p>
                    <b class="pointer fs-7" @click="tab = true">Đăng nhập</b>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
.auth {
    background-color: var(--card_color);
    padding: 40px 30px;
    border-radius: 10px;
    width: max-content;
    min-width: 300px;
    max-width: 900px;
    border: 1px solid var(--card_border_color);
}

.auth-card {
    display: flex;
    align-items: center;
    gap: 50px;
}


@media screen and (max-width: 700px) {
    .auth {
        width: 100%;
        max-width: 100%;
    }
    .auth-card {
        flex-direction: column;
        gap: 30px;
    }
}

@media screen and (max-width: 550px) {
    .logo {
        width: 70px !important;
        min-width: 70px !important;
    }
}
</style>