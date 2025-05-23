<template>
  <div class="exercise-view">
    <h3 class="exercise-title">Прослуховування Listening</h3>

    <div class="audio" v-if="oldAudioUrl">
      <audio :src="oldAudioUrl" controls />
    </div>

    <div class="exercise-text">
      <p>{{ text }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      text: "",
      oldAudioUrl: null,
      exerciseId: null,
    };
  },
  watch: {
    id: {
      immediate: true,
      handler(newId) {
        this.exerciseId = newId;
        if (newId) {
          this.fetchExercise();
        }
      },
    },
  },
  mounted() {
    this.fetchExercise();
  },
  methods: {
    async fetchExercise() {
      try {
        const token = this.$store.state.token;

        const response = await axios.post(
          "http://127.0.0.1:8000/selected_listening_exercise_data/",
          { listening_exersice_id: this.exerciseId },
          {
            headers: { Authorization: `Token ${token}` },
          }
        );

        const exerciseData = response.data[0];
        this.oldAudioUrl = this.getAudioUrl(exerciseData.audio);
        this.text = exerciseData.text;
      } catch (error) {
        console.error("Помилка при отриманні даних:", error);
      }
    },

    getAudioUrl(audioPath) {
      try {
        if (audioPath && audioPath.startsWith("http")) {
          return audioPath;
        }

        const audioFilePath = audioPath.split("audio/")[1];
        const fileName = audioFilePath.split("/").pop();
        return require(`@/../../backend/audio/${fileName}`);
      } catch (error) {
        console.error("Помилка при завантаженні аудіо:", error);
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
.audio audio {
  width: 100%;
}
.audio {
  margin-bottom: 10px;
}
.exercise-view {
  max-width: 600px;
  margin: auto;
  font-family: "Roboto", sans-serif;
}

h3 {
  text-align: center;
  color: #333;
  font-size: 1.8rem;
  margin-bottom: 20px;
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
