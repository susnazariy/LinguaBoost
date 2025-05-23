<template>
  <div class="exercise-form">
    <h3 class="exercise-title">Warm-up / Discussion</h3>

    <div v-if="exercise_image" class="image-container">
      <img
        :src="getPhoto(exercise_image)"
        alt="Exercise Image"
        class="exercise-image"
        :style="{ opacity: new_image_url ? 0 : 1 }"
      />

      <img
        v-if="new_image_url"
        :src="new_image_url"
        alt="New Exercise Image"
        class="exercise-image new-image"
      />
    </div>

    <div>
      <label for="new_image">Завантажити нове фото:</label>
      <input
        type="file"
        id="new_image"
        @change="handleImageUpload"
        accept="image/*"
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

    <div class="buttons">
      <button @click="updateExercise" class="submit-btn">Оновити</button>
      <button @click="deleteExercise" class="delete-exer-btn">
        <i class="fa fa-trash"></i> Видалити
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
      exerciseId: null,
      exercise_image: null,
      new_image: null,
      new_image_url: null,
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
        this.exerciseId = this.$route.params.id;

        const token = this.$store.state.token;
        const response = await axios.post(
          "http://127.0.0.1:8000/selected_discussion_exercise_data/",
          {
            discussion_exersice_id: this.exerciseId,
          },
          {
            headers: { Authorization: `Token ${token}` },
          }
        );

        const exerciseData = response.data[0];
        this.exercise_image = exerciseData.image;
        this.questions.first = exerciseData.first_question;
        this.questions.second = exerciseData.second_question;
        this.questions.third = exerciseData.third_question;
        this.questions.fourth = exerciseData.fourth_question;
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося завантажити вправу", "error");
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

    handleImageUpload(event) {
      const file = event.target.files[0];

      if (file) {
        const allowedExtensions = ["image/jpeg", "image/png", "image/jpg"];
        if (!allowedExtensions.includes(file.type)) {
          Swal.fire(
            "Помилка!",
            "Будь ласка, виберіть зображення формату JPEG, PNG або JPG.",
            "error"
          );
          this.new_image = null;
          return;
        }

        this.new_image = file;
        this.new_image_url = URL.createObjectURL(file);
      }
    },

    async updateExercise() {
      if (
        !this.questions.first.trim() ||
        !this.questions.second.trim() ||
        !this.questions.third.trim() ||
        !this.questions.fourth.trim()
      ) {
        Swal.fire("Помилка", "Всі питання повинні бути заповнені", "error");
        return;
      }

      const formData = new FormData();
      formData.append("discussion_exercise_id", this.exerciseId);
      formData.append("new_first_question", this.questions.first);
      formData.append("new_second_question", this.questions.second);
      formData.append("new_third_question", this.questions.third);
      formData.append("new_fourth_question", this.questions.fourth);

      if (this.new_image) {
        formData.append("new_image", this.new_image);
      }

      try {
        const token = this.$store.state.token;
        await axios.post(
          "http://127.0.0.1:8000/update_discussion_exercise/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Token ${token}`,
            },
          }
        );

        Swal.fire("Успіх", "Вправа успішно оновлена!", "success");
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося оновити вправу", "error");
        console.error("Помилка оновлення:", error);
      }
    },

    async deleteExercise() {
      const token = this.$store.state.token;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/delete_discussion_exercise/",
          { discussion_exercise_id: this.exerciseId },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );

        if (response.data === "Discussion exercise successfully deleted!") {
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
.exercise-image {
  width: 450px;
  height: 300px;
  object-fit: cover;
  transition: opacity 0.3s ease;
}

.new-image {
  position: absolute;
  top: 25px;
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
  width: 100%;
  box-sizing: border-box;
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

label {
  display: block;
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 8px;
  color: #555;
}
</style>
