<template>
  <div class="fill-in-the-blanks">
    <h2>Створення питання</h2>

    <textarea v-model="text" @mouseup="selectWord"></textarea>

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
</template>

<script>
export default {
  data() {
    return {
      text: "Вивчення Vue.js є дуже корисним для розробників.",
      blanks: [],
    };
  },
  methods: {
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
      this.text = this.text.replace(
        `{${this.blanks[index].index}}`,
        this.blanks[index].original
      );
      this.blanks.splice(index, 1);
    },
    saveQuestion() {
      let formattedText = this.text;
      let answers = this.blanks.map((b) => b.correct);

      console.log("Збережене питання:", {
        text: formattedText,
        answers: answers,
      });
    },
  },
};
</script>

<style>
.fill-in-the-blanks {
  max-width: 600px;
  margin: auto;
  font-family: Arial, sans-serif;
}
textarea {
  width: 100%;
  height: 100px;
}
button {
  margin-left: 10px;
}
</style>
