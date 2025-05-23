<template>
  <div class="edit-course-container">
    <aside class="sidebar">
      <h2>Меню</h2>
      <ul>
        <li>
          <router-link
            :to="`/change-course/${courseId}/edit`"
            class="active-link"
          >
            <i class="fas fa-clipboard-list"></i> Список вправ
          </router-link>
        </li>
        <li>
          <router-link :to="`/add-exercise/${lessonId}`">
            <i class="fas fa-plus-circle"></i> Додати вправу
          </router-link>
        </li>
      </ul>
    </aside>
    <main class="edit-course-content">
      <TaskList :lesson-id="lessonId" />
    </main>
  </div>
</template>

<script>
import TaskList from "./TaskList.vue";

export default {
  components: {
    TaskList,
  },
  computed: {
    lessonId() {
      return this.$route.params.id;
    },
  },
};
</script>

<style scoped>
.edit-course-content {
  height: 84vh;

  overflow-y: auto;
}
.edit-course-container {
  display: flex;
  width: 1100px;
  margin: 0 auto;
  font-family: "Roboto", "Open Sans", sans-serif;
}

.sidebar {
  width: 300px;
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
</style>
