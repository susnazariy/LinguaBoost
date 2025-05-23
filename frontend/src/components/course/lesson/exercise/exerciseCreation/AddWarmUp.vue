<template>
  <div class="add-exercise-form">
    <h2>Додати Discussion</h2>

    <form @submit.prevent="submitExercise">
      <label for="exercise_image">Фото:</label>
      <input
        type="file"
        id="exercise_image"
        @change="handleFileUpload"
        accept="image/*"
      />

      <div class="image-preview" v-if="exercise_image_preview">
        <img
          :src="exercise_image_preview"
          alt="Попередній перегляд"
          class="preview-image"
        />
      </div>

      <div>
        <label for="first_question">Перше питання:</label>
        <input
          v-model="questions.first"
          type="text"
          id="first_question"
          required
        />
      </div>

      <div>
        <label for="second_question">Друге питання:</label>
        <input
          v-model="questions.second"
          type="text"
          id="second_question"
          required
        />
      </div>

      <div>
        <label for="third_question">Третє питання:</label>
        <input
          v-model="questions.third"
          type="text"
          id="third_question"
          required
        />
      </div>

      <div>
        <label for="fourth_question">Четверте питання:</label>
        <input
          v-model="questions.fourth"
          type="text"
          id="fourth_question"
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
      lessonId: "",
      exercise_image: null,
      exercise_image_preview: null,
      questions: {
        first: "",
        second: "",
        third: "",
        fourth: "",
      },
      token: "",
    };
  },
  mounted() {
    this.token = this.$store.state.token;
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file && file.type.startsWith("image/")) {
        this.exercise_image = file;
        this.exercise_image_preview = URL.createObjectURL(file);
      } else {
        Swal.fire({
          icon: "error",
          title: "Невірний формат",
          text: "Будь ласка, виберіть зображення.",
        });
        this.exercise_image = null;
        this.exercise_image_preview = null;
      }
    },
    async submitExercise() {
      if (
        !this.questions.first ||
        !this.questions.second ||
        !this.questions.third ||
        !this.questions.fourth
      ) {
        Swal.fire("Помилка", "Будь ласка, заповніть усі питання", "warning");
        return;
      }

      if (
        this.questions.first === this.questions.second ||
        this.questions.first === this.questions.third ||
        this.questions.first === this.questions.fourth ||
        this.questions.second === this.questions.third ||
        this.questions.second === this.questions.fourth ||
        this.questions.third === this.questions.fourth
      ) {
        Swal.fire("Помилка", "Питання повинні бути унікальними", "warning");
        return;
      }
      const lessonId = this.$route.params.id;

      const formData = new FormData();
      formData.append("lesson_id", lessonId);
      formData.append("image", this.exercise_image);
      formData.append("first_question", this.questions.first);
      formData.append("second_question", this.questions.second);
      formData.append("third_question", this.questions.third);
      formData.append("fourth_question", this.questions.fourth);

      try {
        await axios.post(
          "http://127.0.0.1:8000/add_discussion_exercise/",
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

        this.resetForm();
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Помилка",
          text: "Не вдалося додати вправу. Спробуйте ще раз.",
        });
      }
    },
    resetForm() {
      this.lessonId = "";
      this.exercise_image = null;
      this.exercise_image_preview = null;
      this.questions = {
        first: "",
        second: "",
        third: "",
        fourth: "",
      };
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

label {
  display: block;
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 8px;
  color: #555;
}
</style>
