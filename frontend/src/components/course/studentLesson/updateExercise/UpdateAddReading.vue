<template>
  <div class="exercise-view">
    <h3 class="exercise-title">Reading</h3>

    <div v-if="exercise_image" class="image-container">
      <img
        :src="getPhoto(exercise_image)"
        alt="Exercise Image"
        class="exercise-image"
      />
    </div>

    <div class="exercise-text">
      <p>{{ text }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      exerciseId: null,
      exercise_image: null,
      text: "",
    };
  },
  mounted() {
    this.fetchExercise();
  },
  methods: {
    async fetchExercise() {
      try {
        this.exerciseId = this.$route.params.id;
        const token = this.$store.state.token;
        const response = await axios.post(
          "http://127.0.0.1:8000/selected_reading_exercise_data/",
          { reading_exersice_id: this.exerciseId },
          { headers: { Authorization: `Token ${token}` } }
        );

        const exerciseData = response.data[0];
        this.exercise_image = exerciseData.image;
        this.text = exerciseData.text;
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
.exercise-view {
  padding: 20px;
}
.exercise-title {
  text-align: center;
  margin: 0 auto 15px;
  font-size: 19px;
}
.image-container {
  margin-bottom: 15px;
  display: flex;
  justify-content: center;
}
.exercise-image {
  max-width: 450px;
  width: 100%;
  height: auto;
  border-radius: 8px;
}
.exercise-text p {
  padding: 10px 0 0;
  border-radius: 5px;
  font-size: 16px;
  line-height: 1.5;
  color: #444;
  text-align: justify;
}
</style>
