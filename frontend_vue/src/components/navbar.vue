<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

import Store from '../utils/store.js'


const store = Store()


function getLimit() {
    store.loading = true

    axios.get(`${store.api}/api/limit`, store.header)
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


function active(id: String) {
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
        store.component.title = 'Drive của tôi'
        store.component.url = 'home'
    }
    else if (id == '2') {
        store.component.title = 'Có gắn dấu sao'
        store.component.url = 'home?type=saved'
    }
    else if (id == '3') {
        store.component.title = 'Thùng rác'
        store.component.url = 'home?type=trash'
    }
}

</script>

<template>
    <div class="nav">
        <div class="nav-item select-item" id="1" @click="active('1')">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
            <p>Drive của tôi</p>
        </div>
        <div class="nav-item" id="2" @click="active('2')">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                <polygon
                    points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2">
                </polygon>
            </svg>
            <p>Có gắn dấu sao</p>
        </div>
        <div class="nav-item" id="3" @click="active('3')">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
            </svg>
            <p>Thùng rác</p>
        </div>
        <div class="d-flex flex-column gap-2 align-items-center">
            <div class="nav-item" id="4" @click="">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                    <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
                    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
                    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
                </svg>
                <p>Bộ nhớ</p>
            </div>
            <div class="progress">
                <div class="progress-bar bg-info" role="progressbar"
                    :style="`width: ${(parseFloat(store.limit.store) / parseFloat(store.profile.store)).toFixed(2)}%`"
                    aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <p class="fs-7 w-75">Đã sử dụng {{ (parseFloat(store.limit.store) / 1000).toFixed(2) }} Gb trong tổng {{
            parseFloat(store.profile.store) / 1000 }} Gb</p>
            <button>Mua thêm bộ nhớ</button>
        </div>
    </div>
</template>

<style scoped>
.nav {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-top: 70px;
}

.nav-item {
    display: flex;
    gap: 10px;
    align-items: center;
    padding: 5px 15px;
    border-radius: 10px;
    cursor: pointer;
    width: 100%;
    min-width: 200px;
    max-width: 250px;
}

.nav-item:hover {
    background-color: var(--hover_color);
}

.select-item {
    background-color: var(--active_color) !important;
}

.progress {
    height: 7px;
    width: 75%;
}
</style>