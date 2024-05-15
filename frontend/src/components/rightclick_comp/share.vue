<script setup>
import { ref, watch, defineProps } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { checkError } from '../../utils/functions.js'


const store = Store()

const props = defineProps({
    type: String,
    id: String
})
const data = ref(null)
const new_data = ref('')


watch(() => props.id, (newValue, _) => {
    getDetail()
})


function getDetail() {
    store.loading = true

    axios.get(`${store.api}/api/${props.type}/${props.id}/detail`, store.header)
        .then(response => {
            data.value = response.data.permissions
            new_data.value = data.value
            store.loading = false
        })
        .catch(error => {
            checkError(error)
        })
}

getDetail()

function submit() {
    store.loading = true

    const form = new FormData()
    form.append('permissions', new_data.value)

    axios.put(`${store.api}/api/${props.type}/${props.id}/detail`, form, store.header)
        .then(response => {
            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Thay đổi thành công'
            }
            store.reload = true
        })
        .catch(error => {
            checkError(error)
        })
}

function copyLink(e) {
    const url = `http://localhost:5173/file/${props.id}`
    navigator.clipboard.writeText(url)
    e.target.innerHTML = 'Đã sao chép'
}


</script>

<template>
    <div class="change-description">
        <div>
            <slot></slot>
            <select class="form-select mt-3 mb-2" v-model="new_data">
                <option value="0">Cá nhân</option>
                <option value="1">Công khai</option>
            </select>
            <button @click="copyLink">Sao chép liên kết</button>
            <div class="d-flex gap-2 justify-content-end mt-3">
                <button class="btn btn-outline-danger" @click="new_data=data">Huỷ</button>
                <button class="btn btn-primary" @click="submit">Xác nhận</button>
            </div>
        </div>
    </div>
</template>

<style scope>
.change-description {
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

.change-description > div {
    min-width: 300px;
    padding: 20px;
    width: max-content;
    height: max-content;
    border-radius: 10px;
    background-color: var(--card_color);
}
</style>