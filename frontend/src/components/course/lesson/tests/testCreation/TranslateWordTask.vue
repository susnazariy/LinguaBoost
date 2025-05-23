<template>
  <div class="task-form">
    <h3 class="task-title">Створення завдання: Переклад слова</h3>

    <label class="task-label">Введіть слово англійською:</label>
    <input
      v-model="word"
      type="text"
      placeholder="Введіть слово"
      class="task-input"
    />

    <label class="task-label">Введіть переклад:</label>
    <input
      v-model="translation"
      type="text"
      placeholder="Переклад"
      class="task-input"
    />

    <button @click="submit" class="task-btn">Надіслати</button>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      word: "",
      translation: "",
    };
  },
  methods: {
    async submit() {
      if (!this.validateInputs()) {
        return;
      }
      const lessonId = this.$route.params.id;

      const data = {
        lesson_id: lessonId,
        english_word: this.word.trim(),
        ukrainian_word: this.translation.trim(),
      };

      try {
        const token = this.$store.state.token;
        await axios.post(
          "http://127.0.0.1:8000/add_translate_word_task/",
          data,
          {
            headers: { Authorization: `Token ${token}` },
          }
        );

        Swal.fire("Успіх", "Завдання успішно створено!", "success");

        this.word = "";
        this.translation = "";
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося створити завдання", "error");
        console.error("Помилка надсилання:", error);
      }
    },

    validateInputs() {
      const englishRegex = /^[A-Za-z\s]+$/;
      const ukrainianRegex = /^[А-ЩЬЮЯҐЄІЇа-щьюяґєії\s]+$/;

      if (!this.word.trim() || !this.translation.trim()) {
        Swal.fire("Помилка", "Будь ласка, заповніть обидва поля", "warning");
        return false;
      }

      if (!englishRegex.test(this.word.trim())) {
        Swal.fire(
          "Помилка",
          "Англійське слово повинно містити лише латинські літери та пробіли",
          "warning"
        );
        return false;
      }

      if (!ukrainianRegex.test(this.translation.trim())) {
        Swal.fire(
          "Помилка",
          "Український переклад повинен містити лише кирилицю та пробіли",
          "warning"
        );
        return false;
      }

      return true;
    },
  },
};
</script>

<style scoped>
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
  margin: 10px 0 5px;
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
