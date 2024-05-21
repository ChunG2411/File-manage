<script setup>
import { ref, watch, defineProps } from 'vue'

import Store from '../../utils/store.js'


const store = Store()
const props = defineProps({
    data: Object,
    showClose: Boolean
})
const file_format = ref('')
const file = ref(null)


watch(() => props.data, (newValue, _) => {
    checkFormat(newValue.file)
})

function checkFormat(name) {
    const end = name.split('.').at(-1)

    if(['gif', 'jpeg', 'jpg', 'png'].includes(end)){
        file_format.value = 'image'
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
    }
    else if(['pdf'].includes(end)){
        file_format.value = 'pdf'
    }
    else {
        file_format.value = 'file'
    }
}
checkFormat(props.data.file)

</script>

<template>
    <div class="preview">
        <div class="preveiw-header">
            <h6>{{ props.data.name }}</h6>
            <div class="d-flex align-items-center gap-2">
                <div class="icon rec-30" @click="$emit('clickDownload')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5"/>
                    </svg>
                </div>
                <div class="icon rec-30" @click="$emit('clickSave')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
                    </svg>
                </div>
                <div class="icon rec-30" @click="$emit('clickClose')" v-if="showClose">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </div>
                <div class="profile-img rec-30">
                    <img :src="store.api + store.profile.avatar">
                </div>
            </div>
        </div>
        <div class="preveiw-content">
            <div class="preveiw-slot" v-if="file_format == 'image'">
                <img :src="store.api + props.data.file">
            </div>
            <div class="preveiw-slot" v-else-if="file_format == 'video'">
                <video :src="store.api + props.data.file" controls autoplay></video>
            </div>
            <div v-else-if="file_format == 'file'">
                <p>Không thể xem trước tệp tin này</p>
            </div>
            <div class="preveiw-slot" v-else>
                <object :data="store.api + props.data.file" width="800" height="600">Không thể xem trước tệp tin này</object>
            </div>
        </div>
    </div>
</template>

<style scoped>
.preview {
    position: absolute;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    background-color: #040404df;
    z-index: 99;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.preveiw-header {
    width: 100%;
    height: 50px;
    background-color: #000000;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.preveiw-content {
    width: 100%;
    height: calc(100% - 60px);
    display: grid;
    place-items: center;
}

.preveiw-slot {
    width: 800px;
    height: 600px;
}

img, video {
    height: 100%;
    width: 100%;
    object-fit: contain;
}

.icon:hover {
    background-color: #666666;
}

h6, p {
    color: #ffffff;
}

.profile-img:hover {
    border: 1px solid var(--hover_color);
}

@media screen and (max-width: 800px) {
    .preveiw-slot {
        width: 100%;
    }
}
</style>