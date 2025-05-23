<template>
  <div class="task-form">
    <h3 class="task-title">Завдання: Зібрати правильне речення</h3>

    <div v-if="sentence">
      <p>Розкидане речення:</p>
      <div class="words-container">
        <span
          v-for="(word, index) in shuffledWords"
          :key="index"
          class="word-item"
        >
          {{ word }}
        </span>
      </div>

      <label>Введіть правильне речення:</label>
      <input
        v-model="userInput"
        type="text"
        placeholder="Зберіть речення"
        class="task-input"
        :disabled="isAnswered"
      />

      <button @click="submitTask" :disabled="isAnswered" class="submit-btn">
        Перевірити
      </button>
    </div>

    <p v-else>Завантаження завдання...</p>

    <p v-if="isAnswered" :class="{ correct: isCorrect, incorrect: !isCorrect }">
      {{
        isCorrect
          ? "Правильно!"
          : "Неправильно! Правильна відповідь: " + sentence
      }}
    </p>
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
      sentence: "",
      shuffledWords: [],
      userInput: "",
      isAnswered: false,
      isCorrect: false,
    };
  },

  created() {
    this.fetchTaskData();
  },

  watch: {
    taskId: {
      handler() {
        this.fetchTaskData();
      },
      immediate: true,
    },
  },

  methods: {
    async fetchTaskData() {
      try {
        const token = this.$store.state.token;
        const response = await axios.post(
          "http://127.0.0.1:8000/selected_sequence_task_data/",
          { sequence_task_id: this.taskId },
          { headers: { Authorization: `Token ${token}` } }
        );

        this.sentence = response.data[0].sequence_text;

        const words = this.sentence.split(" ");
        this.shuffledWords = this.shuffleWords(words);
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося завантажити завдання", "error");
        console.error("Помилка отримання даних:", error);
      }
    },

    shuffleWords(words) {
      return words.sort(() => Math.random() - 0.5);
    },

    submitTask() {
      if (!this.userInput.trim()) {
        Swal.fire("Помилка", "Поле не може бути порожнім", "error");
        return;
      }

      this.isAnswered = true;

      const isCorrect = this.userInput.trim() === this.sentence;

      this.$emit("answerSelected", {
        correct: isCorrect ? 1 : 0,
        incorrect: isCorrect ? 0 : 1,
      });
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

.words-container {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 15px;
}

.word-item {
  margin: 5px;
  padding: 5px 10px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.task-input {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
}

.submit-btn {
  margin-top: 10px;
  padding: 10px 15px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #45a049;
}
</style>

<style scoped>
.task-form {
  max-width: 1100px;
  margin: 20px auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.task-title {
  text-align: center;
  color: #2562e8;
  font-weight: 700;
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

.submit-btn {
  display: block;
  width: 100%;
  padding: 12px;
  margin-top: 20px;
  background: #2562e8;
  color: #fff;
  font-size: 18px;
  font-weight: 500;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.submit-btn:hover {
  background: #1d4eb5;
}
</style>
