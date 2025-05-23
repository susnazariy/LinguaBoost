<template>
  <div class="exercise-view">
    <h3 class="exercise-title">Vocabulary</h3>

    <p><strong>Кількість слів:</strong> {{ words.length }}</p>

    <div class="buttons">
      <button @click="toggleEnglish" class="toggle-btn">
        {{ showEnglish ? "Закрити" : "Відкрити" }} англійські слова
      </button>

      <button @click="toggleTranslation" class="toggle-btn">
        {{ showTranslation ? "Закрити" : "Відкрити" }} переклад
      </button>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Англійське слово</th>
            <th>Транскрипція</th>
            <th>Переклад</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in words" :key="entry.id">
            <td v-if="showEnglish">{{ entry.word }}</td>
            <td v-else>•••</td>

            <td v-if="showEnglish">{{ entry.transcription }}</td>
            <td v-else>•••</td>

            <td v-if="showTranslation">{{ entry.translation }}</td>
            <td v-else>•••</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  props: ["id"],
  data() {
    return {
      words: [],
      showEnglish: false,
      showTranslation: false,
    };
  },
  mounted() {
    this.fetchExercise();
  },
  methods: {
    async fetchExercise() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/selected_vocabulary_exercise_data/",
          { vocabulary_exersice_id: this.id },
          {
            headers: { Authorization: `Token ${this.$store.state.token}` },
          }
        );

        const exerciseData = response.data[0];
        this.words = exerciseData.vocabulary_words_info.map((wordData) => ({
          id: wordData.id,
          word: wordData.english_word,
          transcription: wordData.transcription,
          translation: wordData.ukrainian_word,
        }));
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося завантажити вправу", "error");
      }
    },
    toggleEnglish() {
      this.showEnglish = !this.showEnglish;
    },
    toggleTranslation() {
      this.showTranslation = !this.showTranslation;
    },
  },
};
</script>

<style scoped>
.exercise-view {
  width: 660px;
  margin: auto;
  font-family: "Roboto", sans-serif;
  text-align: center;
}

h2 {
  color: #333;
  font-size: 2rem;
  margin-bottom: 20px;
}

.buttons {
  display: flex;
  justify-content: space-between;
}

.toggle-btn {
  background: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
  font-size: 1rem;
}

.toggle-btn:hover {
  background: #0056b3;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

thead {
  background: #f8f9fa;
}

td,
th {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}
</style>
