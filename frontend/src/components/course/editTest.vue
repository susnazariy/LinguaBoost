<template>
  <div>
    <div>
      <input
        v-model="newLessonName"
        type="text"
        placeholder="Назва нового заняття"
      />
      <button @click="addLesson">Додати заняття</button>
    </div>

    <div v-for="lesson in lessons" :key="lesson.id" class="lesson-item">
      <input v-model="lesson.id" type="number" disabled />
      <input v-model="lesson.newLessonName" type="text" />
      <button @click="updateLesson(lesson.id, lesson.newLessonName)">
        Оновити заняття
      </button>
      <button @click="deleteLesson(lesson.id)">Видалити заняття</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      token: "",
      courseId: null,
      lessons: [],
      newLessonName: "",
    };
  },
  computed: {
    ...mapGetters(["isAuthenticated"]),
  },
  async mounted() {
    this.token = this.$store.state.token;
    this.courseId = 5;
    if (!this.courseId) return;
    await this.fetchCourseData();
  },
  methods: {
    async fetchCourseData() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/exercises_list/",
          { lesson_id: this.courseId },
          { headers: { Authorization: `Token ${this.token}` } }
        );
        console.log(response.data);
        //   this.lessons = response.data.map((lesson) => ({
        //     id: lesson.id,
        //     newLessonName: lesson.lesson_name,
        //   }));
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Помилка",
          text: "Не вдалося завантажити дані курсу.",
        });
      }
    },
    async addLesson() {
      if (!this.newLessonName) {
        Swal.fire("Помилка", "Введіть назву нового заняття", "error");
        return;
      }
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/add_lesson/",
          { course_id: this.courseId, lesson_name: this.newLessonName },
          { headers: { Authorization: `Token ${this.token}` } }
        );
        this.lessons.push({
          id: response.data.lesson_id,
          newLessonName: this.newLessonName,
        });
        this.newLessonName = "";
        Swal.fire("Успіх", "Заняття додано", "success");
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося додати заняття", "error");
      }
    },
    async updateLesson(lessonId, newLessonName) {
      if (!lessonId || !newLessonName) {
        Swal.fire("Помилка", "Введіть ID заняття та нову назву", "error");
        return;
      }
      try {
        await axios.post(
          "http://127.0.0.1:8000/update_lesson/",
          { lesson_id: lessonId, new_lesson_name: newLessonName },
          { headers: { Authorization: `Token ${this.token}` } }
        );
        Swal.fire("Успіх", "Заняття оновлено", "success");
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося оновити заняття", "error");
      }
    },
    async deleteLesson(lessonId) {
      if (!lessonId) {
        Swal.fire("Помилка", "Введіть ID заняття", "error");
        return;
      }
      try {
        await axios.post(
          "http://127.0.0.1:8000/delete_lesson/",
          { lesson_id: lessonId },
          { headers: { Authorization: `Token ${this.token}` } }
        );
        this.lessons = this.lessons.filter((lesson) => lesson.id !== lessonId);
        Swal.fire("Успіх", "Заняття видалено", "success");
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося видалити заняття", "error");
      }
    },
  },
};
</script>
