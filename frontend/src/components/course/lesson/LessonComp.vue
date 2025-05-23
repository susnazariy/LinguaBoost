<template>
  <div class="lesson-container">
    <aside class="sidebar">
      <h2>Деталі заняття</h2>
      <ul>
        <li v-for="(lesson, key) in lessons" :key="key">
          <router-link :to="'/lesson/' + key" active-class="active-link">
            <i :class="'fas ' + icons[key]"></i>
            {{ lesson.title }}
          </router-link>
        </li>
      </ul>
    </aside>

    <main class="content">
      <div style="max-height: calc(80vh - 168px); overflow-y: auto">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      lessons: {
        category_1: {
          title: "Категорія 1",
          content: "Тут інформація про категорію 1",
        },
        category_2: {
          title: "Категорія 2",
          content: "Тут інформація про категорію 2",
        },
        category_3: {
          title: "Категорія 3",
          content: "Тут інформація про категорію 3",
        },
        test: { title: "Тестування", content: "Перевір свої знання!" },
      },
      icons: {
        category_1: "fa-book",
        category_2: "fa-chalkboard-teacher",
        category_3: "fa-graduation-cap",
        test: "fa-question-circle",
      },
    };
  },
};
</script>

<style scoped>
.lesson-container {
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
}
</style>
