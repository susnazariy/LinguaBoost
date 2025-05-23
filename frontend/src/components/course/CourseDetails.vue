<template>
  <div class="course-page">
    <div class="border" v-if="courseData">
      <h2>{{ courseData.course_name }}</h2>

      <h3>Дані курсу:</h3>
      <p class="course__description">{{ courseData.course_description }}</p>
      <p>
        Кількість занять: <strong>{{ courseData.number_of_lessons }}</strong>
      </p>
      <p>
        Кількість тестових завдань:
        <strong>{{ courseData.number_of_tasks }}</strong>
      </p>
      <p>
        На даний момент вчиться учнів:
        <strong>{{ courseData.number_of_students }}</strong>
      </p>

      <div
        v-if="user_type === 'Учень' && access_course"
        class="container-tests"
      >
        <div v-if="courseData?.lessons_info && courseData.lessons_info.length">
          <h3>Інформація про заняття:</h3>
          <ul class="lessons-list">
            <li v-for="lesson in displayedLessons" :key="lesson.id">
              <router-link :to="`/lesson/${lesson.id}`">
                {{ lesson.lesson_name }}
              </router-link>
            </li>
          </ul>

          <button
            v-if="courseData.lessons_info.length > 3"
            @click="toggleShowMore"
            class="show-more-btn"
          >
            {{ showAll ? "Показати менше" : "Показати більше" }}
          </button>
        </div>

        <div>
          <div v-if="testResults.length" class="test-results">
            <h3 @click="toggleResults" class="toggle-header">
              Результати тесту
              <i
                :class="
                  isResultsVisible ? 'fas fa-chevron-up' : 'fas fa-chevron-down'
                "
              ></i>
            </h3>

            <transition name="fade-slide">
              <ul v-if="isResultsVisible">
                <li
                  v-for="(result, index) in formattedTestResults"
                  :key="index"
                >
                  <p>
                    <strong>Спроба {{ index + 1 }}</strong>
                  </p>
                  <p>
                    Результат тесту: {{ result.test_result }} /
                    {{ result.number_of_tests }}
                  </p>
                  <p>Дата: {{ result.formattedDate }}</p>
                </li>
              </ul>
            </transition>
          </div>

          <div v-if="access_course" class="page-container">
            <p class="lessons-list">
              <template
                v-if="passedLessons === numberLessons && numberLessons > 0"
              >
                <router-link :to="`/course-test/${taskId}`">
                  Пройти фінальне тестування
                </router-link>
              </template>
              <template v-else>
                <span class="warning-message">
                  Успішно пройдіть всі завдання уроків, щоб отримати доступ до
                  фінального тесту.
                </span>
              </template>
            </p>

            <div class="chart-container">
              <canvas ref="myChart"></canvas>
              <p v-if="numberLessons > 0">
                {{ passedLessons }} / {{ numberLessons }} занять пройдено ({{
                  percentage
                }}%)
              </p>
            </div>
          </div>
        </div>
      </div>

      <p v-if="user_type === 'None'">
        Авторизуйтесь, щоб отримати доступ до курсу
      </p>

      <button
        v-if="user_type === 'Учень' && !access_course"
        @click="sendFeedback"
        class="feedback-btn"
      >
        Отримати доступ до курсу
      </button>
    </div>

    <div v-else>
      <p class="error-message">Не вдалося отримати дані курсу.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

import { Chart, ArcElement, Tooltip, Legend, PieController } from "chart.js";

Chart.register(ArcElement, Tooltip, Legend, PieController);

export default {
  data() {
    return {
      taskId: this.$route.params.id,
      courseData: null,
      user_type: null,
      access_course: false,
      testResults: [],
      testPriv: [],
      showAll: false,
      isResultsVisible: false,
      passedLessons: 0,
      numberLessons: 0,
      percentage: null,
      token: this.$store.state.token,
    };
  },
  created() {
    this.fetchCourseData();
    this.fetchCourseFullData();
  },
  watch: {
    "$route.params.id": {
      handler(newId) {
        this.taskId = newId;
        this.fetchCourseData();
      },
      immediate: true,
    },
  },
  computed: {
    displayedLessons() {
      return this.showAll
        ? this.courseData.lessons_info
        : this.courseData.lessons_info.slice(0, 3);
    },
    formattedTestResults() {
      return this.testResults.map((result) => ({
        ...result,
        formattedDate: new Date(result.test_datetime).toLocaleString("uk-UA", {
          year: "numeric",
          month: "long",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        }),
      }));
    },
  },
  methods: {
    toggleResults() {
      this.isResultsVisible = !this.isResultsVisible;
    },
    toggleShowMore() {
      this.showAll = !this.showAll;
    },
    async sendFeedback() {
      const feedbackData = {
        course_id: this.taskId,
      };

      const token = this.$store.state.token;
      this.token = this.$store.state.token;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/add_student_application/",
          feedbackData,
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );

        if (response.data === "Student application successfully added!") {
          Swal.fire({
            title: "Успіх!",
            text: "Запит на доступ до курсу успішно відправлено!",
            icon: "success",
            confirmButtonText: "Гаразд",
          });
        } else if (
          response.data === "You have already send application for this course!"
        ) {
          Swal.fire({
            title: "Помилка!",
            text: "Ви вже відправили запит на даний курс.",
            icon: "error",
            confirmButtonText: "ОК",
          });
        } else {
          throw new Error("Неочікувана відповідь сервера");
        }
      } catch (error) {
        console.error("Помилка під час надсилання запиту:", error);

        Swal.fire({
          title: "Помилка!",
          text: "Щось пішло не так. Спробуйте ще раз.",
          icon: "error",
          confirmButtonText: "ОК",
        });
      }
    },
    async fetchCourseData() {
      try {
        const { data } = await axios.post(
          "http://127.0.0.1:8000/course_and_lessons_data/",
          { course_id: this.taskId },
          {
            headers: this.token ? { Authorization: `Token ${this.token}` } : {},
          }
        );

        this.courseData = data;

        this.user_type = this.courseData.user_type;
        this.access_course = this.courseData.access_course || false;
      } catch (error) {
        console.error("Помилка отримання даних:", error);
      }
    },
    async fetchCourseFullData() {
      try {
        const { data } = await axios.post(
          "http://127.0.0.1:8000/course_data_and_final_test_results/",
          { course_id: this.taskId },
          {
            headers: this.token ? { Authorization: `Token ${this.token}` } : {},
          }
        );

        this.testResults = data.course_test_results;

        this.testPriv = data.tests_info;
        console.log(this.testPriv);

        this.numberLessons = this.testPriv.number_of_tests;
        this.passedLessons = this.testPriv.number_of_passed_tests;

        this.calculatePercentage();

        this.$nextTick(() => {
          if (this.numberLessons > 0) this.loadChart();
        });
      } catch (error) {
        console.error("Помилка отримання даних:", error);
      }
    },
    calculatePercentage() {
      this.percentage = this.numberLessons
        ? Math.round((this.passedLessons / this.numberLessons) * 100)
        : 0;
    },
    loadChart() {
      if (!this.$refs.myChart || !this.numberLessons) return;

      const ctx = this.$refs.myChart.getContext("2d");

      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      this.chartInstance = new Chart(ctx, {
        type: "pie",
        data: {
          labels: ["Пройдено", "Залишилось"],
          datasets: [
            {
              data: [
                this.passedLessons,
                this.numberLessons - this.passedLessons,
              ],

              backgroundColor: ["#4caf50", "#f44336"],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: "top" },
            tooltip: {
              callbacks: {
                label: (tooltipItem) => {
                  const value = tooltipItem.raw;
                  const percent = Math.round(
                    (value / this.numberLessons) * 100
                  );
                  return `${tooltipItem.label}: ${value} (${percent}%)`;
                },
              },
            },
          },
        },
      });
    },
  },
};
</script>

<style scoped>
.toggle-header,
h3 {
  text-align: center;
}
.container-tests {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.container-tests div {
  width: 350px;
}
.container-tests .page-container .chart-container {
  width: 250px;
  margin: 0 auto;
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

.warning-message {
  text-align: center;
  color: red;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  font-size: 14px;
}
.show-more-btn {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
}

.show-more-btn:hover {
  background-color: #45a049;
}
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Open+Sans:wght@400;600&display=swap");

.course__description {
  text-align: justify;
  line-height: 25px;
  font-family: "Open Sans", sans-serif;
}

.course-page {
  width: 1100px;
  margin: 40px auto;
}

h2 {
  font-size: 28px;
  text-align: center;
  color: #333;
  font-family: "Roboto", sans-serif;
}

h3 {
  font-size: 22px;
  margin-top: 20px;
  color: #555;
  font-family: "Roboto", sans-serif;
}

p {
  font-size: 18px;
  margin: 10px 0;
  color: #444;
  font-family: "Open Sans", sans-serif;
}

.strong {
  font-weight: bold;
}

.lessons-list {
  list-style-type: none;
  padding: 0;
  text-align: center;
  margin-bottom: 40px;
}

.lessons-list li {
  margin: 8px 0;
  font-size: 18px;
  line-height: 25px;
  color: #444;
  font-family: "Open Sans", sans-serif;
}

.lessons-list a {
  text-decoration: none;
  font-size: 18px;
  color: #007bff;
  font-family: "Open Sans", sans-serif;
}

.lessons-list a:hover {
  text-decoration: underline;
  color: #0056b3;
}

.feedback-btn {
  display: block;
  width: 100%;
  max-width: 300px;
  margin: 20px auto;
  padding: 12px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 18px;
  text-align: center;
  font-family: "Open Sans", sans-serif;
}

.feedback-btn:hover {
  background-color: #0054ae;
}

.error-message {
  text-align: center;
  color: red;
  font-size: 18px;
  font-family: "Open Sans", sans-serif;
}
</style>
