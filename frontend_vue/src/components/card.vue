<script setup>
import { ref, watch, reactive } from 'vue'
import axios from 'axios'
import { onClickOutside } from '@vueuse/core'
import { vOnClickOutside } from '@vueuse/components'

import Store from '../utils/store.js'
import Infor from './infor.vue'


const store = Store()
const data = ref(null)
const right_click = reactive({
    status: false,
    id: "",
    type: ""
})
const showComp = reactive({
    type_com: '',
    id: '',
    type: ''
})


watch(() => store.component.url, (newValue, _) => {
    getData()
})

function getData() {
    store.loading = true

    axios.get(`${store.api}/api/${store.component.url}`, store.header)
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

getData()

function getFolder(id) {
    store.component.url = `folder/${id}`
}

function showMenu(event, type, id) {
    const element = document.querySelector('.rightclick')
    element.style.left = event.clientX + 'px'
    element.style.top = event.clientY + 'px'
    right_click.status = true
    right_click.id = id
    right_click.type = type
}

function closeMenu() {
    right_click.status = false
}

function showComponent(type) {
    showComp.type_com = type
    showComp.id = right_click.id
    showComp.type = right_click.type
}

</script>


<template>
    <div class="rightclick" v-on-click-outside="closeMenu" v-show="right_click.status">
        <div @click="showComponent('infor')">
            <p>Xem thông tin</p>
        </div>
        <div>
            <p>Di chuyển</p>
        </div>
        <div>
            <p>Đổi tên</p>
        </div>
        <div>
            <p>Xoá</p>
        </div>
        <div>
            <p>Chia sẻ</p>
        </div>
    </div>
    <Infor :type="showComp.type" :id="showComp.id" v-if="showComp.type_com == 'infor'"></Infor>


    <div class="card" v-if="data">
        <div class="c-header">
            <div>
                <div class="d-flex align-items-center">
                    <h5 class="path">{{ (data.path.length > 0) ? '...' : store.component.title }}</h5>
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                        <path d="M9 18l6-6-6-6" />
                    </svg>
                    <template v-if="data.path.length > 2">
                        <h5 class="path">...</h5>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                            <path d="M9 18l6-6-6-6" />
                        </svg>
                    </template>
                    <template v-for="(i, index) in data.path.slice(data.path.length - 2)">
                        <h5 class="path" @click="getFolder(i[1])">{{ (i[0].length > 8) ? i[0].slice(0, 8) + '...' : i[0]
                            }}</h5>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                            <path d="M9 18l6-6-6-6" />
                        </svg>
                    </template>
                </div>
                <div>
                    <!-- icon -->
                </div>
            </div>
            <div class="d-flex gap-3 p-2 mt-2">
                <button>
                    <p>Loại</p>
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 20 20" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                        <path d="M6 9l6 6 6-6" />
                    </svg>
                </button>
                <button>
                    <p>Lần sửa đổi gần đây</p>
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 20 20" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                        <path d="M6 9l6 6 6-6" />
                    </svg>
                </button>
            </div>
        </div>
        <div class="card-content">
            <p class="mt-2 mb-2">Thư mục</p>
            <div class="list-item">
                <div class="item" v-for="(i, index) in data.folder" @dblclick="getFolder(i.id)"
                    @mouseup.right="showMenu($event, 'folder', i.id)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z">
                        </path>
                    </svg>
                    <p>{{ (i.name.length > 10) ? i.name.slice(0, 10) + '...' : i.name }}</p>
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round"
                        @click="showMenu($event, 'folder', i.id)">
                        <circle cx="12" cy="12" r="1"></circle>
                        <circle cx="12" cy="5" r="1"></circle>
                        <circle cx="12" cy="19" r="1"></circle>
                    </svg>
                </div>
            </div>

            <p class="mt-4 mb-2">Tệp</p>
            <div class="list-item">
                <div class="item" v-for="(i, index) in data.file" @mouseup.right="showMenu($event, 'file', i.id)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                        <path d="M13 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V9l-7-7z" />
                        <path d="M13 3v6h6" />
                    </svg>
                    <p>{{ (i.name.length > 10) ? i.name.slice(0, 10) + '...' : i.name }}</p>
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round"
                        @click="showMenu($event, 'file', i.id)">
                        <circle cx=" 12" cy="12" r="1"></circle>
                        <circle cx="12" cy="5" r="1"></circle>
                        <circle cx="12" cy="19" r="1"></circle>
                    </svg>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.card {
    background-color: var(--card_color);
    border-radius: 10px;
    padding: 10px;
    margin-top: 50px;
    width: 100%;
}

.card-content {
    width: 100%;
    overflow-y: auto;
    padding: 10px;
}

.list-item {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
}

.item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 15px;
    background-color: var(--item_color);
    cursor: pointer;
    min-width: 200px;
    max-width: 200px;
    border-radius: 10px;
    flex: 1 0 auto;
}

.item:hover {
    background-color: var(--hover_color);
}

.rightclick {
    position: absolute;
    background-color: var(--card_color);
    border-radius: 10px;
    box-shadow: 0px 3px 5px 3px rgba(0, 0, 0, 0.1);
    z-index: 50;
    padding: 5px;
    width: max-content;
    height: max-content;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.rightclick>div {
    padding: 5px 15px;
    border-radius: 5px;
    display: flex;
    gap: 10px;
    align-items: center;
}

.rightclick>div:hover {
    background-color: var(--hover_color);
}
</style>