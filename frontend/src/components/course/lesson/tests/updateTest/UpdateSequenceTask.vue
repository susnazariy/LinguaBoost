<template>
  <div class="task-form">
    <h3 class="task-title">Розбиття речення на слова</h3>

    <label class="task-label">Введіть речення:</label>
    <input
      v-model="sentence"
      type="text"
      placeholder="Введіть речення"
      class="task-input"
    />
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
    };
  },
  mounted() {
    this.fetchTask();
  },
  created() {
    this.taskId = this.$route.params.id;
  },
  methods: {
    async fetchTask() {
      try {
        const token = this.$store.state.token;
        const response = await axios.post(
          "http://127.0.0.1:8000/selected_sequence_task_data/",
          {
            sequence_task_id: this.taskId,
          },
          {
            headers: { Authorization: `Token ${token}` },
          }
        );
        this.id = response.data[0].id;
        this.sentence = response.data[0].sequence_text;
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося завантажити завдання", "error");
        console.error("Помилка отримання даних:", error);
      }
    },
    async updateTask() {
      if (!this.sentence.trim()) {
        Swal.fire("Помилка", "Речення не може бути порожнім.", "error");
        return;
      }

      const data = {
        sequence_task_id: this.taskId,
        new_sequence_text: this.sentence,
      };

      try {
        const token = this.$store.state.token;
        await axios.post("http://127.0.0.1:8000/update_sequence_task/", data, {
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
          "http://127.0.0.1:8000/delete_sequence_task/",
          { sequence_task_id: task },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );

        if (response.data === "Sequence task successfully deleted!") {
          Swal.fire({
            icon: "success",
            title: "Запитання успішно видалено!",
            showConfirmButton: false,
            timer: 1500,
          });
        } else if (response.data === "Delete sequence task error!") {
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
</style>
