<template>
  <div class="task-form">
    <h3 class="task-title">Створення завдання: Розбиття речення на слова</h3>

    <label class="task-label">Введіть речення:</label>
    <input
      v-model="sentence"
      type="text"
      placeholder="Введіть речення"
      class="task-input"
    />

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
    };
  },
  methods: {
    async submit() {
      if (this.sentence.trim().length === 0) {
        Swal.fire("Помилка", "Будь ласка, введіть речення.", "error");
        return;
      }
      const lessonId = this.$route.params.id;

      const data = {
        lesson_id: lessonId,
        sequence_text: this.sentence.trim(),
      };

      try {
        const token = this.$store.state.token;
        await axios.post("http://127.0.0.1:8000/add_sequence_task/", data, {
          headers: { Authorization: `Token ${token}` },
        });
        Swal.fire("Успіх", "Завдання успішно створено!", "success");

        this.sentence = "";
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
