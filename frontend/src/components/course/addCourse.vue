<template>
  <div class="add-course-form">
    <h2>Додати новий курс</h2>

    <form @submit.prevent="submitCourse">
      <label for="course_name">Назва курсу:</label>
      <input v-model="course_name" type="text" id="course_name" required />

      <label for="course_description">Опис курсу:</label>
      <textarea
        v-model="course_description"
        id="course_description"
        required
      ></textarea>

      <label for="course_image">Зображення курсу:</label>
      <input
        type="file"
        id="course_image"
        @change="handleFileUpload"
        accept="image/*"
      />

      <label for="difficult_level">Рівень складності:</label>
      <select v-model="difficult_level" id="difficult_level" required>
        <option value="★">★ (Легкий)</option>
        <option value="★★">★★ (Середній)</option>
        <option value="★★★">★★★ (Важкий)</option>
      </select>

      <button type="submit">Додати курс</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      course_name: "",
      course_description: "",
      course_image: null,
      difficult_level: "★",
      token: "",
      allowedImageTypes: ["image/jpeg", "image/png", "image/gif", "image/webp"],
    };
  },
  computed: {
    ...mapGetters(["isAuthenticated"]),
  },
  mounted() {
    this.token = this.$store.state.token;
  },

  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];

      if (!file) return;

      if (!this.allowedImageTypes.includes(file.type)) {
        Swal.fire({
          icon: "error",
          title: "Непідтримуваний формат файлу",
          text: "Будь ласка, виберіть зображення у форматі JPEG, PNG, GIF або WebP.",
        });
        this.course_image = null;
        event.target.value = "";
        return;
      }

      this.course_image = file;
    },

    async submitCourse() {
      if (!this.course_image) {
        Swal.fire({
          icon: "error",
          title: "Помилка",
          text: "Будь ласка, виберіть зображення для курсу.",
        });
        return;
      }

      const formData = new FormData();
      formData.append("course_name", this.course_name);
      formData.append("course_description", this.course_description);
      formData.append("course_image", this.course_image);
      formData.append("difficult_level", this.difficult_level);

      try {
        await axios.post("http://127.0.0.1:8000/add_course/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Token ${this.token}`,
          },
        });

        Swal.fire({
          icon: "success",
          title: "Курс успішно додано!",
          confirmButtonText: "OK",
        }).then(() => {
          this.$router.push("/courses");
        });

        this.resetForm();
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Помилка",
          text: "Не вдалося додати курс. Спробуйте ще раз.",
        });
      }
    },

    resetForm() {
      this.course_name = "";
      this.course_description = "";
      this.course_image = null;
      this.difficult_level = "★";
    },
  },
};
</script>

<style scoped>
.add-course-form {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-top: 10px;
}

input,
textarea,
select {
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  margin-top: 15px;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}
</style>
