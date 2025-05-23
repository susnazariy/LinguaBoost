<template>
  <div class="exercise-form">
    <h3 class="exercise-title">Listening</h3>

    <div v-if="oldAudioUrl">
      <label>Старий аудіо:</label>
      <audio :src="oldAudioUrl" controls />
    </div>

    <div v-if="audioUrl">
      <label>Новий аудіо:</label>
      <audio :src="audioUrl" controls />
    </div>

    <div>
      <label for="audio">Новий аудіо файл:</label>
      <input
        type="file"
        id="audio"
        @change="handleFileUpload"
        accept="audio/*"
      />
    </div>

    <div>
      <label for="name">Назва:</label>
      <input v-model="name" id="name" type="text" required />
    </div>

    <div>
      <label for="text">Текст:</label>
      <textarea v-model="text" id="text" required></textarea>
    </div>
    <div class="buttons">
      <button @click="updateExercise" class="submit-btn">Оновити вправу</button>
      <button @click="deleteExercise" class="delete-exer-btn">
        <i class="fa fa-trash"></i> Видалити вправу
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      audio: null,
      text: "",
      name: "",
      token: "",
      audioUrl: null,
      oldAudioUrl: null,
      exerciseId: null,
    };
  },
  mounted() {
    this.token = this.$store.state.token;
    this.fetchExercise();
  },
  methods: {
    async fetchExercise() {
      this.exerciseId = this.$route.params.id;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/selected_listening_exercise_data/",
          { listening_exersice_id: this.exerciseId },
          {
            headers: {
              Authorization: `Token ${this.token}`,
            },
          }
        );

        const exerciseData = response.data[0];
        this.oldAudioUrl = this.getAudioUrl(exerciseData.audio);
        this.text = exerciseData.text;
        this.name = exerciseData.name;
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося завантажити вправу", "error");
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

    handleFileUpload(event) {
      const newAudio = event.target.files[0];

      if (newAudio) {
        this.audio = newAudio;
        this.audioUrl = URL.createObjectURL(this.audio);
      }
    },
    async updateExercise() {
      if (!this.text.trim()) {
        Swal.fire("Помилка", "Текст не може бути порожнім", "error");
        return;
      }

      const formData = new FormData();
      formData.append("listening_exercise_id", this.exerciseId);
      formData.append("new_name", this.name);
      formData.append("new_text", this.text);
      formData.append("new_audio", this.audio);

      try {
        await axios.post(
          "http://127.0.0.1:8000/update_listening_exercise/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Token ${this.token}`,
            },
          }
        );

        Swal.fire("Успіх", "Вправа успішно оновлена!", "success");
        this.fetchExercise();

        this.oldAudioUrl = null;
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося оновити вправу", "error");
        console.error("Помилка оновлення:", error);
      }
    },

    async deleteExercise() {
      const confirmed = await Swal.fire({
        title: "Ви впевнені?",
        text: "Цю вправу буде видалено!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Так, видалити",
        cancelButtonText: "Скасувати",
      });

      if (!confirmed.isConfirmed) {
        return;
      }

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/delete_listening_exercise/",
          { listening_exercise_id: this.exerciseId },
          {
            headers: {
              Authorization: `Token ${this.token}`,
            },
          }
        );

        if (response.data === "Listening exercise successfully deleted!") {
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
  font-family: "Roboto", sans-serif;
}

h2 {
  text-align: center;
  color: #333;
  font-size: 2rem;
  margin-bottom: 20px;
}

audio {
  width: 100%;
  box-sizing: border-box;
  margin: 20px 0;
}

input[type="file"] {
  width: 100%;
  box-sizing: border-box;
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

textarea {
  min-height: 150px;
  max-height: 300px;
  overflow-y: hidden;
  width: 100%;
  box-sizing: border-box;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  margin: 10px 0;
  background: #f9f9f9;
  color: #333;
  resize: vertical;
}

textarea:focus {
  border-color: #007bff;
  background: #fff;
  outline: none;
}

label {
  display: block;
  font-size: 1rem;
  font-weight: bold;
  margin: 10px 0;
  color: #555;
}
</style>
