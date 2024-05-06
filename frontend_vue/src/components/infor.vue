<script setup>
import { ref, watch, defineProps } from 'vue'
import axios from 'axios'

import Store from '../utils/store.js'
import formatDate from '../utils/functions.js'


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



</script>

<template>
    <div class="infor" v-if="data">
        <h5>Chi tiết {{ (props.type == 'folder') ? 'thư mục' : 'tệp tin' }}</h5>
        <div class="d-flex gap-2 mt-3">
            <b>Tên: </b>
            <div>
                <p>{{ data.name }}</p>
                <button class="mt-1">Đổi tên</button>
            </div>
        </div>
        <div class="d-flex gap-2 mt-2">
            <b>Mô tả: </b>
            <div>
                <p>{{ data.description ? data.description : 'Không có' }}</p>
                <button class="mt-1">Chỉnh sửa</button>
            </div>
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
            <div>
                <p>{{ (data.permission == '0') ? 'Công khai' : 'Cá nhân' }}</p>
                <button class="mt-1">Thay đổi</button>
            </div>
        </div>
    </div>
</template>

<style>
.infor {
    position: absolute;
    right: 0;
    bottom: 0;
    height: 100%;
    width: 350px;
    max-width: 350px;
    overflow-y: scroll;
    overflow-x: hidden;
    z-index: 50;
    background-color: var(--card_color);
    border-radius: 10px;
    box-shadow: 0px 3px 5px 3px rgba(0, 0, 0, 0.1);
    padding: 10px;
}
</style>