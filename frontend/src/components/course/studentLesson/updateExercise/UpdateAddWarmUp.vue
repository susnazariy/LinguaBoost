<template>
  <div class="exercise-form">
    <h3 class="exercise-title">Warm-up / Discussion</h3>

    <div v-if="exercise_image" class="image-container">
      <img
        :src="getPhoto(exercise_image)"
        alt="Exercise Image"
        class="exercise-image"
      />
    </div>

    <div class="questions-container">
      <p>{{ questions.first }}</p>
      <p>{{ questions.second }}</p>
      <p>{{ questions.third }}</p>
      <p>{{ questions.fourth }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    id: Number,
  },
  data() {
    return {
      exerciseId: this.id,
      exercise_image: null,
      questions: {
        first: "",
        second: "",
        third: "",
        fourth: "",
      },
    };
  },
  mounted() {
    this.fetchExercise();
  },
  methods: {
    async fetchExercise() {
      try {
        const token = this.$store.state.token;
        const response = await axios.post(
          "http://127.0.0.1:8000/selected_discussion_exercise_data/",
          { discussion_exersice_id: this.exerciseId },
          { headers: { Authorization: `Token ${token}` } }
        );

        const exerciseData = response.data[0];
        this.exercise_image = exerciseData.image;
        this.questions.first = exerciseData.first_question;
        this.questions.second = exerciseData.second_question;
        this.questions.third = exerciseData.third_question;
        this.questions.fourth = exerciseData.fourth_question;
      } catch (error) {
        console.error("Помилка отримання даних:", error);
      }
    },

    getPhoto(imagePath) {
      try {
        if (imagePath && imagePath.startsWith("http")) {
          return imagePath;
        }
        const photoPath = imagePath.split("images/exercise_images/")[1];
        const fileName = photoPath.split("/").pop();
        return require(`@/../../backend/images/exercise_images/${fileName}`);
      } catch (error) {
        console.error("Error loading photo:", error);
        return "";
      }
    },
  },
};
</script>

<style scoped>
.exercise-form {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border-radius: 8px;
}

.exercise-title {
  text-align: center;
  margin: 0 auto 15px;
  font-size: 19px;
}

.exercise-image {
  max-width: 100%;
  border-radius: 8px;
}

.questions-container {
  font-size: 16px;
  line-height: 1.6;
  text-align: justify;
  color: #444;
}

.exercise-image {
  width: 450px;
  height: 300px;
  object-fit: cover;
  transition: opacity 0.3s ease;
}

.new-image {
  position: absolute;
  top: 25px;
  left: 0;
  width: 450px;
  height: 300px;
  object-fit: cover;
  opacity: 1;
}

.image-container {
  position: relative;
  display: inline-block;
  display: flex;
  justify-content: center;
}
.add-exercise-form {
  max-width: 600px;
  margin: auto;
  font-family: "Roboto", sans-serif;
}

h2 {
  text-align: center;
  color: #333;
  font-size: 2rem;
  margin-bottom: 20px;
}

input[type="file"] {
  width: 95%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
  font-size: 1rem;
  margin: 10px 0 20px 0;
  cursor: pointer;
}

input[type="file"]:hover {
  border-color: #007bff;
}

input[type="file"]:focus {
  border-color: #007bff;
  outline: none;
  background: #fff;
}

input[type="text"] {
  width: 95%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  margin: 10px 0;
  background: #f9f9f9;
  color: #333;
}

input[type="text"]:focus {
  border-color: #007bff;
  background: #fff;
  outline: none;
}

button {
  width: 99%;
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
