<script setup>
import { ref, watch, defineProps } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { formatDate } from '../../utils/functions.js'


const store = Store()

const props = defineProps({
    type: String,
    id: String
})
const data = ref(null)


watch(() => props.id, (newValue, _) => {
    getDetail()
})


function getDetail() {
    store.loading = true

    axios.get(`${store.api}/api/${props.type}/${props.id}/detail`, store.header)
        .then(response => {
            data.value = response.data
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

getDetail()

function restore() {
    store.loading = true

    axios.patch(`${store.api}/api/${props.type}/${props.id}`, {}, store.header)
        .then(response => {
            data.value = null
            store.toast = {
                title: 'success',
                content: 'Đã khôi phục'
            }
            store.loading = false
            store.component.reload = true
        })
        .catch(_ => {
            store.loading = false
            store.toast = {
                title: 'error',
                content: 'Vui lòng tải lại trang'
            }
        })
}

function unsave() {
    store.loading = true

    axios.patch(`${store.api}/api/${props.type}/${props.id}/detail?status=unsave`, {}, store.header)
        .then(response => {
            store.toast = {
                title: 'success',
                content: 'Đã bỏ dấu sao'
            }
            store.loading = false
            store.component.reload = true
        })
        .catch(error => {
            store.loading = false
            store.toast = {
                title: 'error',
                content: error.response.data
            }
        })
}

</script>

<template>
    <div class="card custom-card" v-if="data">
        <slot></slot>

        <div class="d-flex gap-2 mt-3">
            <b>Tên: </b>
            <p>{{ data.name }}</p>
        </div>
        <div class="d-flex gap-2 mt-2">
            <b>Mô tả: </b>
            <p>{{ data.description ? data.description : '' }}</p>
        </div>
        <div class="d-flex gap-2 mt-2">
            <b>Kích thước: </b>
            <p>{{ data.size ? (data.size / 1024).toFixed(2) : '0' }} Mb</p>
        </div>
        <div class="d-flex gap-2 mt-2">
            <b>Người sở hữu: </b>
            <p>{{ data?.created_by }}</p>
        </div>
        <div class="d-flex gap-2 mt-2">
            <b>Ngày chỉnh sửa cuối: </b>
            <p>{{ formatDate(data.updated_at) }}</p>
        </div>
        <div class="d-flex gap-2 mt-2">
            <b>Ngày tạo: </b>
            <p>{{ formatDate(data.created_at) }}</p>
        </div>
        <div class="d-flex gap-2 mt-2">
            <b>Quyền: </b>
            <p>{{ (data.permissions == '0') ? 'Cá nhân' : 'Công khai' }}</p>
        </div>
        <div class="d-flex justify-content-center mt-3">
            <button @click="unsave" v-if="data.saved">Bỏ dấu sao</button>
        </div>
        <div class="d-flex justify-content-center mt-3">
            <button @click="restore" v-if="data.deleted">Khôi phục</button>
        </div>
    </div>
</template>

<style scope>
.custom-card {
    width: 350px;
    min-width: 350px;
    max-width: 350px;
    overflow-y: scroll;
    overflow-x: hidden;
}
</style>