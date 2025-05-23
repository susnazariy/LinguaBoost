<template>
  <div class="add-exercise-form">
    <h3 class="exercise-title">Vocabulary</h3>

    <form @submit.prevent="submitExercise">
      <label for="word_count">Кількість слів:</label>
      <select v-model="wordCount">
        <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
      </select>

      <div v-for="(entry, index) in words" :key="index" class="word-entry">
        <h3>Слово {{ index + 1 }}</h3>
        <label :for="'word_' + index">Слово:</label>
        <input
          v-model="entry.word"
          type="text"
          :id="'word_' + index"
          required
        />

        <label :for="'transcription_' + index">Транскрипція:</label>
        <input
          v-model="entry.transcription"
          type="text"
          :id="'transcription_' + index"
          required
        />

        <label :for="'translation_' + index">Переклад:</label>
        <input
          v-model="entry.translation"
          type="text"
          :id="'translation_' + index"
          required
        />
      </div>

      <div class="buttons">
        <button @click="updateExercise" class="submit-btn">Оновити</button>
        <button @click="deleteExercise" class="delete-exer-btn">
          <i class="fa fa-trash"></i> Видалити
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      wordCount: 1,
      words: [{ word: "", transcription: "", translation: "" }],
      token: "",
      exerciseId: null,
    };
  },
  watch: {
    wordCount(newCount) {
      const updatedWords = Array.from(
        { length: newCount },
        (_, i) =>
          this.words[i] || { word: "", transcription: "", translation: "" }
      );
      this.words = updatedWords;
    },
  },
  mounted() {
    this.token = this.$store.state.token;
    this.exerciseId = this.$route.params.id;
    this.fetchExercise();
  },
  methods: {
    async fetchExercise() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/selected_vocabulary_exercise_data/",
          { vocabulary_exersice_id: this.exerciseId },
          {
            headers: { Authorization: `Token ${this.token}` },
          }
        );

        const exerciseData = response.data[0];

        this.words = exerciseData.vocabulary_words_info.map((wordData) => ({
          id: wordData.id,
          word: wordData.english_word,
          transcription: wordData.transcription,
          translation: wordData.ukrainian_word,
        }));
        this.ids = this.words.map((pair) => pair.id);

        this.wordCount = this.words.length;
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося завантажити вправу", "error");
      }
    },
    validateWords() {
      const wordsSet = new Set();
      let isValid = true;

      for (const entry of this.words) {
        const word = entry.word.trim();
        const transcription = entry.transcription.trim();
        const translation = entry.translation.trim();

        if (!word || !transcription || !translation) {
          Swal.fire("Помилка!", "Усі поля мають бути заповнені.", "error");
          isValid = false;
          break;
        }

        if (wordsSet.has(word) || wordsSet.has(translation)) {
          Swal.fire("Помилка!", "Слова не повинні повторюватися.", "error");
          isValid = false;
          break;
        }

        const isEnglish = /^[a-zA-Z\s]+$/.test(word);
        const isUkrainian = /^[а-яА-ЯіІїЇєЄґҐ\s]+$/.test(translation);

        if (isEnglish && isUkrainian) {
          wordsSet.add(word);
          wordsSet.add(translation);
        } else {
          Swal.fire(
            "Помилка!",
            "Англійське слово має бути написано латиницею, а переклад українською.",
            "error"
          );
          isValid = false;
          break;
        }
      }

      return isValid;
    },
    async updateExercise() {
      if (!this.validateWords()) return;

      const formData = {
        vocabulary_exercise_id: this.exerciseId,
        vocabulary_words_ids: this.ids,
        new_vocabulary_words_list: this.words.map((entry) => ({
          english_word: entry.word.trim(),
          transcription: entry.transcription.trim(),
          ukrainian_word: entry.translation.trim(),
        })),
      };

      try {
        await axios.post(
          "http://127.0.0.1:8000/update_vocabulary_exercise/",
          formData,
          {
            headers: {
              Authorization: `Token ${this.token}`,
              "Content-Type": "application/json",
            },
          }
        );

        Swal.fire("Успішно!", "Вправа оновлена", "success");
      } catch (error) {
        Swal.fire("Помилка!", "Не вдалося оновити вправу", "error");
      }
    },
    async deleteExercise() {
      const token = this.$store.state.token;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/delete_vocabulary_exercise/",
          { vocabulary_exercise_id: this.exerciseId },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );

        if (response.data === "Vocabulary exercise successfully deleted!") {
          Swal.fire({
            icon: "success",
            title: "Вправу успішно видалено!",
            showConfirmButton: false,
            timer: 1500,
          }).then(() => {
            this.$router.go(-1);
          });
        } else {
          Swal.fire({
            icon: "error",
            title: "Помилка",
            text: "Не вдалося видалити вправу.",
          });
        }
      } catch (error) {
        console.error("Помилка при видаленні вправи:", error);
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
.exercise-title {
  text-align: center;
  margin: 15px auto;
  font-size: 19px;
}
.add-exercise-form {
  max-width: 600px;
  margin: auto;
  border-radius: 10px;
  font-family: "Roboto", sans-serif;
}

h2 {
  text-align: center;
  color: #333;
  font-size: 2rem;
  margin-bottom: 20px;
}

select {
  width: 100%;
  box-sizing: border-box;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
  font-size: 1rem;
  color: #333;
}

select:focus {
  border-color: #007bff;
  outline: none;
}

.word-entry {
  background: #fff;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.word-entry:hover {
  border-color: #007bff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

input[type="text"] {
  width: 100%;
  box-sizing: border-box;
  padding: 10px;
  margin: 5px 0 15px 0;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  color: #333;
  background: #f9f9f9;
}

input[type="text"]:focus {
  border-color: #007bff;
  background: #fff;
  outline: none;
}

.buttons {
  display: flex;
  justify-content: space-between;
  margin: 0 auto;
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

.delete-exer-btn {
  background-color: red;
}

.submit-btn:hover {
  background-color: #3e4b9f;
}

.delete-exer-btn:hover {
  background-color: rgb(183, 0, 0);
}

label {
  display: block;
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 8px;
  color: #555;
}
</style>
