<template>
  <main class="edit-course-form">
    <h2>Редагувати курс</h2>
    <form @submit.prevent="submitCourse">
      <label for="course_name">Назва курсу:</label>
      <input v-model="course_name" type="text" id="course_name" required />

      <label for="course_description">Опис курсу:</label>
      <textarea
        v-model="course_description"
        id="course_description"
        required
        rows="4"
      ></textarea>

      <label for="course_image">Зображення курсу:</label>
      <input
        type="file"
        id="course_image"
        accept="image/png, image/jpeg, image/gif"
        @change="handleFileUpload"
      />

      <img
        :src="course_image_preview || getPhoto(course_image)"
        alt="Попередній перегляд"
        class="preview-image"
      />

      <label for="difficult_level">Рівень складності:</label>
      <select v-model="difficult_level" id="difficult_level" required>
        <option value="★">★ (Легкий)</option>
        <option value="★★">★★ (Середній)</option>
        <option value="★★★">★★★ (Важкий)</option>
      </select>

      <button type="submit">Зберегти зміни</button>
    </form>
  </main>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      course_id: "",
      course_name: "",
      course_description: "",
      course_image: null,
      course_image_preview: "",
      difficult_level: "★",
      token: "",
      courseId: null,
    };
  },
  computed: {
    ...mapGetters(["isAuthenticated"]),
  },
  async mounted() {
    this.token = this.$store.state.token;
    this.courseId = this.$route.params.id;
    if (!this.courseId) return;
    await this.fetchCourseData();
  },
  methods: {
    async fetchCourseData() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/selected_course_data/",
          { course_id: this.courseId },
          { headers: { Authorization: `Token ${this.token}` } }
        );
        if (response.data.length > 0) {
          const course = response.data[0];
          this.course_id = course.id || "";
          this.course_name = course.course_name || "";
          this.course_image = course.course_image || "";
          this.course_description = course.course_description || "";
          this.difficult_level = course.difficult_level || "★";
        }
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Помилка",
          text: "Не вдалося завантажити дані курсу.",
        });
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const allowedTypes = ["image/jpeg", "image/png", "image/gif"];
      const maxSize = 2 * 1024 * 1024;

      if (!allowedTypes.includes(file.type)) {
        Swal.fire({
          icon: "error",
          title: "Неправильний формат файлу",
          text: "Будь ласка, завантажте зображення у форматі JPG, PNG або GIF.",
        });
        return;
      }

      if (file.size > maxSize) {
        Swal.fire({
          icon: "error",
          title: "Файл завеликий",
          text: "Максимальний розмір файлу – 2MB.",
        });
        return;
      }

      this.course_image_preview = URL.createObjectURL(file);
      this.course_image = file;
    },
    async submitCourse() {
      const formData = new FormData();
      formData.append("course_id", this.course_id);
      formData.append("new_course_name", this.course_name);
      formData.append("new_description", this.course_description);
      formData.append("new_image", this.course_image);
      formData.append("new_difficult_level", this.difficult_level);
      try {
        await axios.post("http://127.0.0.1:8000/update_course/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Token ${this.token}`,
          },
        });
        Swal.fire({
          icon: "success",
          title: "Курс успішно відредаговано!",
          confirmButtonText: "OK",
        }).then(() => {
          this.$router.push("/courses");
        });
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Помилка",
          text: "Не вдалося відредагувати курс.",
        });
      }
    },
    getPhoto(course_image) {
      try {
        return require(`@/../../backend/images/course_images/${course_image
          .split("/")
          .pop()}`);
      } catch (error) {
        return "";
      }
    },
  },
};
</script>

<style scoped>
.preview-image {
  max-width: 200px;
  margin-top: 10px;
  display: block;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.edit-course-form {
  box-sizing: border-box;
  width: 800px;
  margin: 0 auto;
  padding: 30px;
  height: 80vh;
  overflow-y: auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-top: 10px;
  color: #555;
}

input,
textarea,
select {
  padding: 12px;
  margin-top: 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s ease-in-out;
}

input:focus,
textarea:focus,
select:focus {
  border-color: #007bff;
  outline: none;
}

textarea {
  resize: vertical;
  min-height: 100px;
  height: 150px;
}

button {
  padding: 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
  font-size: 16px;
}

button:hover {
  background-color: #0056b3;
}

button:focus {
  outline: none;
}
</style>
