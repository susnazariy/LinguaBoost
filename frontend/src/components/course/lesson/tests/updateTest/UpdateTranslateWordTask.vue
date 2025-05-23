<template>
  <div class="task-form">
    <h3 class="task-title">Переклад слова</h3>

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
    <div class="buttons">
      <button @click="submit" class="submit-btn">Зберегти зміни</button>

      <button @click="deleteTask(taskId)" class="delete-test-btn">
        <i class="fa fa-trash"></i> Видалити тестове
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      taskId: null,
      word: "",
      translation: "",
    };
  },
  created() {
    this.taskId = this.$route.params.id;
  },
  methods: {
    async fetchTaskData(id) {
      try {
        const token = this.$store.state.token;
        const response = await axios.post(
          `http://127.0.0.1:8000/selected_translate_word_task_data/`,
          { translate_word_task_id: this.taskId },
          {
            headers: { Authorization: `Token ${token}` },
          }
        );
        this.word = response.data[0].english_word;
        this.translation = response.data[0].ukrainian_word;
        this.taskId = id;
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося завантажити дані завдання", "error");
        console.error("Помилка завантаження:", error);
      }
    },

    async submit() {
      if (!this.validateInputs()) {
        return;
      }

      const data = {
        translate_word_task_id: this.taskId,
        new_english_word: this.word.trim(),
        new_ukrainian_word: this.translation.trim(),
      };

      try {
        const token = this.$store.state.token;
        await axios.post(
          "http://127.0.0.1:8000/update_translate_word_task/",
          data,
          {
            headers: { Authorization: `Token ${token}` },
          }
        );

        Swal.fire("Успіх", "Завдання успішно оновлено!", "success");
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося оновити завдання", "error");
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

    async deleteTask(task) {
      const token = this.$store.state.token;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/delete_translate_word_task/",
          { translate_word_task_id: task },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );

        if (response.data === "Translate word task successfully deleted!") {
          Swal.fire({
            icon: "success",
            title: "Запитання успішно видалено!",
            showConfirmButton: false,
            timer: 1500,
          });
        } else if (response.data === "Delete translate word task error!") {
          Swal.fire({
            icon: "error",
            title: "Помилка!",
            text: "Не вдалося видалити запитання.",
          });
        } else {
          Swal.fire({
            icon: "error",
            title: "Помилка!",
            text: "Не вдалося видалити курс.",
          });
        }
      } catch (error) {
        console.error("Помилка при видаленні курсу:", error);
        Swal.fire({
          icon: "error",
          title: "Сталася помилка!",
          text: "Спробуйте ще раз.",
        });
      }
    },
  },

  mounted() {
    const taskId = 1;
    this.fetchTaskData(taskId);
  },
};
</script>

<style scoped>
.buttons {
  display: flex;
  justify-content: space-between;
  margin: 20px auto;
  width: 500px;
}
button {
  padding: 12px 20px;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}
.submit-btn {
  padding: 12px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-test-btn {
  background-color: red;
}

.submit-btn:hover {
  background-color: #3e4b9f;
}

.delete-test-btn:hover {
  background-color: rgb(183, 0, 0);
}

.task-title {
  text-align: center;
  margin: 15px auto;
  font-size: 19px;
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

.task-label {
  font-size: 18px;
  font-weight: 500;
  display: block;
  margin: 10px 0 20px;
}

.task-input {
  width: 100%;
  box-sizing: border-box;
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
