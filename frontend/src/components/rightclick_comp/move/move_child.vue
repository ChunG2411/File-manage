<script setup>
import { ref, defineProps } from 'vue'
import axios from 'axios'

import Store from '../../../utils/store.js'
import ChildRecur from './move_child_recur.vue'
import { checkError } from '../../../utils/functions.js'


const store = Store()
const data = ref([])
const loadChild = ref('')

const props = defineProps({
    url: String,
    id: String,
    type: String
})

function getData() {
    store.loading = true

    axios.get(`${store.api}/api/${props.url}`, store.header)
        .then(response => {
            data.value = response.data.folder
            store.loading = false
        })
        .catch(error => {
            checkError(error)
        })
}
getData()


function moveTo(id) {
    store.loading = true

    const form = new FormData()
    form.append('parent', id)

    axios.put(`${store.api}/api/${props.type}/${props.id}/detail`, form, store.header)
        .then(response => {
            store.loading = false
            store.toast = {
                title: 'success',
                content: 'Chuyển thành công'
            }
            store.reload = true
        })
        .catch(error => {
            checkError(error)
        })
}

</script>

<template>
    <template v-if="data.length > 0">
        <div class="ms-2" v-for="(i, index) in data">
            <div class="move-item">
                <div class="d-flex align-items-center gap-2">
                    <div class="icon rec-30">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            @click = "loadChild = i.id">
                            <path d="M6 9l6 6 6-6"/>
                        </svg>
                    </div>
                    <p>{{ (i.name.length > 20) ? i.name.slice(0, 20) + '...' : i.name }}</p>
                </div>
                <div class="icon rec-30">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        @click="moveTo(i.id)">
                        <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                        <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                    </svg>
                </div>
            </div>
            <div class="ms-2" v-if="loadChild == i.id">
                <ChildRecur :type="props.type" :id="props.id" :url="`folder/${i.id}`"></ChildRecur>
            </div>
        </div>
    </template>
    <div v-else>
        <p class="fs-7">Trống</p>
    </div>
</template>

<style scope>
</style>