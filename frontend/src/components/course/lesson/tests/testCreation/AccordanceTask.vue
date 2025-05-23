<template>
  <div class="task-form">
    <h3 class="task-title">Створення завдання: Зв'язування пар</h3>

    <label class="gaps">Кількість пар:</label>
    <select
      v-model="pairCount"
      @change="generateInputFields"
      class="pair-select"
    >
      <option v-for="num in 9" :key="num" :value="num + 1">
        {{ num + 1 }}
      </option>
    </select>

    <div v-for="(pair, index) in pairs" :key="index" class="pair-container">
      <div class="pair">
        <input
          v-model="pair.left"
          type="text"
          placeholder="Ліва частина"
          class="task-input"
        />
        <input
          v-model="pair.right"
          type="text"
          placeholder="Права частина"
          class="task-input"
        />
      </div>
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
      pairCount: 2,
      pairs: Array.from({ length: 2 }, () => ({ left: "", right: "" })),
    };
  },
  methods: {
    generateInputFields() {
      const count = parseInt(this.pairCount);
      this.pairs = Array.from({ length: count }, () => ({
        left: "",
        right: "",
      }));
    },

    async submit() {
      const leftValues = new Set();
      const rightValues = new Set();

      for (const pair of this.pairs) {
        if (!pair.left || !pair.right) {
          Swal.fire("Помилка", "Будь ласка, заповніть всі пари", "error");
          return;
        }
        if (leftValues.has(pair.left) || rightValues.has(pair.right)) {
          Swal.fire("Помилка", "Усі значення мають бути унікальними!", "error");
          return;
        }
        leftValues.add(pair.left);
        rightValues.add(pair.right);
      }
      const lessonId = this.$route.params.id;

      const data = { lesson_id: lessonId, variants: this.pairs };

      try {
        const token = this.$store.state.token;
        await axios.post("http://127.0.0.1:8000/add_accordance_task/", data, {
          headers: { Authorization: `Token ${token}` },
        });

        Swal.fire("Успіх", "Завдання успішно створено!", "success");

        this.pairCount = 2;
        this.pairs = Array.from({ length: this.pairCount }, () => ({
          left: "",
          right: "",
        }));
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося створити завдання", "error");
        console.error("Помилка надсилання:", error);
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
