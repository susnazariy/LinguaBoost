<template>
  <div class="page-container">
    <div v-if="loading" class="loading">Завантаження курсів...</div>
    <div v-else class="container-courses">
      <div v-for="course in courses" :key="course.id" class="course-card">
        <img :src="getPhoto(course)" alt="Course Image" class="course-image" />
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
            Почати курс
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CourseList",
  data() {
    return {
      courses: [],
      loading: true,
      baseImageUrl: "http://127.0.0.1:8000/images/course_images/",
    };
  },
  async created() {
    try {
      const response = await fetch("http://127.0.0.1:8000/courses_full_data/");
      const data = await response.json();
      this.courses = data.flatMap((teacher) => teacher.courses_info);
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
.page-container {
  display: flex;
  justify-content: center;
  margin: 50px 0;
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
  max-height: 380px;
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
