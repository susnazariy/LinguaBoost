<template>
  <div class="container-reg">
    <div class="container-left">
      <p>Ласкаво просимо, ми раді Вас тут знову бачити!</p>
    </div>
    <div class="login-container">
      <div class="login-form">
        <h2>Вхід</h2>
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <input
              type="text"
              id="login-username"
              v-model="username"
              :class="{ 'input-field': true, error: !isValidUsername }"
              placeholder="Введіть логін"
            />
            <div class="error-message" v-if="showUsernameError">
              {{ usernameErrorMessage }}
            </div>
          </div>
          <div class="form-group">
            <input
              type="password"
              id="login-password"
              v-model="password"
              class="input-field"
              placeholder="Введіть пароль"
            />
            <div class="error-message" v-if="showPasswordError">
              {{ passwordErrorMessage }}
            </div>
          </div>
          <div class="form-actions gap-bot">
            <button type="submit" @click="login" class="login-button">
              Увійти
            </button>
          </div>
        </form>
        <div class="line"></div>
        <div class="have-account">
          Немає аккаунту? <a href="#/register">Реєстрація</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";

export default {
  mounted() {
    if (localStorage.getItem("auth_token")) {
      localStorage.removeItem("auth_token");
      window.location.reload();
    }
  },
  data() {
    return {
      username: "",
      password: "",
      showUsernameError: false,
      showPasswordError: false,
      usernameErrorMessage: "Логін порожній",
      passwordErrorMessage: "Пароль порожній",
    };
  },
  computed: {
    isValidUsername() {
      return /^[a-zA-Z0-9_]+$/.test(this.username);
    },
  },
  methods: {
    parseData(data) {
      const parsedData = {};
      data[0].forEach((item) => {
        const [key, value] = item.split(":").map((str) => str.trim());
        parsedData[key] = value;
      });
      return parsedData;
    },
    login() {
      this.showUsernameError = false;
      this.showPasswordError = false;

      if (!this.username && !this.password) {
        this.showUsernameError = true;
        this.showPasswordError = true;
        return;
      } else if (!this.username) {
        this.showUsernameError = true;
        return;
      } else if (!this.password) {
        this.showPasswordError = true;
        return;
      }
    },
    submitForm() {
      const formData = {
        username: this.username,
        password: this.password,
      };

      if (this.isValidUsername) {
        axios
          .post("http://127.0.0.1:8000/authorization/token/login/", formData)
          .then((response) => {
            const token = response.data.auth_token;
            axios.defaults.headers.common["Authorization"] = "Token " + token;

            if (response.status === 200) {
              axios
                .get("http://127.0.0.1:8000/profile/", {
                  headers: {
                    Authorization: `Token ${token}`,
                  },
                })
                .then((profileResponse) => {
                  const info = this.parseData(profileResponse.data.user_info);
                  const account_type = info.account_type;

                  this.$store.commit("setToken", { token, account_type });

                  Swal.fire({
                    title: "Вітаю!",
                    text: "Ви ввійшли в профіль!",
                    icon: "success",
                  }).then(() => {
                    let route = "/profile";

                    if (account_type === "Учень") {
                      route = "/profile-student/courses";
                    }
                    if (account_type === "Викладач") {
                      route = "/profile-teacher/courses";
                    } else if (account_type === "Адміністратор") {
                      route = "/profile-admin/link";
                    }

                    this.$router.push(route).then(() => {
                      window.location.reload();
                    });
                  });
                })
                .catch((error) => {
                  console.error("Failed to fetch user profile:", error);
                  Swal.fire({
                    icon: "error",
                    text: "Не вдалося отримати інформацію про користувача!",
                  });
                });
            } else {
              Swal.fire({
                icon: "error",
                text: "Не вірний логін або пароль!",
              });
            }
          })
          .catch((error) => {
            console.error("Login failed:", error);
            Swal.fire({
              text: "Не вірний логін або пароль!",
              icon: "error",
            });
          });
      } else {
        Swal.fire({
          title: "Помилка",
          text: "Введіть правильний логін або пароль!",
          icon: "error",
        });
      }
    },
  },
};
</script>

<style>
.container-reg {
  max-width: 1100px;
  margin: 70px auto;
  display: flex;
  justify-content: space-between;
  gap: 50px;
  background-color: #e9effd;
  border-radius: 12px;
}
.container-left {
  background-image: url(../../assets/auth.png);
  width: 550px;
  height: 550px;
  border-radius: 12px 0 0 12px;
}
.container-left p {
  font-family: "Open Sans";
  font-style: normal;
  font-weight: 700;
  font-size: 20px;
  line-height: 30px;
  color: #282828;
  width: 250px;
  margin: 20px;
}
.login-container {
  display: flex;
  align-items: center;
  width: 550px;
  height: 550px;
}
.login-form {
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-form h2 {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
  font-family: "Roboto";
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.input-field {
  width: 400px;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #ccc;
  border-radius: 6px;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  border-color: #4a90e2;
  outline: none;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 5px;
}

.login-button {
  width: 427px;
  padding: 12px;
  background-color: #4a90e2;
  color: white;
  font-size: 18px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #357abd;
}

.line {
  height: 1px;
  background-color: #ddd;
  margin: 20px 0;
}

.have-account {
  font-size: 14px;
}

.have-account a {
  color: #4a90e2;
  text-decoration: none;
  font-weight: bold;
}

.have-account a:hover {
  text-decoration: underline;
}
</style>
