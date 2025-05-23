<template>
  <header class="header">
    <div class="container-head">
      <div class="logo">LinguaBoost</div>
      <nav class="nav">
        <router-link to="/">Головна</router-link>
        <router-link to="/courses">Курси</router-link>
        <router-link to="/contacts">Контакти</router-link>
      </nav>
      <div class="profile" @click="goToProfile">
        <i class="fas fa-user"></i>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  data() {
    return {
      isAuthenticated: false,
      account_type: null,
    };
  },
  name: "HeaderComp",
  computed: {
    isLoggedIn() {
      return localStorage.getItem("auth_token") !== null;
    },
  },
  methods: {
    goToProfile() {
      if (this.isLoggedIn) {
        if (this.account_type === "Викладач") {
          this.$router.push("/profile-teacher/courses");
        } else if (this.account_type === "Учень") {
          this.$router.push("/profile-student/courses");
        } else {
          this.$router.push("/profile-admin/link");
        }
      } else {
        this.$router.push("/login");
      }
    },
  },
  mounted() {
    const token = localStorage.getItem("auth_token");
    if (token) {
      this.account_type = localStorage.getItem("account_type");
      this.isAuthenticated = true;
    }
  },
};
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: white;
  padding: 15px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.container-head {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
}

.nav {
  display: flex;
  gap: 50px;
}

.nav a {
  text-decoration: none;
  font-family: "Open Sans";
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 24px;
  text-align: center;
  color: #404040;
}

.nav a:hover,
.profile:hover {
  color: #0065f4;
}

.profile {
  font-size: 1.5rem;
  cursor: pointer;
}
</style>
