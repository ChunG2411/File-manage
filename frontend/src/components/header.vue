<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'
import { useRouter } from 'vue-router'

import { getText, checkError } from '../utils/functions.js'
import Store from '../utils/store.js'


const store = Store()
const router = useRouter()

const input = ref('')
const search_data = ref(null)

const card = ref('')


function getProfile() {
    store.loading = true

    axios.get(`${store.api}/api/my-profile`, store.header)
        .then(response => {
            store.profile = response.data
            store.loading = false
        })
        .catch(error => {
            checkError(error)
        })
}
getProfile()

function closeMenu() {
    card.value = ''
}

function search() {
    store.loading = true

    axios.get(`${store.api}/api/search?search=${input.value}`, store.header)
        .then(response => {
            search_data.value = response.data
            card.value = 'search'
            store.loading = false
        })
        .catch(error => {
            checkError(error)
        })
}

function Logout(params) {
    store.loading = true

    const form = new FormData()
    if (params == 'all') {
        form.append('all', 'true')
    }

    axios.post(`${store.api}/api/logout`, form, store.header)
        .then(response => {
            localStorage.removeItem('token')
            store.is_login = false

            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Đăng xuất thành công'
            }
            router.push({ path: '/login' })
        })
        .catch(error => {
            checkError(error)
        })
}

function getFolder(id) {
    input.value = ''
    search_data.value = null
    card.value = null
    router.push({ name: 'card_folder', params: { id } })
}

function setTheme(theme) {
    store.loading = true
    setTimeout(()=>{
        localStorage.setItem('theme', theme)
        document.documentElement.className = theme
        store.loading = false
    }, 1000)
}

function setLang(lang) {
    store.loading = true
    setTimeout(()=>{
        localStorage.setItem('lang', lang)
        store.lang = lang
        store.loading = false
    }, 1000)
}

</script>

<template>
    <div class="header">
        <router-link to="/home" class="header-logo">
            <div class="logo rec-40">
                <img src="../assets/image/logo.png">
            </div>
            <h4>Drive</h4>
        </router-link>
        <div class="search">
            <div class="icon rec-30 position-absolute" style="left: 10px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
            </div>
            <input class="search-input" type="text" placeholder="Tìm trong Drive" v-model="input" @keyup="search">
            <div class="icon rec-30 position-absolute" style="right: 10px;" @click="input = '';search_data=null">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </div>
            <div class="header-card w-100" style="top:100%;left:0" v-if="card=='search' && input" v-on-click-outside="closeMenu">
                <div class="header-card-1 header-card-item" v-for="i in search_data.folder">
                    <div class="d-flex align-items-center gap-3 pointer" @click="getFolder(i.id)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z">
                            </path>
                        </svg>
                        <p>{{ i.name }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="d-flex gap-2 align-items-center position-relative">
            <div class="position-relative">
                <div class="icon rec-30" @click="card='setting'">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="3"></circle>
                        <path
                            d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 
                                1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 
                                0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 
                                1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 
                                0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 
                                1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 
                                0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 
                                1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 
                                0 0 0-1.51 1z">
                        </path>
                    </svg>
                </div>
                <div class="header-card" v-if="card=='setting'" v-on-click-outside="closeMenu">
                    <div class="header-card-1 header-card-item">
                        <p>{{ getText(store.lang, 'header', '1') }}</p>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M9 18l6-6-6-6"/>
                        </svg>
                        <div class="header-card-2">
                            <div class="header-card-item" @click="setTheme('light')">
                                <p>{{ getText(store.lang, 'header', '2') }}</p>
                            </div>
                            <div class="header-card-item" @click="setTheme('dark')">
                                <p>{{ getText(store.lang, 'header', '3') }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="header-card-1 header-card-item">
                        <p>{{ getText(store.lang, 'header', '4') }}</p>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M9 18l6-6-6-6"/>
                        </svg>
                        <div class="header-card-2">
                            <div class="header-card-item" @click="setLang('en')">
                                <p>{{ getText(store.lang, 'header', '5') }}</p>
                            </div>
                            <div class="header-card-item" @click="setLang('vi')">
                                <p>{{ getText(store.lang, 'header', '6') }}</p>
                            </div>
                            <div class="header-card-item" @click="setLang('zh')">
                                <p>{{ getText(store.lang, 'header', '7') }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="position-relative">
                <div class="profile-img rec-30" @click="card='profile'">
                    <img :src="store.api + store.profile.avatar">
                    <div class="profile-abs">
                        <p class="fs-7">{{ getText(store.lang, 'header', '8') }}</p>
                        <p class="fs-7">{{ store.profile.fullname }}</p>
                        <p class="fs-7">{{ store.profile.email }}</p>
                    </div>
                </div>
                <div class="header-card" v-if="card=='profile'" v-on-click-outside="closeMenu">
                    <router-link to="/profile" class="header-card-1 header-card-item">
                        <p>{{ getText(store.lang, 'header', '9') }}</p>
                    </router-link>
                    <div class="header-card-1 header-card-item" @click="Logout('all')">
                        <p>{{ getText(store.lang, 'header', '10') }}</p>
                    </div>
                    <div class="header-card-1 header-card-item" @click="Logout('')">
                        <p>{{ getText(store.lang, 'header', '11') }}</p>
                    </div>
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
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-height: 60px;
    z-index: 50;
}

.header-logo {
    display: flex;
    align-items: center;
    cursor: pointer;
    gap: 10px;
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

.header-card {
    position: absolute;
    background-color: var(--card_color);
    border-radius: 10px;
    box-shadow: 0px 3px 5px 3px rgba(0, 0, 0, 0.1);
    z-index: 60;
    padding: 10px 0;
    width: max-content;
    height: max-content;
    display: flex;
    flex-direction: column;
    right: 0;
}

.header-card-item {
    padding: 5px 10px;
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
    position: relative;
    min-width: 100px;
}

.header-card-item:hover {
    background-color: var(--hover_color);
}

.header-card-1:hover .header-card-2{
    display: flex;
}

.header-card-2 {
    display: none;
    position: absolute;
    background-color: var(--card_color);
    border-radius: 10px;
    box-shadow: 0px 3px 5px 3px rgba(0, 0, 0, 0.1);
    z-index: 50;
    padding: 10px 0;
    width: max-content;
    height: max-content;
    flex-direction: column;
    right: 100%;
    top: 0;
}

@media screen and (max-width: 550px) {
    .header-logo {
        display: none;
    }
    .search {
        width: 70%;
    }
}
</style>