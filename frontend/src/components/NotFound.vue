<template>
  <div class="not-found">
    <img
      src="../assets/error.png"
      alt="404 Not Found"
      class="not-found-image"
    />
    <h2>Ой! Щось пішло не так...</h2>
    <p>Сторінку, яку ви шукаєте, не знайдено.</p>
    <router-link to="/" class="home-link">Повернутися на головну</router-link>
  </div>
</template>

<style scoped>
.not-found {
  text-align: center;
  margin: 50px;
  font-family: "Open Sans";
}

.not-found-image {
  max-width: 400px;
  width: 100%;
  height: auto;
}

h2 {
  font-size: 2rem;
  color: #333;
  margin-top: 20px;
}

p {
  font-size: 18px;
  color: #666;
}

.home-link {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 1rem;
  color: white;
  background-color: #007bff;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.home-link:hover {
  background-color: #0056b3;
}
</style>
