<template>
  <div class="page-container">
    <div v-if="loading" class="loading">Завантаження курсів...</div>
    <div v-else class="container-courses">
      <div v-for="course in courses" :key="course.id" class="course-card">
        <div class="image-container">
          <img
            :src="getPhoto(course)"
            alt="Course Image"
            class="course-image"
          />
          <button @click="confirmDelete(course.id)" class="delete-course-btn">
            <i class="fa fa-trash"></i>
          </button>
        </div>
        <div class="course-info">
          <h3 class="course-title">{{ course.course_name }}</h3>
          <div class="course-details">
            <div class="detail-item">
              <i class="fa fa-calendar"></i> {{ course.creation_date }}
            </div>
            <div class="detail-item">
              Рівень складності {{ course.difficult_level }}
            </div>
          </div>
          <router-link :to="`/course/${course.id}`" class="start-course-btn">
            Перейти до курсу
          </router-link>
          <router-link
            :to="`/change-course/${course.id}/edit`"
            class="edit-course-btn"
          >
            Редагувати курс
          </router-link>
        </div>
      </div>

      <router-link to="/add-course" class="course-card add-course-card">
        <div class="add-course-content">
          <span class="plus-icon">+</span>
          <span>Додати курс</span>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  computed: {
    ...mapGetters(["isAuthenticated"]),
  },
  name: "CourseList",
  data() {
    return {
      courses: [],
      loading: true,
      baseImageUrl: "http://127.0.0.1:8000/images/course_images/",
    };
  },
  created() {
    this.fetchCourses();
  },
  methods: {
    getPhoto(course) {
      try {
        const photoPath = course.course_image.split("images/course_images/")[1];
        const fileName = photoPath.split("/").pop();
        return require(`@/../../backend/images/course_images/${fileName}`);
      } catch (error) {
        console.error("Error loading photo:", error);
        return "";
      }
    },
    async fetchCourses() {
      this.loading = true;
      try {
        const token = this.$store.state.token;
        const response = await axios.get(
          "http://127.0.0.1:8000/profile_teacher_courses/",
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );
        this.courses = response.data;
      } catch (error) {
        console.error("Помилка завантаження курсів:", error);
      } finally {
        this.loading = false;
      }
    },
    confirmDelete(courseId) {
      Swal.fire({
        title: "Ви впевнені?",
        text: "Цю дію не можна скасувати!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Так, видалити",
        cancelButtonText: "Скасувати",
      }).then(async (result) => {
        if (result.isConfirmed) {
          await this.deleteCourse(courseId);
        }
      });
    },
    async deleteCourse(courseId) {
      const token = this.$store.state.token;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/delete_course/",
          { course_id: courseId },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );

        if (response.data === "Course successfully deleted!") {
          await this.fetchCourses();
          Swal.fire({
            icon: "success",
            title: "Курс успішно видалено!",
            timer: 1500,
          });
        } else if (response.data === "Delete course error!") {
          Swal.fire({
            icon: "error",
            title: "Помилка!",
            text: "Не вдалося видалити курс.",
          });
        } else {
          Swal.fire({
            icon: "error",
            title: "Помилка!",
            text: "Не вдалося видалити курс.",
          });
        }
      } catch (error) {
        console.error("Помилка при видаленні курсу:", error);
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
.image-container {
  position: relative;
  display: flex;
  justify-content: center;
}

.delete-course-btn {
  background-color: transparent;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: #e74c3c;
  position: absolute;
  top: 10px;
  right: 10px;
}

.delete-course-btn:hover {
  transform: scale(1.1);
}

.delete-course-btn i {
  font-size: 24px;
}

.course-card {
  position: relative;
  border: 1px solid #ddd;
  border-radius: 10px;
  overflow: hidden;
}

.course-info {
  padding: 20px;
}

.container-courses {
  max-width: 1100px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 50px;
  justify-items: center;
}

@media (max-width: 1550px) {
  .container-courses {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1200px) {
  .container-courses {
    grid-template-columns: repeat(1, 1fr);
  }
}

.add-course-card {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f4f4f4;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
}

.plus-icon {
  font-size: 30px;
  color: #2ecc71;
}

.add-course-content {
  font-size: 18px;
  color: #2ecc71;
}

.page-container {
  display: flex;
  justify-content: center;
  background: #f8f9fa;
  padding: 10px 0;
}

.course-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
  text-align: center;
  padding-bottom: 10px;
  width: 320px;
}

.course-card:hover {
  transform: translateY(-5px);
}

.course-image {
  width: 320px;
  height: 180px;
  object-fit: cover;
}

.course-info {
  padding: 15px 20px;
}

.course-title {
  font-size: 20px;
  font-weight: bold;
  margin: 10px;
}

.course-details {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-size: 14px;
  color: #666;
  padding: 5px 0;
}

.detail-item {
  text-align: left;
  gap: 5px;
}

.course-details .detail-item:nth-of-type(2) {
  text-align: right;
}

.start-course-btn {
  display: block;
  margin: 15px auto 0;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: background 0.3s ease;
}

.start-course-btn:hover {
  background-color: #0056b3;
}

.add-course-card {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 320px;
  height: 180px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  font-size: 20px;
  font-weight: bold;
  color: #007bff;
  border: 2px dashed #007bff;
  transition: background 0.3s ease, transform 0.3s ease;
}

.add-course-card:hover {
  background: #e6f0ff;
  transform: translateY(-5px);
}

.add-course-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.plus-icon {
  font-size: 40px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #007bff;
}
.edit-course-btn {
  display: block;
  margin: 10px auto;
  padding: 8px 15px;
  background-color: #28a745;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: background 0.3s ease;
}

.edit-course-btn:hover {
  background-color: #218838;
}
.delete-course-btn {
  display: block;
  margin: 10px auto;
  padding: 8px 15px;
  background-color: #dc3545;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: background 0.3s ease;
}

.delete-course-btn:hover {
  background-color: #c82333;
}
</style>
