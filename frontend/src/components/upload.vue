<script setup>
import axios from 'axios'
import { ref, watch } from 'vue'

import Store from '../utils/store.js'
import { checkError } from '../utils/functions.js'


const store = Store()
const process = ref([])


watch(() => store.upload, (newValue, _) => {
    const cur_process = {...newValue, process: 0, status: '0'}
    process.value.push(cur_process)
    upload(cur_process)
})

function upload(data) {
    axios.post(`${store.api}/api/file`, data.data, {
        headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`
            },
        onUploadProgress: function(progressEvent) {
            process.value.forEach(item => {
                if (item.id == data.id) {
                    item.process = Math.round((progressEvent.loaded / progressEvent.total) * 100)
                }
            })
        }
        })
        .then(response => {
            process.value.forEach(item => {
                if (item.id == data.id) {
                    item.status = '1'
                }
            })
            setTimeout(() => {
                process.value = process.value.filter((item)=>item.id != data.id)
            }, 2000)
            store.toast = {
                title: 'success',
                content: 'Tải lên thành công'
            }
            store.reload = true
        })
        .catch(error => {
            process.value.forEach(item => {
                if (item.id == data.id) {
                    item.status = '2'
                }
            })
            setTimeout(() => {
                process.value = process.value.filter((item)=>item.id != data.id)
            }, 2000)
            checkError(error)
        })
}

</script>

<template>
    <div class="upload" v-show="process.length > 0">
        <h6 class="mb-3">Danh sách tải lên</h6>
        <div class="d-flex align-items-center gap-2 mb-1" v-for="i in process">
            <p>{{ i.name.slice(0, 8) }}...</p>
            <div class="progress">
                <div class="progress-bar" :class="(i.status == '0') ? 'bg-info' : (i.status == '1') ? 'bg-success' : 'bg-danger'" role="progressbar"
                    :style="`width: ${i.process}%`"
                    aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
                </div>
            </div>
        </div>
    </div>
</template>

<style scope>
.upload {
    position: absolute;
    top: 10px;
    right: 10px;
    width: max-content;
    padding: 10px 20px;
    border-radius: 10px;
    background-color: var(--card_color);
    border: 1px solid var(--card_border_color);
    z-index: 99;
}

.progress {
    height: 7px;
    width: 150px;
}
</style>