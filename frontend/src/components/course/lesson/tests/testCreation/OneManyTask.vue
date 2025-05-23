<template>
  <div class="task-form">
    <h3 class="task-title">Створення завдання: Заповніть пропуск у реченні</h3>

    <label class="task-label">Речення з пропуском:</label>
    <div class="sentence-container">
      <input
        v-model="sentence"
        type="text"
        placeholder="Введіть речення, в якому є пропуск"
        class="task-inputs"
      />
      <span class="help-text"
        >Позначте пропуск символом <strong>&&</strong> в реченні</span
      >
    </div>

    <label class="task-label">Варіанти відповіді:</label>
    <div class="answer-container">
      <input
        v-model="answers[0]"
        type="text"
        placeholder="Варіант 1"
        class="task-input"
      />
      <input
        v-model="answers[1]"
        type="text"
        placeholder="Варіант 2"
        class="task-input"
      />
      <input
        v-model="answers[2]"
        type="text"
        placeholder="Варіант 3"
        class="task-input"
      />
      <input
        v-model="answers[3]"
        type="text"
        placeholder="Варіант 4"
        class="task-input"
      />
      <p class="instruction">* Перший варіант завжди правильний.</p>
    </div>

    <button @click="submit" class="submit-btn">Надіслати</button>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      sentence: "",
      answers: ["", "", "", ""],
    };
  },
  methods: {
    async submit() {
      if (this.answers.some((answer) => answer.trim() === "")) {
        Swal.fire("Помилка", "Всі варіанти повинні бути заповнені.", "error");
        return;
      }

      if (new Set(this.answers).size !== this.answers.length) {
        Swal.fire(
          "Помилка",
          "Варіанти відповідей повинні бути унікальними.",
          "error"
        );
        return;
      }

      const pattern = /\s&&\s/;
      if (!pattern.test(this.sentence)) {
        Swal.fire(
          "Помилка",
          "Речення повинно містити пропуск (&&) з пробілами з обох боків.",
          "error"
        );
        return;
      }
      const lessonId = this.$route.params.id;

      const data = {
        lesson_id: lessonId,
        text: this.sentence,
        correct_answer: this.answers[0],
        first_wrong_answer: this.answers[1],
        second_wrong_answer: this.answers[2],
        third_wrong_answer: this.answers[3],
      };

      try {
        const token = this.$store.state.token;
        await axios.post("http://127.0.0.1:8000/add_one_many_task/", data, {
          headers: { Authorization: `Token ${token}` },
        });

        Swal.fire("Успіх", "Завдання успішно створено!", "success");

        this.sentence = "";
        this.answers = ["", "", "", ""];
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося створити завдання", "error");
        console.error("Помилка надсилання:", error);
      }
    },
  },
};
</script>

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

.task-label {
  font-size: 18px;
  font-weight: 500;
  display: block;
  margin: 10px 0;
}

.task-input,
.task-inputs {
  width: 95%;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #2562e8;
  border-radius: 5px;
  outline: none;
  margin-bottom: 10px;
}

.task-input:first-of-type {
  border: 2px solid green;
}

.sentence-container {
  margin-bottom: 20px;
}

.help-text {
  display: block;
  font-size: 14px;
  color: #888;
  margin-top: 5px;
}

.answer-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
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

.instruction {
  font-size: 16px;
  margin-top: 15px;
  color: #555;
}
</style>
