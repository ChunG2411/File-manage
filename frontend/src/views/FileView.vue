<script setup>
import axios from 'axios'
import { ref } from 'vue'
import Preveiw from '../components/preview/preveiw.vue'

import { useRoute, useRouter } from 'vue-router'
import Store from '../utils/store.js'


const store = Store()
const route = useRoute()
const router = useRouter()

const data = ref(null)
const permission = ref('')


function getDetail() {
    store.loading = true

    axios.get(`${store.api}/api/file/${route.params.id}/detail`, store.header)
        .then(response => {
            data.value = response.data
            permission.value = response.data.permissions
            store.loading = false
        })
        .catch(_ => {
            store.loading = false
            router.push({name: 'not_found'})
        })
}

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
getDetail()


function saveFunc() {
    store.loading = true

    axios.patch(`${store.api}/api/file/${data.value.id}/detail`, {}, store.header)
        .then(response => {
            store.toast = {
                title: 'success',
                content: 'Đã thêm dấu sao'
            }
            store.loading = false
        })
        .catch(error => {
            store.loading = false
            store.toast = {
                title: 'error',
                content: error.response.data
            }
        })
}

function downloadFile() {
    axios.get(`${store.api}/api/file/${data.value.id}/download`,
                {
                    responseType: 'blob',
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}`}
                })
        .then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', data.value.name)
            document.body.appendChild(link)
            link.click()

            store.toast = {
                title: 'info',
                content: 'Đang tải xuống'
            }
        })
        .catch(error => {
            store.toast = {
                title: 'error',
                content: 'Vui lòng thử lại'
            }
        })
}
</script>

<template>
    <template v-if="data">
        <div v-if="permission=='0' && data.created_by !== store.profile.user">
            <h5>Bạn không có quyền xem tệp này</h5>
            <p>Vui lòng liên hệ lại chủ sở hữu</p>
        </div>
        <Preveiw :data="data" :showClose="false" @click-save="saveFunc" @click-download="downloadFile" v-else></Preveiw>
    </template>
</template>

<style scoped>
</style>