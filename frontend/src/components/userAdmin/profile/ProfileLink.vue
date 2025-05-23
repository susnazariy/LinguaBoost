<template>
  <div class="admin-greeting">
    <h1>Ласкаво просимо!</h1>
    <p>
      Перейдіть до
      <a href="http://127.0.0.1:8000/admin/" target="_blank">адмін-панелі</a>
    </p>
  </div>
</template>

<script>
export default {
  name: "AdminGreeting",
};
</script>

<style scoped>
.admin-greeting {
  text-align: center;
  margin-top: 50px;
}
.admin-greeting a {
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
}
.admin-greeting a:hover {
  text-decoration: underline;
}
</style>
