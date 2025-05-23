<template>
  <div class="lesson-container">
    <div v-if="categories.length === 0" class="no-tasks">
      <img src="../../../../assets/nothing.webp" class="no-image" />
      <p>Вправ немає.</p>
      <router-link :to="`/add-exercise/${courseId}`">
        <i class="fas fa-plus-circle"></i> Додати вправу
      </router-link>
    </div>

    <div v-else>
      <h3>Список вправ</h3>

      <div
        v-for="category in categories"
        :key="category.id"
        class="category-item"
      >
        <div class="category-info">
          <input
            v-model="category.id"
            type="number"
            disabled
            class="category-id"
          />
          <input
            v-model="category.category_name"
            type="text"
            class="category-name"
            disabled
          />
        </div>
        <div class="actions">
          <router-link
            :to="`/update-exercise/${convertToKey(category.category_name)}-${
              category.id
            }`"
            class="edit-link"
          >
            <i class="fas fa-pencil-alt"></i> Редагувати
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      token: "",
      courseId: null,
      categories: [],
    };
  },
  computed: {
    ...mapGetters(["isAuthenticated"]),
  },
  async mounted() {
    this.token = this.$store.state.token;
    this.courseId = this.$route.params.id;
    if (!this.courseId) return;
    await this.fetchCourseData();
  },
  methods: {
    convertToKey(categoryName) {
      const categoryMap = {
        Обговорення: "discussion_exercises_info",
        Аудіювання: "listening_exercises_info",
        Читання: "reading_exercises_info",
        Правила: "rules_exercises_info",
        "Словниковий запас": "vocabulary_exercises_info",
      };
      return categoryMap[categoryName] || "unknown_task";
    },
    async fetchCourseData() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/exercises_list/",
          { lesson_id: this.courseId },
          { headers: { Authorization: `Token ${this.token}` } }
        );

        const categories = [];

        Object.entries(response.data).forEach(([, taskGroup]) => {
          if (typeof taskGroup !== "object" || taskGroup === null) {
            console.error(
              `❌ Помилка: taskGroup має некоректний формат`,
              taskGroup
            );
            return;
          }

          Object.entries(taskGroup).forEach(([fieldName, tasks]) => {
            if (!Array.isArray(tasks)) return;

            const categoryNameMap = {
              discussion_exercises_info: "Обговорення",
              listening_exercises_info: "Аудіювання",
              reading_exercises_info: "Читання",
              rules_exercises_info: "Правила",
              vocabulary_exercises_info: "Словниковий запас",
            };

            const categoryName =
              categoryNameMap[fieldName] || "Невідома категорія";

            tasks.forEach((task) => {
              categories.push({
                id: task.id,
                category_name: categoryName,
              });
            });
          });
        });

        this.categories = categories;
      } catch (error) {
        console.error("❌ Помилка при отриманні даних:", error);
      }
    },
  },
};
</script>

<style scoped>
.no-tasks {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.no-tasks a {
  text-decoration: none;
  background: #007bff;
  color: white;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 5px;
  transition: background 0.3s ease-in-out;
  cursor: pointer;
}

.no-tasks a:hover {
  color: black;
  background: white;
}
.no-image {
  width: 300px;
  height: 300px;
  object-fit: cover;
  transform: scale(1.3);
}
.lesson-container {
  box-sizing: border-box;
  width: 740px;
  margin: 20px auto;
  padding: 15px;
  background: #fff;
  border-radius: 12px;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background 0.3s ease;
}

.category-item:hover {
  background: #e8f0fe;
}

.category-info {
  gap: 30px;
  display: flex;
}

.category-id {
  width: 60px;
  font-size: 14px;
  border: 1px solid #ddd;
  padding: 8px;
  background-color: #f1f1f1;
  border-radius: 6px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.category-name {
  flex-grow: 1;
  font-size: 14px;
  border: 1px solid #ddd;
  padding: 8px;
  background-color: #f1f1f1;
  border-radius: 6px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  font-weight: bold;
  color: #333;
}

.category-name {
  font-weight: bold;
  color: #333;
}

.actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
}

.edit-link {
  background: #3498db;
  color: white;
  padding: 8px 15px;
  text-decoration: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  transition: background-color 0.3s;
}

.edit-link:hover {
  background: #2980b9;
}

.edit-link i {
  margin-right: 8px;
}
</style>
