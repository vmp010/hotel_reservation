<template>
    <h1>房型瀏覽--我想要做成下面圖片的樣子</h1>
    <img src="/homeView_I_want.png"></img>
</template>
<script setup>
// 中介軟體：auth.ts 判斷是否登入
definePageMeta({
  middleware: 'auth'
})
</script>
<style scoped>
img{
    height: 50%;
    width: 50%;
}
</style>