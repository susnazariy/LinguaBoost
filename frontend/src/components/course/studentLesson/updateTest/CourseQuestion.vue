<template>
  <div class="center-test">
    <div class="child" v-if="!showResult">
      <component
        :is="currentComponent"
        :key="currentTask?.id"
        v-if="currentComponent && currentTask"
        :task-id="currentTask.id"
        @answerSelected="handleTaskCompletion"
      />
      <div class="button-container">
        <transition name="fade-scale">
          <button
            v-if="answerSelected && currentIndex < tasks.length - 1"
            @click="nextQuestion"
            class="next-btn"
          >
            Далі
          </button></transition
        >
      </div>
      <transition name="fade-scale">
        <button
          v-if="answerSelected && currentIndex === tasks.length - 1"
          @click="showResults"
          class="next-btn"
        >
          Завершити тест
        </button></transition
      >
    </div>

    <div v-else class="result">
      <div class="result-card">
        <h2 class="result-title">Тест завершено!</h2>
        <p class="result-message">Ви завершили всі завдання.</p>
        <p class="result-score">
          Ваш результат: <span class="score">{{ totalScore }}</span> з
          <span class="total">{{ totalQuestions }}</span>
        </p>
        <p
          class="result-status"
          :class="isSuccessfullyPassed ? 'success' : 'fail'"
        >
          {{
            isSuccessfullyPassed
              ? "Ви успішно склали тест! 🎉"
              : "Тест не складено. Спробуйте ще раз! ❌"
          }}
        </p>
        <button @click="$router.go(-1)" class="back-button">← Назад</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SelectOneManyTask from "./SelectOneManyTask.vue";
import SelectFixSentenceTask from "./SelectFixSentenceTask.vue";
import SelectTranslateWordTask from "./SelectTranslateWordTask.vue";
import SelectSequenceTask from "./SelectSequenceTask.vue";
import SelectAccordanceTask from "./SelectAccordanceTask.vue";

const componentsMap = {
  "Один із багатьох": "SelectOneManyTask",
  "Виправлення речень": "SelectFixSentenceTask",
  "Переклад слів": "SelectTranslateWordTask",
  Послідовність: "SelectSequenceTask",
  Відповідність: "SelectAccordanceTask",
};

export default {
  components: {
    SelectOneManyTask,
    SelectFixSentenceTask,
    SelectTranslateWordTask,
    SelectSequenceTask,
    SelectAccordanceTask,
  },
  data() {
    return {
      tasks: [],
      currentIndex: 0,
      results: [],
      answerSelected: false,
      showResult: false,
      isSuccessfullyPassed: false,
    };
  },
  computed: {
    currentTask() {
      return this.tasks[this.currentIndex] || null;
    },
    currentComponent() {
      return this.currentTask
        ? componentsMap[this.currentTask.category_name] || null
        : null;
    },
    totalScore() {
      return this.results.reduce((sum, result) => sum + result.correct, 0);
    },
    totalQuestions() {
      return this.results.reduce(
        (sum, result) => sum + result.correct + result.incorrect,
        0
      );
    },
  },
  methods: {
    async fetchCourseData() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/course_final_random_tasks_list/",
          { course_id: this.lessonId },
          { headers: { Authorization: `Token ${this.token}` } }
        );

        const categories = [];
        const categoryNameMap = {
          one_many_tasks_info: "Один із багатьох",
          fix_sentence_tasks_info: "Виправлення речень",
          translate_word_tasks_info: "Переклад слів",
          sequence_tasks_info: "Послідовність",
          accordance_tasks_info: "Відповідність",
        };

        Object.entries(response.data).forEach(([fieldName, tasks]) => {
          if (!Array.isArray(tasks)) return;

          const categoryName =
            categoryNameMap[fieldName] || "Невідома категорія";

          tasks.forEach((task) => {
            categories.push({
              id: task.id,
              category_name: categoryName,
              totalPairs: task.pairs ? task.pairs.length : 1,
            });
          });
        });

        this.tasks = categories;
      } catch (error) {
        console.error("❌ Помилка отримання завдань:", error);
      }
    },
    handleTaskCompletion({ correct, incorrect }) {
      this.results.push({ correct, incorrect });

      this.totalScore += correct;

      const currentTask = this.tasks[this.currentIndex];
      const taskCount =
        currentTask.category_name === "Відповідність"
          ? currentTask.totalPairs || 1
          : 1;

      this.totalQuestions += taskCount;

      this.answerSelected = true;
    },

    nextQuestion() {
      if (this.currentIndex < this.tasks.length - 1) {
        this.currentIndex++;
        this.answerSelected = false;
      }
    },
    showResults() {
      this.showResult = true;
      const correctAnswers = this.totalScore;
      const totalQuestions = this.totalQuestions;

      const isSuccessfullyPassed = correctAnswers >= totalQuestions / 2;

      this.isSuccessfullyPassed = isSuccessfullyPassed;

      const finalResults = {
        course_id: this.lessonId,
        test_result: correctAnswers,
        number_of_tests: totalQuestions,
        is_successfully_passed: isSuccessfullyPassed,
      };

      axios
        .post(
          "http://127.0.0.1:8000/add_course_final_test_result/",
          finalResults,
          {
            headers: { Authorization: `Token ${this.token}` },
          }
        )
        .then((response) => {
          console.log("✅ Результати успішно надіслані:", response.data);
        })
        .catch((error) => {
          console.error("❌ Помилка надсилання результатів:", error);
        });
    },
  },
  mounted() {
    this.lessonId = this.$route.params.id;
    this.token = this.$store.state.token;
    this.fetchCourseData();
  },
};
</script>

<style>
.back-button {
  margin-top: 15px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.back-button:hover {
  background-color: #0056b3;
}

.button-container {
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.5s ease;
}

.fade-scale-enter-from {
  opacity: 0;
  transform: scale(0.8);
}

.fade-scale-enter-to {
  opacity: 1;
  transform: scale(1);
}

.fade-scale-leave-from {
  opacity: 1;
  transform: scale(1);
}

.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

.next-btn {
  margin: 20px auto;
  display: flex;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}
.next-btn:hover {
  background-color: #0056b3;
}

.task-content {
  margin: 0 auto;
  padding: 20px 40px 0 40px;
  overflow-y: auto;
}
.task-content-container {
  margin-bottom: 20px;
}
.task-selection-container {
  display: flex;
  width: 1100px;
  margin: 0 auto;
  font-family: "Roboto", "Open Sans", sans-serif;
}

.sidebar {
  width: 350px;
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

.preview-image {
  max-width: 200px;
  margin-top: 10px;
  display: block;
  border-radius: 5px;
}

.task-selection-title {
  text-align: center;
  color: #2562e8;
  font-weight: 700;
  margin: 0;
}

.task-selection-label {
  font-size: 18px;
  font-weight: 500;
  display: block;
  margin-bottom: 10px;
}

.task-selection-dropdown {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #2562e8;
  border-radius: 5px;
  outline: none;
}

.task-selection-btn {
  display: block;
  width: 100%;
  padding: 12px;
  margin-top: 15px;
  background: #2562e8;
  color: #fff;
  font-size: 18px;
  font-weight: 500;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.task-selection-btn:hover {
  background: #1d4eb5;
}

.task-container {
  border-radius: 5px;
  background: #fff;
}
</style>
