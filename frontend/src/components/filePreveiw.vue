<script setup>
import { ref, defineProps, watch } from 'vue'
import axios from 'axios'

import Store from '../utils/store.js'
import pdf from '../assets/image/pdf.png'


const props = defineProps({
    src: String,
    id: String
})

const store = Store()
const file_format = ref(null)
const file_url = ref(null)


watch(()=>props.src, (newValue, _)=>{
    file_url.value = null
    checkFormat(newValue)
})

function checkFormat(name) {
    const end = name.split('.').at(-1)

    if(['gif', 'jpeg', 'jpg', 'png'].includes(end)){
        file_format.value = 'image'
        file_url.value = `${store.api}${props.src}`
    }
    else if(['rar', 'zip'].includes(end)){
        file_format.value = 'zip'
    }
    else if(['ppt', 'pptx'].includes(end)){
        file_format.value = 'ppt'
    }
    else if(['xls', 'xlsx'].includes(end)){
        file_format.value = 'xls'
    }
    else if(['doc', 'docx', 'txt'].includes(end)){
        file_format.value = 'doc'
    }
    else if(['mp4'].includes(end)){
        file_format.value = 'video'
        file_url.value = `${store.api}${props.src}`
    }
    else if(['pdf'].includes(end)){
        file_format.value = 'pdf'
        getPreview()
    }
    else {
        file_format.value = 'file'
    }
}
checkFormat(props.src)


function getPreview() {
    axios.get(`${store.api}/api/file/${props.id}/preview`, store.header)
        .then(response => {
            file_url.value = `${store.api}${response.data}`
        })
        .catch(_ => {
            file_url.value = pdf
        })
}

</script>

<template>
    <div class="file-preview">
        <img :src="file_url" v-if="file_format == 'image'"/>
        <img src="../assets/image/doc.png" v-else-if="file_format == 'doc'"/>
        <img src="../assets/image/zip.png" v-else-if="file_format == 'zip'"/>
        <img src="../assets/image/xls.png" v-else-if="file_format == 'xls'"/>
        <img src="../assets/image/ppt.png" v-else-if="file_format == 'ppt'"/>
        <video :src="file_url" v-else-if="file_format == 'video'"></video>
        <img :src="file_url" v-else-if="file_format == 'pdf'"/>
        <img src="../assets/image/file.png" v-else/>
    </div>
</template>

<style scope>
.file-preview {
    width: 170px;
    height: 120px;
    overflow: hidden;
    display: flex;
    justify-content: center;
    border-radius: 5px;
}

:where(.file-preview) img, video{
    height: 100%;
    width: 100%;
    object-fit: cover;
}

@media screen and (max-width: 550px) {
    .file-preview {
        width: 100px;
        height: 80px;
    }
}
</style>