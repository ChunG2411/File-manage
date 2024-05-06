<script setup>
import Header from '../components/header.vue'
import Navbar from '../components/navbar.vue'
import Card from '../components/card.vue'


</script>

<template>
    <Header />
    <div class="main-content">
        <Navbar />
        <Card />
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