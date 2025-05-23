<template>
  <div class="edit-course-container">
    <aside class="sidebar">
      <h3>Список вправ</h3>
      <div
        v-for="category in categories"
        :key="category.id"
        class="category-item"
        :class="{ 'active-category': selectedCategory === category.key }"
        @click="selectTask(category)"
      >
        <i :class="category.icon"></i>
        <span>{{ category.id }}</span>
        <span>{{ category.category_name }}</span>
      </div>

      <router-link :to="'/test/' + courseId" class="test-link">
        <i class="fas fa-play"></i> Тести
      </router-link>
      <div v-if="testResults.length > 0" class="test-results">
        <h3 @click="toggleResults" class="toggle-header">
          Результати тесту
          <i
            :class="
              isResultsVisible ? 'fas fa-chevron-up' : 'fas fa-chevron-down'
            "
          ></i>
        </h3>
        <transition name="fade-slide"
          ><ul v-show="isResultsVisible">
            <li v-for="(result, index) in formattedTestResults" :key="index">
              <p>
                <strong>Спроба {{ index + 1 }}</strong>
              </p>
              <p>
                Результат тесту: {{ result.test_result }} /
                {{ result.number_of_tests }}
              </p>
              <p>Дата: {{ result.formattedDate }}</p>
              <p v-if="result.is_successfully_passed === false">
                Тест не пройдено
              </p>
              <p v-else>Тест успішно пройдено</p>
            </li>
          </ul></transition
        >
      </div>
    </aside>

    <main class="edit-course-content">
      <TaskEditor :category="selectedCategory" :id="selectedTaskId" />
    </main>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
import TaskEditor from "./updateExercise/UpdateExercise.vue";

export default {
  components: {
    TaskEditor,
  },
  data() {
    return {
      token: "",
      courseId: null,
      categories: [],
      selectedCategory: null,
      selectedTaskId: null,
      testResults: [],
      isResultsVisible: false,
    };
  },
  computed: {
    ...mapGetters(["isAuthenticated"]),
    formattedTestResults() {
      return this.testResults.map((result) => {
        return {
          ...result,
          formattedDate: new Date(result.test_datetime).toLocaleString(
            "uk-UA",
            {
              year: "numeric",
              month: "long",
              day: "numeric",
              hour: "2-digit",
              minute: "2-digit",
              second: "2-digit",
            }
          ),
        };
      });
    },
  },
  async mounted() {
    this.token = this.$store.state.token;
    this.courseId = this.$route.params.id;
    if (!this.courseId) return;
    await this.fetchCourseData();
    await this.fetchTestResults();
  },
  methods: {
    toggleResults() {
      this.isResultsVisible = !this.isResultsVisible;
    },
    selectTask(category) {
      this.selectedCategory = category.key;
      this.selectedTaskId = category.id;
    },
    async fetchCourseData() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/exercises_list/",
          { lesson_id: this.courseId },
          { headers: { Authorization: `Token ${this.token}` } }
        );

        const categoryMap = {
          discussion_exercises_info: {
            name: "Обговорення",
            icon: "fas fa-comments",
          },
          listening_exercises_info: {
            name: "Аудіювання",
            icon: "fas fa-headphones",
          },
          reading_exercises_info: { name: "Читання", icon: "fas fa-book-open" },
          rules_exercises_info: { name: "Правила", icon: "fas fa-cogs" },
          vocabulary_exercises_info: {
            name: "Словниковий запас",
            icon: "fas fa-book",
          },
        };

        const categories = [];
        Object.entries(response.data).forEach(([, taskGroup]) => {
          if (typeof taskGroup !== "object" || taskGroup === null) return;

          Object.entries(taskGroup).forEach(([fieldName, tasks]) => {
            if (!Array.isArray(tasks)) return;

            const categoryInfo = categoryMap[fieldName] || {
              name: "Невідома категорія",
              icon: "fas fa-question",
            };

            tasks.forEach((task) => {
              categories.push({
                id: task.id,
                category_name: categoryInfo.name,
                icon: categoryInfo.icon,
                key: fieldName,
              });
            });
          });
        });

        this.categories = categories;
      } catch (error) {
        console.error("❌ Помилка при отриманні даних:", error);
      }
    },

    async fetchTestResults() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/lesson_test_results/",
          { lesson_id: this.courseId },
          { headers: { Authorization: `Token ${this.token}` } }
        );

        this.testResults = response.data;
      } catch (error) {
        console.error("❌ Помилка при отриманні результатів тесту:", error);
      }
    },
  },
};
</script>

<style scoped>
.test-link {
  margin-top: 40px;
}
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.5s ease;
  overflow: hidden;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}

.fade-slide-enter-to,
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
  max-height: 500px;
}
.active-category {
  background: #007bff;
  color: white;
  font-weight: bold;
}

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

h3 {
  margin-bottom: 15px;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease-in-out;
}

.category-item:hover {
  background: #e0e0e0;
}

.sidebar i {
  font-size: 18px;
  width: 24px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
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
</style>
