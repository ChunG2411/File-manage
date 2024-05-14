<script setup>
import Header from '../components/header.vue'
import Navbar from '../components/navbar.vue'
import Upload from '../components/upload.vue'

import { useRouter } from 'vue-router'

const router = useRouter()
router.push({name: 'card'})

</script>

<template>
    <Header />
    <div class="main-content">
        <Navbar />
        <router-view></router-view>
        <Upload />
    </div>
</template>

<style scoped>
.main-content {
    display: flex;
    gap: 15px;
    width: 100%;
    height: 100%;
    padding: 10px;
    overflow: hidden;
}
</style>