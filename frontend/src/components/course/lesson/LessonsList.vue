<template>
  <div class="lesson-container">
    <div v-for="lesson in lessons" :key="lesson.id" class="lesson-item">
      <input v-model="lesson.newLessonName" type="text" class="lesson-name" />
      <div class="lesson-links">
        <router-link
          :to="'/created-exercises/' + lesson.id"
          class="exercise-link"
        >
          Вправи
        </router-link>
        <router-link :to="'/created-tests/' + lesson.id" class="test-link">
          Тести
        </router-link>
      </div>
      <button
        class="update-btn"
        @click="updateLesson(lesson.id, lesson.newLessonName)"
      >
        <i class="fa-solid fa-check"></i>
      </button>

      <button class="delete-btn" @click="confirmDelete(lesson.id)">
        <i class="fa-solid fa-trash"></i>
      </button>
    </div>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h2>Додати заняття</h2>
        <input
          v-model="newLessonName"
          type="text"
          placeholder="Назва нового заняття"
        />
        <div class="modal-actions">
          <button class="save-btn" @click="addLesson">Зберегти</button>
          <button class="cancel-btn" @click="closeModal">Скасувати</button>
        </div>
      </div>
    </div>
    <button class="add-btn" @click="openModal">Додати заняття</button>
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
      showModal: false,
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
          "http://127.0.0.1:8000/lessons_list/",
          {
            course_id: this.courseId,
          },
          { headers: { Authorization: `Token ${this.token}` } }
        );
        this.lessons = response.data.map((lesson) => ({
          id: lesson.id,
          newLessonName: lesson.lesson_name,
        }));
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося завантажити заняття", "error");
      }
    },
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.newLessonName = "";
    },
    async addLesson() {
      if (!this.newLessonName) {
        Swal.fire("Помилка", "Введіть назву нового заняття", "error");
        return;
      }
      try {
        await axios.post(
          "http://127.0.0.1:8000/add_lesson/",
          { course_id: this.courseId, lesson_name: this.newLessonName },
          { headers: { Authorization: `Token ${this.token}` } }
        );

        this.newLessonName = "";
        this.showModal = false;

        await this.fetchCourseData();

        Swal.fire("Успіх", "Заняття додано", "success");
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося додати заняття", "error");
      }
    },
    async updateLesson(lessonId, newLessonName) {
      try {
        await axios.post(
          "http://127.0.0.1:8000/update_lesson/",
          {
            lesson_id: lessonId,
            new_lesson_name: newLessonName,
          },
          { headers: { Authorization: `Token ${this.token}` } }
        );
        Swal.fire("Успіх", "Заняття оновлено", "success");
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося оновити заняття", "error");
      }
    },
    confirmDelete(lessonId) {
      Swal.fire({
        title: "Ви впевнені?",
        text: "Цю дію не можна скасувати!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Так, видалити",
        cancelButtonText: "Скасувати",
      }).then(async (result) => {
        if (result.isConfirmed) {
          await this.deleteLesson(lessonId);
        }
      });
    },
    async deleteLesson(lessonId) {
      try {
        await axios.post(
          "http://127.0.0.1:8000/delete_lesson/",
          {
            lesson_id: lessonId,
          },
          { headers: { Authorization: `Token ${this.token}` } }
        );
        this.lessons = this.lessons.filter((lesson) => lesson.id !== lessonId);
        Swal.fire({
          icon: "success",
          title: "Заняття успішно видалено!",
          timer: 1500,
        });
      } catch (error) {
        Swal.fire("Помилка", "Не вдалося видалити заняття", "error");
      }
    },
  },
};
</script>

<style scoped>
.lesson-container {
  box-sizing: border-box;
  width: 800px;
  margin: 20px auto;
  padding: 40px 0 40px 40px;
}

.lesson-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background 0.3s ease;
  gap: 25px;
}

.lesson-item:hover {
  background: #e8f0fe;
}

.lesson-id {
  width: 30px;
  font-size: 14px;
  border: 1px solid #ddd;
  padding: 8px;
  background-color: #f1f1f1;
  border-radius: 6px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.lesson-name {
  flex-grow: 1;
  font-size: 14px;
  border: 1px solid #ddd;
  padding: 8px;
  background-color: #f1f1f1;
  border-radius: 6px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  font-weight: bold;
  color: #333;
}

.lesson-links {
  display: flex;
  gap: 25px;
}

.lesson-links a {
  font-size: 16px;
  font-weight: bold;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.exercise-link {
  color: #27ae60;
  background: rgba(39, 174, 96, 0.1);
  border: 2px solid #27ae60;
}

.exercise-link:hover {
  color: white;
  background: #27ae60;
}

.test-link {
  font-size: 18px;
  font-weight: bold;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
  color: #3498db;
  background: rgba(52, 152, 219, 0.1);
  border: 2px solid #3498db;
}

.test-link:hover {
  color: white;
  background: #3498db;
}

.update-btn {
  background: #3498db;
  color: white;
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s;
}

.update-btn:hover {
  background-color: #2980b9;
}

.delete-btn {
  background: #e74c3c;
  color: white;
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s;
}

.delete-btn:hover {
  background-color: #c0392b;
}

.add-btn {
  background: #27ae60;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  margin: 30px auto;
}

.add-btn:hover {
  background-color: #2ecc71;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  width: 500px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
  text-align: center;
}
.modal-content input {
  font-size: 16px;
  width: 300px;
  padding: 10px;
  border-radius: 5px;
}

.modal-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
  justify-content: center;
}

.save-btn,
.cancel-btn {
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  border: none;
  font-size: 16px;
}

.save-btn {
  background-color: #27ae60;
  color: white;
}

.cancel-btn {
  background-color: #e74c3c;
  color: white;
}

.save-btn:hover {
  background-color: #2ecc71;
}

.cancel-btn:hover {
  background-color: #c0392b;
}
</style>
