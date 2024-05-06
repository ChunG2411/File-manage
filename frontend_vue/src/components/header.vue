<script setup>
import { ref } from 'vue'
import axios from 'axios'

import Store from '../utils/store.js'


const store = Store()
const input = ref('')


function getProfile() {
    store.loading = true

    axios.get(`${store.api}/api/my-profile`, store.header)
        .then(response => {
            store.profile = response.data
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

</script>

<template>
    <div class="header">
        <div class="d-flex gap-2 align-items-center pointer">
            <div class="logo rec-40">
                <img src="../assets/image/logo.png">
            </div>
            <h4>Drive</h4>
        </div>
        <div class="search">
            <div class="icon rec-30 position-absolute" style="left: 10px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
            </div>
            <input class="search-input" type="text" placeholder="Tìm trong Drive" v-model="input">
            <div class="icon rec-30 position-absolute" style="right: 10px;" @click="input = ''">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </div>
        </div>
        <div class="d-flex gap-2 align-items-center position-relative">
            <div class="icon rec-30">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                    <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
            </div>
            <div class="icon rec-30">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="3"></circle>
                    <path
                        d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z">
                    </path>
                </svg>
            </div>
            <div class="profile-img rec-30">
                <img :src="store.api + store.profile.avatar">
                <div class="profile-abs">
                    <p class="fs-7">Tài khoản người dùng</p>
                    <p class="fs-7">{{ store.profile.fullname }}</p>
                    <p class="fs-7">{{ store.profile.email }}</p>
                </div>
            </div>

        </div>
    </div>
</template>

<style scoped>
.header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    padding: 10px 20px 10px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-height: 60px;
    z-index: 50;
}

.search {
    display: flex;
    padding: 5px 50px;
    border-radius: 30px;
    background-color: #eeeeee;
    position: relative;
    align-items: center;
}

.search-input {
    background-color: transparent;
    border: 0;
}

.search-input:focus {
    outline-width: 0;
}

.profile-abs {
    display: none;
    position: absolute;
    top: 40px;
    right: 0;
    width: max-content;
    background-color: var(--card_color);
    padding: 5px 5px;
    border-radius: 5px;
    box-shadow: 0px 5px 20px 0px rgba(0, 0, 0, 0.1);
}

.profile-img:hover .profile-abs {
    display: block;
}
</style>