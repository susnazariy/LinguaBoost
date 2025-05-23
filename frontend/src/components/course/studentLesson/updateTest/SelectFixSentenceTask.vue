<template>
  <div class="task-form">
    <h3 v-if="task" class="task-title">Завдання</h3>

    <div v-if="task" class="task-label">
      <p class="sentence">{{ formattedSentence(task.bad_text) }}</p>
      <textarea
        v-model="userAnswer"
        type="text"
        placeholder="Введіть правильне речення"
        class="task-input"
        :disabled="isAnswered"
      />

      <button @click="checkAnswer" :disabled="isAnswered" class="task-btn">
        Перевірити
      </button>

      <p
        v-if="isAnswered"
        :class="{ correct: isCorrect, incorrect: !isCorrect }"
      >
        {{
          isCorrect
            ? "Правильно!"
            : "Неправильно! Правильна відповідь: " + task.correct_text
        }}
      </p>
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
      userAnswer: "",
      isAnswered: false,
      isCorrect: false,
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
          "http://127.0.0.1:8000/selected_fix_sentence_task_data/",
          { fix_sentence_task_id: this.taskId },
          { headers: { Authorization: `Token ${token}` } }
        );
        this.task = response.data[0];
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося завантажити завдання", "error");
        console.error("Помилка отримання завдання:", error);
      }
    },

    checkAnswer() {
      if (!this.userAnswer.trim()) {
        Swal.fire("Помилка", "Поле не може бути порожнім", "error");
        return;
      }

      this.isAnswered = true;

      const isCorrect =
        this.userAnswer.trim().toLowerCase() ===
        this.task.correct_text.trim().toLowerCase();

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
.correct {
  color: green;
}

.incorrect {
  color: red;
}

.feedback-message {
  font-size: 14px;
  margin-top: 10px;
}

.task-form {
  max-width: 1100px;
  margin: 20px auto;
  padding: 20px;
  font-family: "Roboto", sans-serif;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.task-title {
  text-align: center;
  color: #2562e8;
  font-weight: 700;
}

.task-label {
  font-size: 18px;
  font-weight: 500;
  display: block;
  margin: 10px 0 20px;
}

.task-input {
  width: 95%;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #2562e8;
  border-radius: 5px;
  outline: none;
  margin-bottom: 10px;
}

.task-input.correct {
  border-color: green;
  background-color: #d4edda;
}

.task-input.incorrect {
  border-color: red;
  background-color: #f8d7da;
}

.instruction {
  font-size: 16px;
  margin-top: 15px;
  color: #555;
}

.task-btn {
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

.task-btn:hover {
  background: #1d4eb5;
}
</style>
