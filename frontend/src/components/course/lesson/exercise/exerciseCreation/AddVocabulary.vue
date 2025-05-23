<template>
  <div class="add-exercise-form">
    <h2>Додати Vocabulary</h2>

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

      <button type="submit">Додати вправу</button>
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
  },
  methods: {
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
    async submitExercise() {
      if (!this.validateWords()) return;
      const lessonId = this.$route.params.id;

      const formData = {
        lesson_id: lessonId,
        vocabulary_words_list: this.words.map((entry) => ({
          english_word: entry.word.trim(),
          transcription: entry.transcription.trim(),
          ukrainian_word: entry.translation.trim(),
        })),
      };

      try {
        await axios.post(
          "http://127.0.0.1:8000/add_vocabulary_exercise/",
          formData,
          {
            headers: {
              Authorization: `Token ${this.token}`,
              "Content-Type": "application/json",
            },
          }
        );

        Swal.fire({
          icon: "success",
          title: "Вправа успішно додана!",
          confirmButtonText: "OK",
        }).then(() => {
          this.$router.go("-1");
        });
        this.resetForm();
      } catch (error) {
        Swal.fire("Помилка!", "Не вдалося додати вправу", "error");
      }
    },
    resetForm() {
      this.wordCount = 1;
      this.words = [{ word: "", transcription: "", translation: "" }];
    },
  },
};
</script>

<style scoped>
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
  width: 95%;
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

button {
  width: 100%;
  padding: 12px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #3e4b9f;
}

label {
  display: block;
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 8px;
  color: #555;
}
</style>
