<template>
  <div class="task-form">
    <h3 class="task-title">Зв'язування пар</h3>

    <label class="gaps">Кількість пар: </label>
    <select
      v-model="pairCount"
      @change="generateInputFields"
      class="pair-select"
    >
      <option value="2">2</option>
      <option value="3">3</option>
      <option value="4">4</option>
      <option value="5">5</option>
      <option value="6">6</option>
      <option value="7">7</option>
      <option value="8">8</option>
      <option value="9">9</option>
      <option value="10">10</option>
    </select>

    <div v-for="(pair, index) in pairs" :key="index" class="pair-container">
      <div class="pair">
        <input
          v-model="pair.first_variant"
          type="text"
          placeholder="Ліва частина"
          class="task-input"
        />
        <input
          v-model="pair.second_variant"
          type="text"
          placeholder="Права частина"
          class="task-input"
        />
      </div>
    </div>
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
      pairCount: 1,
      pairs: [{ first_variant: "", second_variant: "" }],
      taskId: null,
    };
  },
  created() {
    this.taskId = this.$route.params.id;

    if (this.taskId) {
      this.fetchTaskData();
    }
  },
  methods: {
    async fetchTaskData() {
      try {
        const token = this.$store.state.token;
        const response = await axios.post(
          `http://127.0.0.1:8000/selected_accordance_task_data/`,
          { accordance_task_id: this.taskId },
          {
            headers: { Authorization: `Token ${token}` },
          }
        );

        this.taskId = response.data[0].id;
        this.pairs = response.data[0].accordance_task_variants_info || [];
        this.ids = this.pairs.map((pair) => pair.id);

        this.pairCount = this.pairs.length || 1;
        this.generateInputFields();
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося отримати дані завдання", "error");
        console.error("Помилка отримання даних:", error);
      }
    },

    generateInputFields() {
      const count = parseInt(this.pairCount);

      if (count < this.pairs.length) {
        this.pairs = this.pairs.slice(0, count);
      } else if (count > this.pairs.length) {
        for (let i = this.pairs.length; i < count; i++) {
          this.pairs.push({ first_variant: "", second_variant: "" });
        }
      }
    },

    async submit() {
      for (const pair of this.pairs) {
        if (!pair.first_variant || !pair.second_variant) {
          Swal.fire("Помилка", "Будь ласка, заповніть всі пари", "error");
          return;
        }
      }

      const renamedPairs = this.pairs.map((pair) => ({
        left: pair.first_variant,
        right: pair.second_variant,
      }));

      const data = {
        accordance_task_id: 2,
        accordance_task_variants_ids: this.ids,
        new_variants: renamedPairs,
      };

      try {
        const token = this.$store.state.token;
        await axios.post(
          `http://127.0.0.1:8000/update_accordance_task/`,
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
    async deleteTask(task) {
      const token = this.$store.state.token;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/delete_accordance_task/",
          { accordance_task_id: task },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );

        if (response.data === "Accordance task successfully deleted!") {
          Swal.fire({
            icon: "success",
            title: "Запитання успішно видалено!",
            showConfirmButton: false,
            timer: 1500,
          });
        } else if (response.data === "Delete accordance task error!") {
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
.gaps {
  margin-right: 20px;
}
.task-form {
  max-width: 1100px;
  margin: 20px auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.pair-select {
  font-size: 16px;
  padding: 8px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.pair-container {
  margin-bottom: 20px;
}

.pair {
  display: flex;
  gap: 10px;
}

.pair {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f4f4f4;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.task-input {
  width: 48%;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #2562e8;
  border-radius: 5px;
  outline: none;
}
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
</style>
