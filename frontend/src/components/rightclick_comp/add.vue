<script setup>
import { ref, watch, defineProps } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'


const store = Store()

const props = defineProps({
    type: String,
    id: String
})

const name = ref('')
const file = ref(null)
const show_error = ref('')


function addFolder() {
    if (name.value == '') {
        show_error.value = 'Vui lòng nhập tên'
        return
    }
    if (name.value.length > 100) {
        show_error.value = 'Tên tối đa 100 ký tự'
        return
    }
    store.loading = true

    const form = new FormData()
    form.append('parent', props.id)
    form.append('name', name.value)

    axios.post(`${store.api}/api/${props.type}`, form, store.header)
        .then(response => {
            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Thêm mới thành công'
            }
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

function upload_file(e) {
    file.value = e.target.files[0]
}

function addFile() {
    if (!file.value) {
        show_error.value = 'Vui lòng thêm tệp'
        return
    }
    store.loading = true

    const form = new FormData()
    form.append('parent', props.id)
    form.append('file', file.value)

    axios.post(`${store.api}/api/${props.type}`, form, store.header)
        .then(response => {
            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Thêm mới thành công'
            }
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
    <div class="add">
        <div v-if="props.type == 'folder'">
            <slot></slot>
            <input class="form-control mt-3" :class="show_error ? 'input-error' : ''" type="text" placeholder="Nhập tên" v-model="name" @keypress="show_error=false">
            <p class="fs-7 ms-1 text-danger" v-if="show_error">{{ show_error }}</p>
            <div class="d-flex gap-2 justify-content-end mt-3">
                <button class="btn btn-primary" @click="addFolder">Xác nhận</button>
            </div>
        </div>
        <div v-if="props.type == 'file'">
            <slot></slot>
            <input class="form-control mt-3" :class="show_error ? 'input-error' : ''" type="file" @change="upload_file">
            <p class="fs-7 ms-1 text-danger" v-if="show_error">{{ show_error }}</p>
            <div class="d-flex gap-2 justify-content-end mt-3">
                <button class="btn btn-primary" @click="addFile">Xác nhận</button>
            </div>
        </div>
    </div>
</template>

<style scope>
.add {
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

.add > div {
    min-width: 300px;
    padding: 20px;
    width: max-content;
    height: max-content;
    border-radius: 10px;
    background-color: var(--card_color);
}
</style>