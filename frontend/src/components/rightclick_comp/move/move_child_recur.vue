<script setup>
import { defineProps } from 'vue'

import Child from './move_child.vue'


const props = defineProps({
    url: String,
    id: String,
    type: String
})


</script>

<template>
    <Child :type="props.type" :id="props.id" :url="props.url"></Child>
</template>

<style scope>
</style>