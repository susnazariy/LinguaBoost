<template>
  <div class="page-container">
    <div v-if="loading" class="loading">Завантаження курсів...</div>
    <div v-else>
      <div v-if="courses.length > 0" class="container-courses">
        <div v-for="course in courses" :key="course.id" class="course-card">
          <img
            :src="getPhoto(course)"
            alt="Course Image"
            class="course-image"
          />
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
          </div>
        </div>
      </div>

      <div v-else class="no-courses">
        <img src="../../../assets/nothing.webp" class="no-image" />
        <p>Курсів немає.</p>
        <router-link to="/courses">
          <i class="fas fa-plus-circle"></i> Залишити заявку на курс
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios";

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
  async created() {
    const token = this.$store.state.token;
    this.token = this.$store.state.token;
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/profile_student_courses/",
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
  },
};
</script>

<style scoped>
.no-courses {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.no-courses a {
  text-decoration: none;
  background: #007bff;
  color: white;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 5px;
  transition: background 0.3s ease-in-out;
  cursor: pointer;
}

.no-courses a:hover {
  color: black;
  background: white;
}
.no-image {
  width: 300px;
  height: 300px;
  object-fit: cover;
  transform: scale(1.3);
}
.page-container {
  display: flex;
  justify-content: center;
  background: #f8f9fa;
  padding: 10px 0;
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

@media (max-width: 1000px) {
  .container-courses {
    grid-template-columns: repeat(1, 1fr);
  }
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
</style>
