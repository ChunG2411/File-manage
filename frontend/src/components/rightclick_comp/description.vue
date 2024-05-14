<script setup>
import { ref, watch, defineProps } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'


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
            data.value = response.data.description
            new_data.value = data.value
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

function submit() {
    store.loading = true

    const form = new FormData()
    form.append('description', new_data.value)

    axios.put(`${store.api}/api/${props.type}/${props.id}/detail`, form, store.header)
        .then(response => {
            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Thay đổi thành công'
            }
            store.reload = true
        })
        .catch(_ => {
            store.loading = false
            store.toast = {
                title: 'error',
                content: 'Vui lòng tải lại trang'
            }
        })
}


</script>

<template>
    <div class="change-description">
        <div>
            <slot></slot>
            <input class="form-control mt-3" type="text" placeholder="Nhập mô tả" v-model="new_data">
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