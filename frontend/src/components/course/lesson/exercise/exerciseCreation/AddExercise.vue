<template>
  <div class="exercise-container">
    <aside class="sidebar">
      <h2>Додати вправу</h2>
      <ul>
        <li v-for="(exercise, key) in exercises" :key="key">
          <router-link
            :to="`/add-exercise/${lessonId}/${key}`"
            :class="{ 'active-link': $route.path.includes(key) }"
          >
            <i :class="'fas ' + icons[key]"></i>
            {{ exercise.title }}
          </router-link>
        </li>
      </ul>
    </aside>

    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      exercises: {
        warm_up: { title: "Обговорення" },
        listening: { title: "Аудіювання" },
        reading: { title: "Читання" },
        rules: { title: "Правила" },
        vocabulary: { title: "Словниковий запас" },
      },
      icons: {
        warm_up: "fa-running",
        listening: "fa-headphones",
        reading: "fa-book",
        rules: "fa-scroll",
        vocabulary: "fa-font",
      },
    };
  },
  computed: {
    lessonId() {
      return this.$route.params.id;
    },
  },
};
</script>

<style scoped>
.exercise-container {
  display: flex;
  width: 1100px;
  margin: 0 auto;
  font-family: "Roboto", "Open Sans", sans-serif;
}

.sidebar {
  width: 250px;
  background: #f4f4f4;
  padding: 20px;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 80vh;
  overflow-y: auto;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  margin-bottom: 10px;
}

.sidebar a {
  text-decoration: none;
  color: black;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 5px;
  transition: background 0.3s ease-in-out;
  cursor: pointer;
}

.sidebar a.active-link {
  background: #007bff;
  color: white;
}

.sidebar i {
  font-size: 18px;
}

.content {
  flex: 1;
  padding: 20px;
  background: #ffffff;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  height: 80vh;
  overflow-y: auto;
}
</style>
