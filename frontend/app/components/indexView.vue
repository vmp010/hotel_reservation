<template>
    <section class="py-5">
      <div class="container">
        <h2 class="mb-4 fw-bold">熱門房型</h2>
        <div class="row g-4">
          <div class="col-md-4" v-for="room in rooms" :key="room.id">
            <div class="card shadow-sm">
              <img :src="room.image" class="card-img-top" :alt="room.name" />
              <div class="card-body">
                <h5 class="card-title">{{ room.name }}</h5>
                <p class="card-text text-muted">{{ room.location }}</p>
                <p class="fw-bold text-primary">$ {{ room.price }} / 晚</p>
                <a href="#" class="btn btn-outline-primary w-100">查看詳情</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
</template>
<script setup>
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
];
</script>