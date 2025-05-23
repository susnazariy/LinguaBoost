<template>
  <div class="test-container">
    <h3 v-if="task" class="task-title">Завдання</h3>

    <div v-if="task" class="task-content">
      <p class="sentence">{{ formattedSentence(task.text) }}</p>

      <div class="answer-options">
        <button
          v-for="(answer, index) in shuffledAnswers"
          :key="index"
          @click="handleAnswer(answer)"
          :class="{
            correct: selectedAnswer && answer === task.correct_answer,
            wrong: selectedAnswer && answer !== task.correct_answer,
          }"
          :disabled="selectedAnswer"
        >
          {{ answer }}
        </button>
      </div>
    </div>

    <p v-else>Завантаження завдання...</p>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  props: {
    taskId: Number,
  },

  data() {
    return {
      task: null,
      shuffledAnswers: [],
      selectedAnswer: null,
    };
  },

  watch: {
    taskId: {
      handler() {
        this.fetchTask();
      },
      immediate: true,
    },
  },

  methods: {
    async fetchTask() {
      try {
        const token = this.$store.state.token;
        const response = await axios.post(
          "http://127.0.0.1:8000/selected_one_many_task_data/",
          { one_many_task_id: this.taskId },
          { headers: { Authorization: `Token ${token}` } }
        );

        this.task = response.data[0];
        this.shuffleAnswers();
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося завантажити завдання", "error");
        console.error("Помилка отримання завдання:", error);
      }
    },

    shuffleAnswers() {
      if (!this.task) return;

      const answers = [
        this.task.correct_answer,
        this.task.first_wrong_answer,
        this.task.second_wrong_answer,
        this.task.third_wrong_answer,
      ];

      this.shuffledAnswers = answers.sort(() => Math.random() - 0.5);
    },

    handleAnswer(answer) {
      if (this.selectedAnswer) return;

      if (!answer) {
        Swal.fire(
          "Помилка",
          "Будь ласка, виберіть відповідь перед продовженням.",
          "warning"
        );
        return;
      }

      this.selectedAnswer = answer;
      const isCorrect = answer === this.task.correct_answer;

      this.$emit("answerSelected", {
        correct: isCorrect ? 1 : 0,
        incorrect: isCorrect ? 0 : 1,
      });
    },

    formattedSentence(sentence) {
      return sentence.replace("&&", "_____");
    },
  },
};
</script>

<style scoped>
.test-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.task-title {
  font-size: 22px;
  color: #2562e8;
  font-weight: bold;
}

.sentence {
  font-size: 18px;
  margin: 20px 0;
}

.answer-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

button {
  padding: 12px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.correct {
  background: #28a745;
  color: white;
}

.wrong {
  background: #dc3545;
  color: white;
}

.next-btn {
  margin-top: 20px;
  background: #007bff;
  color: white;
}
</style>
