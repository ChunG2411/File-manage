<script setup>
</script>

<template>
    <div class="delete">
        <div>
            <h5>Xoá</h5>
            <p class="mt-1">Bạn chắc chắn muốn xoá?</p>
            <div class="d-flex gap-2 justify-content-end mt-3">
                <button class="btn btn-outline-danger" @click="$emit('close-func')">Huỷ</button>
                <button class="btn btn-primary" @click="$emit('submit-func')">Xác nhận</button>
            </div>
        </div>
    </div>
</template>

<style scope>
.delete {
    position: absolute;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    background-color: var(--card_background_color);
    z-index: 50;
    display: grid;
    place-items: center;
}

.delete > div {
    min-width: 300px;
    padding: 20px;
    width: max-content;
    height: max-content;
    border-radius: 10px;
    background-color: var(--card_color);
}
</style>