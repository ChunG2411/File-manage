<script setup>
import { ref, watch, reactive, Transition } from 'vue'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'
import { useRoute, useRouter } from 'vue-router'

import Store from '../utils/store.js'
import Infor from './rightclick_comp/infor.vue'
import ChangeName from './rightclick_comp/name.vue'
import ChangeDes from './rightclick_comp/description.vue'
import Delete from './rightclick_comp/delete.vue'
import Move from './rightclick_comp/move/move.vue'
import Share from './rightclick_comp/share.vue'
import FilePreveiw from './filePreveiw.vue'
import Add from './rightclick_comp/add.vue'
import Preveiw from './preview/preveiw.vue'

import { differentDate, checkError } from '../utils/functions.js'


const store = Store()
const route = useRoute()
const router = useRouter()

var data_res = {}
const data = ref(null)
const right_card = ref(null)

const filter_ext = reactive({
    ext: '',
    label: ''
})
const filter_time = reactive({
    time: '',
    label: ''
})
const selected = ref([])

const right_click = reactive({
    status: false,
    data: null,
    type: ""
})
const showComp = reactive({
    type_com: '',
    id: '',
    type: ''
})
const showPreveiw = reactive({
    status: false,
    data: null
})


watch(() => store.reload, (newValue, _) => {
    if (newValue) {
        showComp.type_com = ''
        filter_ext.ext = ''
        filter_ext.label = ''
        filter_time.time = ''
        filter_time.label = ''
        selected.value = []
        removeSelect()
        getData(route.path)
    }
})
watch(() => route.path, (newId, oldId) => {
    showComp.type_com = ''
    filter_ext.ext = ''
    filter_ext.label = ''
    filter_time.time = ''
    filter_time.label = ''
    selected.value = []
    removeSelect()
    getData(newId)
})


watch(() => filter_ext.ext, (newValue, _) => {
    data.value = {...data_res}
    
    if (newValue == 'folder') {
        data.value.file = []
    }
    else if (newValue == 'file') {
        data.value.folder = []
    }
    else if (newValue == 'doc') {
        data.value.folder = []
        data.value.file = data.value.file.filter((item) => ['doc', 'docx', 'txt'].includes(item.file.split('.').at(-1)))
    }
    else if (newValue == 'xls') {
        data.value.folder = []
        data.value.file = data.value.file.filter((item) => ['xls', 'xlsx'].includes(item.file.split('.').at(-1)))
    }
    else if (newValue == 'png') {
        data.value.folder = []
        data.value.file = data.value.file.filter((item) => ['gif', 'jpeg', 'jpg', 'png'].includes(item.file.split('.').at(-1)))
    }
    else if (newValue == 'mp4') {
        data.value.folder = []
        data.value.file = data.value.file.filter((item) => ['mp4'].includes(item.file.split('.').at(-1)))
    }
    else if (newValue == 'ppt') {
        data.value.folder = []
        data.value.file = data.value.file.filter((item) => ['ppt', 'pptx'].includes(item.file.split('.').at(-1)))
    }
    else if (newValue == 'zip') {
        data.value.folder = []
        data.value.file = data.value.file.filter((item) => ['zip', 'rar'].includes(item.file.split('.').at(-1)))
    }
})
watch(() => filter_time.time, (newValue, _) => {
    data.value = {...data_res}

    if (newValue == 'now') {
        data.value.folder = data.value.folder.filter((item) => differentDate(item.update_at) == 0)
        data.value.file = data.value.file.filter((item) => differentDate(item.update_at) == 0)
    }
    else if (newValue == 'day') {
        data.value.folder = data.value.folder.filter((item) => differentDate(item.update_at) < 7)
        data.value.file = data.value.file.filter((item) => differentDate(item.update_at) < 7)
    }
    else if (newValue == 'month') {
        data.value.folder = data.value.folder.filter((item) => differentDate(item.update_at) < 30)
        data.value.file = data.value.file.filter((item) => differentDate(item.update_at) < 30)
    }
    else if (newValue == 'year') {
        data.value.folder = data.value.folder.filter((item) => differentDate(item.update_at) < 365)
        data.value.file = data.value.file.filter((item) => differentDate(item.update_at) < 365)
    }
})


async function getData(path) {
    store.loading = true

    await axios.get(`${store.api}/api${path}`, store.header)
        .then(response => {
            data_res = {...response.data}
            data.value = {...response.data}
            
            store.loading = false
            store.reload = false
        })
        .catch(error => {
            checkError(error)
        })
}
getData(route.path)


function getFolder(id) {
    right_click.status = false
    router.push({ name: 'card_folder', params: { id } })
}

function showMenu(event, type, data) {
    if (event.clientX + 190 > window.innerWidth) {
        right_card.value.style.left = (event.clientX - 170) + 'px'
    }
    else {
        right_card.value.style.left = event.clientX + 'px'
    }
    if (event.clientY + 230 > window.innerHeight) {
        right_card.value.style.top =( event.clientY - 230) + 'px'
    }
    else {
        right_card.value.style.top = event.clientY + 'px'
    }
    right_click.status = true
    right_click.data = data
    right_click.type = type
}

function closeMenu() {
    right_click.status = false
}

function showComponent(type) {
    showComp.type_com = type
    showComp.id = right_click.data.id
    showComp.type = right_click.type
    right_click.status = false
}

function showComponentAdd(type) {
    showComp.type_com = 'add'
    if (route.name == 'card_folder') {
        showComp.id = route.params.id
    }
    else {
        showComp.id = ''
    }   
    showComp.type = type
}

function showPreveiwFunc(data) {
    right_click.type = 'file'
    right_click.data = data
    showPreveiw.status = true
    showPreveiw.data = data
}

function DeleteFunc() {
    store.loading = true

    axios.delete(`${store.api}/api/${showComp.type}/${showComp.id}`, store.header)
        .then(response => {
            store.toast = {
                title: 'success',
                content: 'Xoá thành công'
            }
            store.loading = false
            store.reload = true
        })
        .catch(error => {
            checkError(error)
        })
}

function saveFunc() {
    store.loading = true

    axios.patch(`${store.api}/api/${right_click.type}/${right_click.data.id}/detail`, {}, store.header)
        .then(response => {
            store.toast = {
                title: 'success',
                content: 'Đã thêm dấu sao'
            }
            store.loading = false
        })
        .catch(error => {
            checkError(error)
        })
}

function downloadFile() {
    axios.get(`${store.api}/api/${right_click.type}/${right_click.data.id}/download`,
                {
                    responseType: 'blob',
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}`}
                })
        .then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', right_click.data.name)
            document.body.appendChild(link)
            link.click()

            store.toast = {
                title: 'info',
                content: 'Đang tải xuống'
            }
        })
        .catch(error => {
            checkError(error)
        })
}

function changeFilterExt(ext, label) {
    filter_time.time = ''
    filter_ext.ext = ext
    filter_ext.label = label
}
function changeFilterTime(time, label) {
    filter_ext.ext = ''
    filter_time.time = time
    filter_time.label = label
}

function selectItem(event, type, item) {
    if (event.currentTarget.classList.contains('item-selected')) {
        event.currentTarget.classList.remove('item-selected')
        selected.value = selected.value.filter(select => select.item.id !== item.id)
    }
    else {
        event.currentTarget.classList.add('item-selected')
        selected.value.push({
            type: type,
            item: item
        })
    }
}

function removeSelect() {
    selected.value = []
    document.querySelectorAll('.item-selected').forEach(item => {
        item.classList.remove('item-selected')
    })
}

function selectAll() {
    removeSelect()
    document.querySelectorAll('.item').forEach(item => {
        if (!item.classList.contains('item-selected')) {
            item.classList.add('item-selected')
        }
    })
    data.value.folder.forEach(item => {
        selected.value.push({
            type: 'folder',
            item: item
        })
    })
    data.value.file.forEach(item => {
        selected.value.push({
            type: 'file',
            item: item
        })
    })
}

function deleteSelect() {
    selected.value.forEach(item => {
        axios.delete(`${store.api}/api/${item.type}/${item.item.id}`, store.header)
            .then(response => {
                store.toast = {
                    title: 'success',
                    content: 'Xoá thành công'
                }
                store.reload = true
            })
            .catch(error => {
                checkError(error)
            })
    })
}

</script>


<template>
    <div class="card" v-if="data">
        <div class="c-header">
            <div>
                <div class="d-flex align-items-center">
                    <h5 class="path">{{ (data.path.length > 0) ? '...' :
                        route.params.type ? (route.params.type == 'saved') ? 'Có gắn dấu sao' :
                        (route.params.type == 'trash') ? 'Thùng rác' :
                        'Drive của tôi' : 'Drive của tôi'
                    }}</h5>
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
            <div class="d-flex gap-3 p-2 mt-2" v-if="selected.length > 0">
                <button class="btn btn-outline-primary" @click="selectAll">Chọn tất cả</button>
                <button @click="removeSelect">Bỏ chọn</button>
                <button class="btn btn-outline-danger" @click="deleteSelect">Xoá</button>
            </div>
            <div class="d-flex gap-3 p-2 mt-2" v-else>
                <div class="btn-drop">
                    <button>
                        <p>Thêm mới</p>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 20 20" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                            <path d="M6 9l6 6 6-6" />
                        </svg>
                    </button>
                    <div class="btn-drop-content">
                        <div class="btn-drop-item" @click="showComponentAdd('folder')">
                            <p>Thư mục</p>
                        </div>
                        <div class="btn-drop-item" @click="showComponentAdd('file')">
                            <p>Tệp</p>
                        </div>
                    </div>
                </div>
                <div class="btn-drop">
                    <button>
                        <p>{{ filter_ext.label ? filter_ext.label : 'Loại' }}</p>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 20 20" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round"
                            v-if="filter_ext.ext==''">
                            <path d="M6 9l6 6 6-6" />
                        </svg>
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 20 20" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            v-else @click="changeFilterExt('', 'Loại')">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                    <div class="btn-drop-content">
                        <div class="btn-drop-item" @click="changeFilterExt('folder', 'Thư mục')">
                            <p>Thư mục</p>
                        </div>
                        <div class="btn-drop-item" @click="changeFilterExt('file', 'Tệp')">
                            <p>Tệp</p>
                        </div>
                        <div class="btn-drop-item" @click="changeFilterExt('doc', 'Tài liệu')">
                            <p>Tài liệu</p>
                        </div>
                        <div class="btn-drop-item" @click="changeFilterExt('xls', 'Bảng tính')">
                            <p>Bảng tính</p>
                        </div>
                        <div class="btn-drop-item" @click="changeFilterExt('png', 'Ảnh')">
                            <p>Ảnh</p>
                        </div>
                        <div class="btn-drop-item" @click="changeFilterExt('mp4', 'Đoạn phim')">
                            <p>Đoạn phim</p>
                        </div>
                        <div class="btn-drop-item" @click="changeFilterExt('ppt', 'Trình bày')">
                            <p>Trình bày</p>
                        </div>
                        <div class="btn-drop-item" @click="changeFilterExt('zip', 'Tệp nén')">
                            <p>Tệp nén</p>
                        </div>
                    </div>
                </div>
                <div class="btn-drop">
                    <button>
                        <p>{{ filter_time.label ? filter_time.label : 'Gần đây' }}</p>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 20 20" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round"
                            v-if="filter_time.time==''">
                            <path d="M6 9l6 6 6-6" />
                        </svg>
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 20 20" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            v-else @click="changeFilterTime('', 'Gần đây')">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                    <div class="btn-drop-content">
                        <div class="btn-drop-item" @click="changeFilterTime('now', 'Hôm nay')">
                            <p>Hôm nay</p>
                        </div>
                        <div class="btn-drop-item" @click="changeFilterTime('day', '7 ngày')">
                            <p>7 ngày</p>
                        </div>
                        <div class="btn-drop-item" @click="changeFilterTime('month', '1 tháng')">
                            <p>1 tháng</p>
                        </div>
                        <div class="btn-drop-item" @click="changeFilterTime('year', '1 năm')">
                            <p>1 năm</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ---------------------------------------------------content--------------------------------------------------- -->
        <div class="card-content">
            <p class="mt-2 mb-2">Thư mục</p>
            <div class="list-item">
                <div class="item" v-for="(i, index) in data.folder" @dblclick="getFolder(i.id)"
                    @mouseup.right="showMenu($event, 'folder', i)" @click="selectItem($event, 'folder', i)">
                    <div class="item-header">
                        <div class="d-flex align-items-center position-relative">
                            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none"
                                stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z">
                                </path>
                            </svg>
                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none"
                                stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="position-absolute" style="bottom: 2px; left: 1px" v-if="i.permissions=='1'">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                <circle cx="12" cy="7" r="4"></circle>
                            </svg>
                        </div>
                        <p>{{ (i.name.length > 10) ? i.name.slice(0, 10) + '...' : i.name }}</p>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round"
                            @click="showMenu($event, 'folder', i)">
                            <circle cx="12" cy="12" r="1"></circle>
                            <circle cx="12" cy="5" r="1"></circle>
                            <circle cx="12" cy="19" r="1"></circle>
                        </svg>
                    </div>
                </div>
            </div>

            <p class="mt-4 mb-2">Tệp</p>
            <div class="list-item">
                <div class="item" v-for="(i, index) in data.file" @dblclick="showPreveiwFunc(i)"
                    @mouseup.right="showMenu($event, 'file', i)" @click="selectItem($event, 'file', i)">
                    <div class="item-header">
                        <div class="d-flex align-items-center position-relative">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round">
                                <path d="M13 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V9l-7-7z" />
                                <path d="M13 3v6h6" />
                            </svg>
                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none"
                                stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="position-absolute" style="bottom: 2px; left: 3px" v-if="i.permissions=='1'">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                <circle cx="12" cy="7" r="4"></circle>
                            </svg>
                        </div>
                        <p>{{ (i.name.length > 10) ? i.name.slice(0, 7) + '...' : i.name }}</p>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="#4f4f4f" stroke-width="2" stroke-linecap="square" stroke-linejoin="round"
                            @click="showMenu($event, 'file', i)">
                            <circle cx=" 12" cy="12" r="1"></circle>
                            <circle cx="12" cy="5" r="1"></circle>
                            <circle cx="12" cy="19" r="1"></circle>
                        </svg>
                    </div>
                    <FilePreveiw :src="i.file" :id="i.id"></FilePreveiw>
                </div>
            </div>
        </div>
    </div>

    <!-- --------------------------------------------right click------------------------------------------------------- -->
    <div class="rightclick" ref="right_card" v-on-click-outside="closeMenu" v-show="right_click.status">
        <div class="right-tab-1 item-right" @click="(right_click.type=='folder') ? getFolder(right_click.data.id) : showPreveiwFunc(right_click.data)">
            <p>Mở</p>
        </div>
        <div class="right-tab-1 item-right" @click="showComponent('infor')">
            <p>Xem thông tin</p>
        </div>
        <div class="right-tab-1 item-right">
            <p>Chỉnh sửa</p>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 18l6-6-6-6"/>
            </svg>
            <div class="right-tab-2">
                <div class="item-right" @click="showComponent('name')">
                    <p>Đổi tên</p>
                </div>
                <div class="item-right" @click="showComponent('description')">
                    <p>Thêm mô tả</p>
                </div>
            </div>
        </div>
        <div class="right-tab-1 item-right">
            <p>Sắp xếp</p>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 18l6-6-6-6"/>
            </svg>
            <div class="right-tab-2">
                <div class="item-right" @click="showComponent('move')">
                    <p>Di chuyển</p>
                </div>
                <div class="item-right" @click="saveFunc">
                    <p>Thêm dấu sao</p>
                </div>
            </div>
        </div>
        <div class="right-tab-1 item-right" @click="showComponent('delete')">
            <p v-if="right_click.data?.delete">Xoá</p>
            <p v-else>Chuyển vào thùng rác</p>
        </div>
        <div class="right-tab-1 item-right" v-if="right_click.type == 'file'" @click="downloadFile">
            <p>Tải xuống</p>
        </div>
        <div class="right-tab-1 item-right" @click="showComponent('share')">
            <p>Chia sẻ</p>
        </div>
    </div>

    <!-- --------------------------------------------components---------------------------------------------- -->
    <Transition name="infor">
        <Infor :type="showComp.type" :id="showComp.id" v-if="showComp.type_com == 'infor'">
            <div class="d-flex justify-content-between align-items-center">
                <h5>Chi tiết {{ (showComp.type == 'folder') ? 'thư mục' : 'tệp tin' }}</h5>
                <div class="icon rec-30" @click="showComp.type_com = ''">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </div>
            </div>
        </Infor>
    </Transition>

    <ChangeName :type="showComp.type" :id="showComp.id" v-if="showComp.type_com=='name'">
        <div class="d-flex justify-content-between align-items-center">
            <h5>Đổi tên {{ (showComp.type == 'folder') ? 'thư mục' : 'tệp tin' }}</h5>
            <div class="icon rec-30" @click="showComp.type_com = ''">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </div>
        </div>
    </ChangeName>

    <ChangeDes :type="showComp.type" :id="showComp.id" v-if="showComp.type_com=='description'">
        <div class="d-flex justify-content-between align-items-center">
            <h5>Mô tả {{ (showComp.type == 'folder') ? 'thư mục' : 'tệp tin' }}</h5>
            <div class="icon rec-30" @click="showComp.type_com = ''">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </div>
        </div>
    </ChangeDes>

    <Delete @close-func="showComp.type_com = ''" @submit-func="DeleteFunc" v-if="showComp.type_com=='delete'"></Delete>

    <Move :type="showComp.type" :id="showComp.id" v-if="showComp.type_com=='move'">
        <div class="d-flex justify-content-between align-items-center">
            <h5>Chọn đường dẫn</h5>
            <div class="icon rec-30" @click="showComp.type_com = ''">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </div>
        </div>
    </Move>

    <Share :type="showComp.type" :id="showComp.id" v-if="showComp.type_com=='share'">
        <div class="d-flex justify-content-between align-items-center">
            <h5>Chia sẻ {{ (showComp.type == 'folder') ? 'thư mục' : 'tệp tin' }}</h5>
            <div class="icon rec-30" @click="showComp.type_com = ''">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </div>
        </div>
    </Share>

    <Add :type="showComp.type" :id="showComp.id" v-if="showComp.type_com=='add'">
        <div class="d-flex justify-content-between align-items-center">
            <h5>Thêm mới {{ (showComp.type == 'folder') ? 'thư mục' : 'tệp tin' }}</h5>
            <div class="icon rec-30" @click="showComp.type_com = ''">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#4f4f4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </div>
        </div>
    </Add>

    <Preveiw :data="showPreveiw.data" :showClose="true" v-if="showPreveiw.status"
        @click-close="showPreveiw.status=false"
        @click-save="saveFunc"
        @click-download="downloadFile">
    </Preveiw>
</template>

<style scoped>
.card {
    background-color: var(--card_color);
    border-radius: 10px;
    padding: 10px;
    margin-top: 50px;
    width: 100%;
    height: calc(100% - 50px);
    border: 1px solid var(--card_border_color);
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
    flex-direction: column;
    align-items: center;
    gap: 10px;
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

.item-selected {
    background-color: var(--active_background_color);
}
.item-selected:hover {
    background-color: var(--active_background_color);
}

.item-header {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.rightclick {
    position: absolute;
    background-color: var(--card_color);
    border-radius: 10px;
    box-shadow: 0px 3px 5px 3px rgba(0, 0, 0, 0.1);
    z-index: 50;
    padding: 10px 0;
    width: max-content;
    height: max-content;
    display: flex;
    flex-direction: column;
    min-width: 170px;
}

.item-right {
    padding: 5px 15px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
}

.item-right:hover {
    background-color: var(--hover_color);
}

.right-tab-1:hover .right-tab-2{
    display: flex;
}

.right-tab-2 {
    display: none;
    position: absolute;
    background-color: var(--card_color);
    border-radius: 10px;
    box-shadow: 0px 3px 5px 3px rgba(0, 0, 0, 0.1);
    z-index: 50;
    padding: 10px 0;
    width: max-content;
    height: max-content;
    flex-direction: column;
    right: 100%;
    top: 0;
}


.infor-enter-active {
  transition: all 0.3s ease-in;
}

.infor-leave-active {
  transition: all 0.3s ease-out;
}

.infor-enter-from,
.infor-leave-to {
  margin-right: -350px;
}


@media screen and (max-width: 550px) {
    .item {
        min-width: 150px;
        max-width: 150px;
        padding: 8px 10px;
    }
    .card {
        height: calc(100% - 100px);
        max-height: calc(100% - 100px);
    }
    .card-content {
        padding: 5px;
    }
}
</style>