<template>
  <div class="test-container">
    <h1 class="test-title">Тестування англійської мови</h1>

    <section v-for="task in oneManyTasks" :key="task.id" class="task-container">
      <p class="task-text">{{ task.text }}</p>
      <div class="answer-buttons">
        <label
          v-for="(answer, index) in task.answers"
          :key="index"
          class="answer-label"
        >
          <input
            type="radio"
            :name="'question_' + task.id"
            :value="answer"
            v-model="selectedAnswers[task.id]"
            class="answer-radio"
          />
          {{ answer }}
        </label>
      </div>
    </section>

    <hr class="divider" />

    <section
      v-for="task in fixSentenceTasks"
      :key="task.id"
      class="task-container"
    >
      <p class="task-text">{{ task.bad_text }}</p>
      <textarea
        v-model="userAnswer[task.id]"
        class="answer-textarea"
        placeholder="Виправте помилку"
      ></textarea>
    </section>

    <button @click="checkAllAnswers" class="check-btn">
      Перевірити всі відповіді
    </button>
  </div>
</template>

<script>
import axios from "axios";
import { reactive } from "vue";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      oneManyTasks: [],
      fixSentenceTasks: [],
      userAnswer: reactive({}),
      selectedAnswers: reactive({}),
      score: null,
      totalQuestions: 0,
    };
  },
  methods: {
    async fetchTasks() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/test/");
        this.oneManyTasks = response.data.OneManyTask.map((task) => ({
          ...task,
          answers: [
            task.correct_answer,
            task.first_wrong_answer,
            task.second_wrong_answer,
            task.third_wrong_answer,
          ].sort(() => Math.random() - 0.5),
        }));
        this.fixSentenceTasks = response.data.FixSentenceTask;
        this.totalQuestions =
          this.oneManyTasks.length + this.fixSentenceTasks.length;
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    },
    checkAllAnswers() {
      let correctAnswers = 0;

      this.oneManyTasks.forEach((task) => {
        const selectedAnswer = this.selectedAnswers[task.id];
        if (selectedAnswer === task.correct_answer) {
          correctAnswers++;
        }
      });

      this.fixSentenceTasks.forEach((task) => {
        const userText = this.userAnswer[task.id];
        if (userText === task.correct_text) {
          correctAnswers++;
        }
      });

      this.score = correctAnswers;

      Swal.fire({
        title: "Ваш результат",
        text: `Правильних відповідей: ${this.score} з ${this.totalQuestions}`,
        icon: this.score === this.totalQuestions ? "success" : "error",
        showCancelButton: false,
        confirmButtonText: "Перейти до профілю",
      }).then(() => {
        this.$router.push("/profile-student");
      });
    },
  },
  mounted() {
    this.fetchTasks();
  },
};
</script>

<style scoped>
.test-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Arial", sans-serif;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.test-title {
  text-align: center;
  font-size: 2rem;
  color: #333;
  margin-bottom: 20px;
}

.task-text {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 10px;
}

.answer-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.answer-label {
  font-size: 1rem;
  color: #444;
  cursor: pointer;
}

.answer-radio {
  margin-right: 10px;
}

.answer-textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  min-height: 80px;
}

.check-btn {
  display: block;
  width: 100%;
  padding: 15px;
  background-color: #007bff;
  color: white;
  font-size: 1.2rem;
  text-align: center;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s ease;
}

.check-btn:hover {
  background-color: #0056b3;
}

.divider {
  margin: 20px 0;
  border: 0;
  border-top: 1px solid #ddd;
}
</style>
