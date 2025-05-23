<template>
  <div class="task-form">
    <h3 class="task-title">Завдання: Зв'язування пар</h3>

    <div v-if="pairs.length > 0">
      <p>З'єднайте правильні пари:</p>

      <div class="pairs-container">
        <div class="side left-side">
          <h4>Ліва частина</h4>
          <ul>
            <li v-for="(pair, index) in leftSide" :key="index">
              <div class="pair">
                <span>{{ pair.text }}</span>
              </div>
            </li>
          </ul>
        </div>

        <div class="side right-side">
          <h4>Права частина</h4>
          <ul>
            <li v-for="(pair, index) in rightSide" :key="index">
              <select
                v-model="rightSide[index].selectedRight"
                :disabled="isRightSideDisabled(pair)"
                @change="selectPair(pair, 'right')"
                class="pair"
              >
                <option value="">Виберіть</option>
                <option
                  v-for="(rightPair, idx) in rightSide"
                  :key="idx"
                  :value="rightPair.text"
                  :disabled="isDisabledRightOption(rightPair)"
                >
                  {{ rightPair.text }}
                </option>
              </select>
            </li>
          </ul>
        </div>
      </div>

      <button @click="checkAnswer" class="submit-btn">Перевірити</button>

      <div v-if="resultMessage" class="result-message" :class="resultClass">
        <p>{{ resultMessage }}</p>
      </div>
    </div>

    <p v-else>Завантаження завдання...</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    taskId: Number,
  },
  data() {
    return {
      pairs: [],
      leftSide: [],
      rightSide: [],
      selectedLeft: null,
      selectedRight: null,
      isAnswered: false,
      resultMessage: "",
      resultClass: "",
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
          `http://127.0.0.1:8000/selected_accordance_task_data/`,
          { accordance_task_id: this.taskId },
          { headers: { Authorization: `Token ${token}` } }
        );

        this.pairs = response.data[0].accordance_task_variants_info || [];
        this.splitPairs();
      } catch (error) {
        this.resultMessage = "Не вдалося отримати дані завдання";
        this.resultClass = "error";
        console.error("Помилка отримання даних:", error);
      }
    },

    splitPairs() {
      this.leftSide = this.pairs.map((pair) => ({
        text: pair.first_variant,
        selected: false,
      }));

      this.rightSide = this.pairs.map((pair) => ({
        text: pair.second_variant,
        selected: false,
        selectedRight: "",
      }));

      this.shuffleArray(this.rightSide);
    },

    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
    },

    isRightSideDisabled(pair) {
      return this.leftSide.some(
        (leftPair) => leftPair.selected && leftPair.text === pair.text
      );
    },

    isDisabledRightOption(rightPair) {
      return this.rightSide.some(
        (pair) => pair.selectedRight === rightPair.text
      );
    },

    selectPair(pair, side) {
      if (side === "left") {
        if (this.selectedLeft && this.selectedLeft !== pair) {
          this.selectedLeft.selected = false;
        }
        pair.selected = true;
        this.selectedLeft = pair;
      } else {
        if (this.selectedRight && this.selectedRight !== pair) {
          this.selectedRight.selected = false;
        }
        pair.selected = true;
        this.selectedRight = pair;
      }
    },

    checkAnswer() {
      const allSelected = this.rightSide.every(
        (pair) => pair.selectedRight !== ""
      );

      if (!allSelected) {
        this.resultMessage = "Будь ласка, виберіть всі пари перед перевіркою.";
        this.resultClass = "error";
        return;
      }

      let correctCount = 0;
      let incorrectCount = 0;

      this.pairs.forEach((pair, index) => {
        const selectedAnswer = this.rightSide[index].selectedRight;
        if (selectedAnswer === pair.second_variant) {
          correctCount++;
        } else {
          incorrectCount++;
        }
      });

      console.log(
        "✅ Правильні:",
        correctCount,
        "❌ Неправильні:",
        incorrectCount
      );

      this.$emit("answerSelected", {
        correct: correctCount,
        incorrect: incorrectCount,
      });

      this.isAnswered = true;
    },
  },
};
</script>

<style scoped>
.result-message {
  margin-top: 20px;
  padding: 10px;
  text-align: center;
  border-radius: 5px;
}

.result-message.success {
  background-color: #4caf50;
  color: white;
}

.result-message.error {
  background-color: #f44336;
  color: white;
}

.submit-btn {
  margin-top: 20px;
}
</style>

<style scoped>
.task-form {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.task-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.pairs-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.side {
  flex: 1;
  padding: 0 20px;
}

.left-side h4,
.right-side h4 {
  text-align: center;
  margin-bottom: 10px;
  font-size: 18px;
}

.pair {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f4f4f4;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.pair-button {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  text-align: left;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.pair-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.submit-btn {
  display: block;
  width: 100%;
  padding: 10px;
  margin-top: 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.submit-btn:hover {
  background-color: #45a049;
}

@media (max-width: 768px) {
  .pairs-container {
    flex-direction: column;
  }
  .side {
    padding: 0;
  }
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

.task-label {
  font-size: 18px;
  font-weight: 500;
  display: block;
  margin: 10px 0 20px;
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
