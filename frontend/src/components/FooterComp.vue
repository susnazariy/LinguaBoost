<template>
  <footer class="footer">
    <div class="container-foot">
      <div class="footer-content">
        <div class="footer-column">
          <p class="slogan">Навчайся разом з LinguaBoost!</p>
          <div class="social-links">
            <a :href="website_facebook" target="_blank"
              ><i class="fab fa-facebook"></i
            ></a>
            <a :href="website_linkedin" target="_blank"
              ><i class="fab fa-linkedin"></i
            ></a>
            <a :href="website_instagram" target="_blank"
              ><i class="fab fa-instagram"></i
            ></a>
          </div>
        </div>
        <div class="footer-column">
          <h3>Найновіші курси</h3>
          <ul>
            <li v-if="loading">Завантаження курсів...</li>
            <li v-else v-for="course in courses" :key="course.id">
              <router-link :to="`/course/${course.id}`">
                {{ course.course_name }}
              </router-link>
            </li>
          </ul>
        </div>
        <div class="footer-column">
          <h3>Сторінки</h3>
          <ul>
            <li><router-link to="/">Головна</router-link></li>
            <li><router-link to="/courses">Курси</router-link></li>
            <li><router-link to="/contacts">Контакти</router-link></li>
          </ul>
        </div>
      </div>
      <div class="footer-line"></div>
      <div class="footer-bottom">
        <p>2025 LinguaBoost. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "FooterComp",
  data() {
    return {
      courses: [],
      loading: true,
      website_facebook: "",
      website_linkedin: "",
      website_instagram: "",
    };
  },
  async created() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch("http://127.0.0.1:8000/home/");
        const data = await response.json();
        if (data.length > 0) {
          this.website_facebook = data[0].website_facebook;
          this.website_linkedin = data[0].website_linkedin;
          this.website_instagram = data[0].website_instagram;
        }
        const coursesResponse = await fetch(
          "http://127.0.0.1:8000/courses_full_data/"
        );
        const coursesData = await coursesResponse.json();
        this.courses = coursesData
          .flatMap((teacher) => teacher.courses_info)
          .sort((a, b) => new Date(b.creation_date) - new Date(a.creation_date))
          .slice(0, 3);
      } catch (error) {
        console.error("Помилка завантаження даних:", error);
      } finally {
        this.loading = false;
      }
    },
  },
  watch: {
    "$route.params.courseId": "fetchData",
  },
};
</script>

<style scoped>
.footer {
  background: linear-gradient(to top, #13347a, #2562e8);
  padding: 20px 30px;
  text-align: center;
  color: white;
}

.container-foot {
  max-width: 1100px;
  margin: 0 auto;
  gap: 70px;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.footer-column {
  flex: 1;
  min-width: 200px;
}

.footer-column p {
  font-style: normal;
  font-weight: 400;
  font-size: 18px;
  line-height: 24px;
  color: #ffffff;
  padding-bottom: 20px;
}

.slogan {
  font-weight: bold;
  margin-bottom: 10px;
}

.social-links a {
  margin: 0 10px;
  font-size: 1.2rem;
  color: white;
  transition: color 0.3s;
}

.social-links a:hover {
  color: #ffcc00;
}

.footer-column h3 {
  margin-bottom: 10px;
  font-style: normal;
  font-weight: 700;
  font-size: 20px;
  line-height: 24px;
  color: #ffffff;
}

.footer-bottom .slogan {
  font-style: normal;
  font-weight: 600;
  font-size: 16px;
  line-height: 18px;
  letter-spacing: 0.8px;
  color: #ffffff;
}

.footer-column ul {
  list-style: none;
  padding: 0;
}

.footer-column ul li {
  margin-bottom: 5px;
}

.footer-column ul li a {
  text-decoration: none;
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 21px;
  color: #ffffff;
  transition: color 0.3s;
}

.footer-column ul li a:hover {
  color: #ffcc00;
}

.footer-line {
  width: 100%;
  height: 1px;
  background-color: white;
  margin: 15px 0;
}
</style>
