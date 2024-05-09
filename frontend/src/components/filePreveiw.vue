<script setup>
import { ref, defineProps, watch } from 'vue'

import Store from '../utils/store.js'


const props = defineProps({
    src: String
})

const store = Store()
const file_format = ref(null)

watch(()=>props.src, (newValue, _)=>{
    checkFormat(newValue)
})

function checkFormat(name) {
    const end = name.split('.').at(-1)

    if(['gif', 'jpeg', 'jpg', 'png'].includes(end)){
        file_format.value = 'image'
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
    else {
        file_format.value = 'file'
    }
}
checkFormat(props.src)

</script>

<template>
    <div class="file-preview">
        <img :src="`${store.api}${props.src}`" v-if="file_format == 'image'"/>
        <img src="../assets/image/doc.png" v-else-if="file_format == 'doc'"/>
        <img src="../assets/image/zip.png" v-else-if="file_format == 'zip'"/>
        <img src="../assets/image/xls.png" v-else-if="file_format == 'xls'"/>
        <img src="../assets/image/ppt.png" v-else-if="file_format == 'ppt'"/>
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
    border-radius: 10px;
}

.file-preview img{
    height: 100% !important;
    width: max-content !important;
}
</style>