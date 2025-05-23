<template>
  <div class="task-form">
    <h3 class="task-title">Заповніть пропуск у реченні</h3>

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
    <div class="buttons">
      <button @click="updateTask" class="submit-btn">Зберегти зміни</button>

      <button @click="deleteTask(id)" class="delete-test-btn">
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
      id: null,
      sentence: "",
      answers: ["", "", "", ""],
    };
  },
  created() {
    this.taskId = this.$route.params.id;
  },
  async mounted() {
    try {
      const token = this.$store.state.token;
      const response = await axios.post(
        "http://127.0.0.1:8000/selected_one_many_task_data/",
        { one_many_task_id: this.taskId },
        { headers: { Authorization: `Token ${token}` } }
      );

      const task = response.data[0];
      this.sentence = task.text;
      this.id = task.id;

      this.answers = [
        task.correct_answer,
        task.first_wrong_answer,
        task.second_wrong_answer,
        task.third_wrong_answer,
      ];
    } catch (error) {
      Swal.fire("Помилка", "Не вдалося завантажити завдання", "error");
      console.error("Помилка отримання завдання:", error);
    }
  },

  methods: {
    async updateTask() {
      if (this.answers.some((answer) => answer.trim() === "")) {
        Swal.fire("Помилка", "Всі варіанти повинні бути заповнені.", "error");
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

      const data = {
        one_many_task_id: this.id,
        new_text: this.sentence,
        new_correct_answer: this.answers[0],
        new_first_wrong_answer: this.answers[1],
        new_second_wrong_answer: this.answers[2],
        new_third_wrong_answer: this.answers[3],
      };

      try {
        const token = this.$store.state.token;
        await axios.post("http://127.0.0.1:8000/update_one_many_task/", data, {
          headers: { Authorization: `Token ${token}` },
        });

        Swal.fire("Успіх", "Завдання успішно оновлено!", "success");
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося оновити завдання", "error");
        console.error("Помилка оновлення:", error);
      }
    },
    async deleteTask(task) {
      const token = this.$store.state.token;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/delete_one_many_task/",
          { one_many_task_id: task },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );

        if (response.data === "One many task successfully deleted!") {
          Swal.fire({
            icon: "success",
            title: "Запитання успішно видалено!",
            showConfirmButton: false,
            timer: 1500,
          });
        } else if (response.data === "Delete one many task error!") {
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
.task-label {
  font-size: 18px;
  font-weight: 500;
  display: block;
  margin: 10px 0 20px;
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
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}
.task-input,
.task-inputs {
  width: 100%;
  box-sizing: border-box;
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

.instruction {
  font-size: 16px;
  margin-top: 15px;
  color: #555;
}
</style>
