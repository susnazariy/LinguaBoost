<template>
  <div class="task-creator">
    <h2>Створення завдання</h2>

    <button @click="toggleDropdown">Вибрати тип завдання</button>

    <div v-if="dropdownVisible" class="dropdown">
      <ul>
        <li @click="selectTask('question')">Питання та відповіді</li>
        <li @click="selectTask('sentence')">Правильне/неправильне речення</li>
        <li @click="selectTask('blank')">Пропуски</li>
      </ul>
    </div>

    <div v-if="selectedTask === 'question'">
      <h3>Питання та відповіді</h3>
      <label for="question">Питання:</label>
      <input
        v-model="questionText"
        id="question"
        placeholder="Введіть питання"
      />

      <h4>Відповіді:</h4>
      <div v-for="(answer, index) in answers" :key="index">
        <input
          v-model="answers[index]"
          :placeholder="'Відповідь ' + (index + 1)"
        />
      </div>
      <button @click="saveQuestion">Зберегти питання</button>
    </div>

    <div v-if="selectedTask === 'sentence'">
      <h3>Правильне/Неправильне речення</h3>
      <label for="sentence">Речення з помилкою:</label>
      <input
        v-model="sentenceText"
        id="sentence"
        placeholder="Введіть речення"
      />
      <button @click="saveSentence">Зберегти речення</button>
    </div>

    <div v-if="selectedTask === 'blank'">
      <h3>Пропуски</h3>
      <textarea v-model="text" @input="updateBlanksIndexes"></textarea>

      <h3>Пропуски:</h3>
      <ul>
        <li v-for="(word, index) in blanks" :key="index">
          {{ word.original }} →
          <input v-model="word.correct" placeholder="Введіть правильне слово" />
          <button @click="removeBlank(index)">❌</button>
        </li>
      </ul>

      <button @click="saveQuestion">Зберегти питання</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dropdownVisible: false,
      selectedTask: null,
      questionText: "",
      answers: ["", "", ""],
      sentenceText: "",
      text: "",
      blanks: [],
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    selectTask(task) {
      this.selectedTask = task;
      this.dropdownVisible = false;
    },
    saveQuestion() {
      console.log("Збережене питання:", {
        question: this.questionText,
        answers: this.answers,
      });
    },
    saveSentence() {
      console.log("Збережене речення:", {
        sentence: this.sentenceText,
      });
    },
    selectWord() {
      let selection = window.getSelection().toString().trim();
      if (selection && !this.blanks.some((b) => b.original === selection)) {
        const index = this.text.indexOf(selection);
        this.blanks.push({
          original: selection,
          correct: selection,
          index: index,
        });

        this.text = this.replaceWordWithPlaceholder(
          this.text,
          selection,
          index
        );
      }
    },
    replaceWordWithPlaceholder(text, word, index) {
      const placeholder = `{${index}}`;
      return text.replace(word, placeholder);
    },
    removeBlank(index) {
      const placeholder = `{${this.blanks[index].index}}`;
      this.text = this.text.replace(placeholder, this.blanks[index].original);

      this.blanks.splice(index, 1);

      this.updateBlanksIndexes();
      this.text = this.updateTextWithBlanks();
    },
    updateBlanksIndexes() {
      this.blanks.forEach((word) => {
        word.index = this.text.indexOf(word.original);
      });
    },
    updateTextWithBlanks() {
      let updatedText = this.text;
      this.blanks.forEach((word) => {
        const placeholder = `{${word.index}}`;
        updatedText = updatedText.replace(placeholder, word.original);
      });
      return updatedText;
    },
  },
};
</script>

<style scoped>
.task-creator {
  margin: 20px;
}

.dropdown {
  position: absolute;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  width: 200px;
}

.dropdown ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropdown li {
  padding: 8px;
  cursor: pointer;
}

.dropdown li:hover {
  background-color: #ddd;
}
</style>
