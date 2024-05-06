<script setup>
import { ref, defineProps } from 'vue'
import axios from 'axios'

import Store from '../../../utils/store.js'
import Child from './move_child.vue'


const store = Store()
const data = ref(null)

const props = defineProps({
    id: String,
    type: String
})


function getData() {
    store.loading = true

    axios.get(`${store.api}/api/home`, store.header)
        .then(response => {
            data.value = response.data.folder
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
getData()


function moveToHome() {
    store.loading = true

    const form = new FormData()
    form.append('parent', 'home')

    axios.put(`${store.api}/api/${props.type}/${props.id}/detail`, form, store.header)
        .then(response => {
            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Chuyển thành công'
            }
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

</script>

<template>
    <div class="move">
        <div class="move-card">
            <slot></slot>

            <div class="move-item mt-3">
                <div class="d-flex align-items-center gap-2">
                    <div class="icon rec-30">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M6 9l6 6 6-6"/>
                        </svg>
                    </div>
                    <p>Drive của tôi</p>
                </div>
                <div class="icon rec-30">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        @click="moveToHome()">
                        <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                        <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                    </svg>
                </div>
            </div>

            <Child :type="props.type" :id="props.id" url="home"></Child>
        </div>
    </div>
</template>

<style scope>
.move {
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

.move-card {
    min-width: 300px;
    padding: 20px;
    width: max-content;
    height: max-content;
    border-radius: 10px;
    background-color: var(--card_color);
}

.move-item {
    padding: 5px 10px;
    margin-bottom: 5px;
    background-color: var(--card_background_color);
    display: flex;
    justify-content: space-between;
}

</style>