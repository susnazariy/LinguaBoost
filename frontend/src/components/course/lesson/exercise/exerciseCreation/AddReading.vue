<template>
  <div class="add-exercise-form">
    <h2>Додати Reading</h2>

    <form @submit.prevent="submitExercise">
      <label for="exercise_image">Фото:</label>
      <input
        type="file"
        id="exercise_image"
        @change="handleFileUpload"
        accept="image/*"
      />

      <div v-if="exercise_image">
        <h4>Попередній перегляд:</h4>
        <div class="image-preview">
          <img :src="imagePreview" alt="Preview" width="200" />
        </div>
      </div>

      <label for="text">Текст:</label>
      <textarea v-model="text" id="text" required></textarea>

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
      exercise_image: null,
      text: "",
      token: "",
      imagePreview: null,
    };
  },
  mounted() {
    this.token = this.$store.state.token;
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];

      if (file) {
        const allowedExtensions = ["image/jpeg", "image/png", "image/jpg"];
        if (!allowedExtensions.includes(file.type)) {
          Swal.fire(
            "Помилка!",
            "Будь ласка, виберіть зображення формату JPEG, PNG або JPG.",
            "error"
          );
          this.exercise_image = null;
          this.imagePreview = null;
          return;
        }

        this.exercise_image = file;

        this.imagePreview = URL.createObjectURL(file);
      }
    },
    async submitExercise() {
      if (!this.text.trim()) {
        Swal.fire("Помилка!", "Текст не може бути порожнім.", "error");
        return;
      }

      const lessonId = this.$route.params.id;
      const formData = new FormData();
      formData.append("lesson_id", lessonId);
      formData.append("image", this.exercise_image);
      formData.append("text", this.text);

      try {
        await axios.post(
          "http://127.0.0.1:8000/add_reading_exercise/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Token ${this.token}`,
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
      } catch (error) {
        Swal.fire("Помилка!", "Не вдалося додати вправу", "error");
      }
    },
  },
};
</script>

<style scoped>
.image-preview {
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

textarea {
  width: 95%;
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
  margin-bottom: 8px;
  color: #555;
}
</style>
