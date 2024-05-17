<script setup>
import axios from 'axios'
import { ref } from 'vue';
import { useRouter } from 'vue-router'

import Store from '../utils/store.js'
import { formatSize, checkError } from '../utils/functions.js'


const store = Store()
const router = useRouter()

const showComp = ref('')


async function getLimit() {
    store.loading = true

    await axios.get(`${store.api}/api/limit`, store.header)
        .then(response => {
            store.limit = response.data
            store.loading = false
        })
        .catch(_ => {
            checkError(error)
        })
}

getLimit()


function active(id) {
    const items = document.querySelectorAll('.nav-item')
    items.forEach(item => {
        if (item.id == id) {
            item.classList.add('select-item')
        }
        else {
            item.classList.remove('select-item')
        }
    })

    if (id == '1') {
        router.push({name: 'card_type', params: {type: 'home'}})
    }
    else if (id == '2') {
        router.push({name: 'card_type', params: {type: 'saved'}})
    }
    else if (id == '3') {
        router.push({name: 'card_type', params: {type: 'trash'}})
    }
}

function getType() {
    if (store.profile.type == '0') {
        return 'quản trị'
    }
    else {
        return 'người dùng'
    }
}

function sendRequest() {
    store.loading = true

    axios.patch(`${store.api}/api/my-profile`, {}, store.header)
        .then(response => {
            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Đã gửi yêu cầu'
            }
            showComp.value = ''
        })
        .catch(error => {
            checkError(error)
        })
}

</script>

<template>
    <div class="nav">
        <div class="nav-list">
            <div class="nav-item select-item" id="1" @click="active('1')">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
                <p>Drive của tôi</p>
            </div>
            <div class="nav-item" id="2" @click="active('2')">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                    <polygon
                        points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2">
                    </polygon>
                </svg>
                <p>Có gắn dấu sao</p>
            </div>
            <div class="nav-item" id="3" @click="active('3')">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    <line x1="10" y1="11" x2="10" y2="17"></line>
                    <line x1="14" y1="11" x2="14" y2="17"></line>
                </svg>
                <p>Thùng rác</p>
            </div>
            <div class="d-flex flex-column gap-2 align-items-center">
                <div class="nav-item" id="4" @click="showComp='store'">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                        <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
                        <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
                        <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
                    </svg>
                    <p>Bộ nhớ</p>
                </div>
                <div class="store-infor">
                    <div class="progress">
                        <div class="progress-bar bg-info" role="progressbar"
                            :style="`width: ${((parseFloat(store.limit.store) / parseFloat(store.profile.store)) * 100).toFixed(2)}%`"
                            aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">
                        </div>
                    </div>
                    <p class="fs-7 w-75">Đã sử dụng {{ formatSize(store.limit.store) }} trong tổng {{ formatSize(store.profile.store) }}</p>
                    <button @click="showComp='upgrade'">Nâng cấp tài khoản</button>
                </div>
            </div>
        </div>
    </div>
    <!-- -----------------------------------------------popup---------------------------------------------------- -->
    <div class="buy" v-if="showComp=='upgrade'">
        <div>
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5>Nâng cấp tài khoản</h5>
                <div class="icon rec-30" @click="showComp=''">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </div>
            </div>
            <p>Tài khoản của bạn là tài khoản {{ getType() }}</p>
            <div class="d-flex gap-2 justify-content-end mt-3">
                <button class="btn btn-success" v-if="store.profile.type!='0'" @click="sendRequest">Nâng cấp</button>
                <button class="btn btn-primary" @click="showComp=''">Xác nhận</button>
            </div>
        </div>
    </div>
    <div class="buy" v-if="showComp=='store'">
        <div>
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5>Bộ nhớ</h5>
                <div class="icon rec-30" @click="showComp=''">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </div>
            </div>
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
                <button class="btn btn-primary" @click="showComp=''">Xác nhận</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.nav {
    margin-top: 70px;
    min-width: 200px;
    max-width: 200px;
}

.nav-list {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.nav-item {
    display: flex;
    gap: 10px;
    align-items: center;
    padding: 5px 15px;
    border-radius: 10px;
    cursor: pointer;
    width: 100%;
}

.nav-item:hover {
    background-color: var(--hover_color);
}

.select-item {
    background-color: var(--active_background_color) !important;
}

.store-infor {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
}

.progress {
    height: 7px;
    width: 75%;
}

.buy {
    position: absolute;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    background-color: var(--card_background_color);
    z-index: 50;
    display: grid;
    place-items: center;
}

.buy > div {
    min-width: 300px;
    padding: 20px;
    width: max-content;
    height: max-content;
    border-radius: 10px;
    background-color: var(--card_color);
}

@media screen and (max-width: 700px) {
  .nav {
    position: fixed;
    bottom: 0;
    left: 0;
    z-index: 49;
    width: 100%;
    max-width: 100%;
    margin-top: 0;
    display: flex;
    justify-content: center;
  }
  .nav-list {
    flex-direction: row;
    background-color: var(--card_color);
    border-radius: 10px;
    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.1);
    padding: 5px;
  }
  .nav-item {
    width: max-content;
    height: max-content;
    flex-direction: column;
    gap: 2px;
    padding: 5px 10px;
  }
  .store-infor {
    display: none;
  }
}
</style>