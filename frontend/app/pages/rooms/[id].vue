<template>
  <div class="container py-5">
    <NuxtLink to="/" class="btn btn-secondary mt-3"><i class="bi bi-arrow-left">返回</i></NuxtLink>
    <h1>{{ room.name }}</h1>
    <img :src="room.image" class="img-fluid rounded mb-3" alt="">
    <p>地點：{{ room.location }}</p>
    <p>價格：${{ room.price }} / 晚</p>
    <p>地點：{{ room.location }}</p>

    
  </div>
</template>

<script setup>
const route = useRoute()

// 模擬房型資料，可之後改成用 API 或 @nuxt/content 取得
const rooms = [
  {
    id: 1,
    name: '豪華雙人房',
    location: '台北市中正區',
    price: 3200,
    image: 'https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=800&q=80',
  },
  {
    id: 2,
    name: '海景套房',
    location: '高雄市鼓山區',
    price: 4500,
    image: 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80',
  },
  {
    id: 3,
    name: '家庭四人房',
    location: '台中市西屯區',
    price: 5000,
    image: 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80',
  },
]

// 根據網址 id 找出對應房型
const room = rooms.find(r => r.id === Number(route.params.id))
</script>