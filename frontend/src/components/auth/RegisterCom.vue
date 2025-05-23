<template>
  <div class="container-reg">
    <div class="container-left">
      <p>Ласкаво просимо, здається Ви тут вперше!</p>
    </div>
    <div class="regist-container back-wh">
      <div class="regist-form">
        <h2>Реєстрація</h2>
        <div class="registration-form-style">
          <form @submit.prevent="register" class="form-grid">
            <div class="form-group">
              <input
                type="text"
                id="user-username"
                v-model="userUsername"
                :class="{ 'input-field': true, error: !isValidUsername }"
                maxlength="20"
                placeholder="Введіть логін"
                @blur="clearRegistrationError"
              />
              <div
                v-if="!isValidUsername && userUsername !== ''"
                class="error-message"
              >
                Введіть коректний логін!
              </div>
              <div v-if="registrationUserError" class="error-message">
                {{ registrationUserError }}
              </div>
            </div>
            <div class="form-group">
              <input
                type="email"
                id="user-email"
                v-model="userEmail"
                :class="{ 'input-field': true, error: !isValidEmail }"
                maxlength="60"
                placeholder="Введіть електронну адресу"
                @blur="clearRegistrationError"
              />
              <div
                v-if="!isValidEmail && userEmail !== ''"
                class="error-message"
              >
                Введіть дійсну адресу електронної пошти!
              </div>
              <div v-if="registrationEmailError" class="error-message">
                {{ registrationEmailError }}
              </div>
            </div>
            <div class="form-group">
              <input
                type="tel"
                id="user-phone"
                v-model="userPhoneNumber"
                :class="{ 'input-field': true, error: !isValidPhoneNumber }"
                maxlength="13"
                placeholder="Введіть номер телефону"
                @blur="clearRegistrationError"
              />
              <div
                v-if="!isValidPhoneNumber && userPhoneNumber !== ''"
                class="error-message"
              >
                Введіть дійсний номер телефону!
              </div>
              <div v-if="registrationPhoneError" class="error-message">
                {{ registrationPhoneError }}
              </div>
            </div>
            <div class="form-group">
              <input
                type="text"
                id="user-first-name"
                v-model="userFirstName"
                :class="{ 'input-field': true, error: !isValidFirstName }"
                maxlength="60"
                placeholder="Введіть ім'я"
              />
              <div
                v-if="!isValidFirstName && userFirstName !== ''"
                class="error-message"
              >
                Введіть справжнє ім'я!
              </div>
            </div>

            <div class="form-group">
              <input
                type="text"
                id="user-middle-name"
                v-model="userMiddleName"
                :class="{ 'input-field': true, error: !isValidMiddleName }"
                maxlength="60"
                placeholder="Введіть по батькові"
              />
              <div
                v-if="!isValidMiddleName && userMiddleName !== ''"
                class="error-message"
              >
                Введіть справжнє по батькові!
              </div>
            </div>

            <div class="form-group">
              <input
                type="text"
                id="user-last-name"
                v-model="userLastName"
                :class="{ 'input-field': true, error: !isValidLastName }"
                maxlength="60"
                placeholder="Введіть прізвище"
              />
              <div
                v-if="!isValidLastName && userLastName !== ''"
                class="error-message"
              >
                Введіть справжнє прізвище!
              </div>
            </div>

            <div class="form-group">
              <input
                type="date"
                id="user-birthday"
                v-model="userBirthday"
                :class="{ 'input-field': true, error: !isValidBirthday }"
              />
              <div
                v-if="!isValidBirthday && userBirthday !== ''"
                class="error-message"
              >
                Оберіть коректну дату народження!
              </div>
            </div>
            <div class="form-group">
              <input
                type="password"
                id="user-password"
                v-model="userPassword"
                :class="{ 'input-field': true, error: !isValidPassword }"
                placeholder="Введіть пароль"
              />
              <div
                v-if="!isValidPassword && userPassword !== ''"
                class="error-message"
              >
                {{ passwordErrorMessage }}
              </div>
            </div>
            <div class="form-group">
              <input
                type="password"
                id="user-confirm-password"
                v-model="userConfirmPassword"
                :class="{ 'input-field': true, error: !isValidConfirmPassword }"
                placeholder="Підтвердіть обраний пароль"
              />
              <div
                v-if="!isValidConfirmPassword && userConfirmPassword !== ''"
                class="error-message"
              >
                Паролі не співпадають!
              </div>
            </div>
            <div class="form-group centered">
              <select
                id="user-type"
                v-model="userType"
                :class="{ 'input-field-select': true }"
              >
                <option value="" disabled selected>
                  Оберіть тип користувача
                </option>
                <option value="Учень">Учень</option>
                <option value="Викладач">Викладач</option>
              </select>
            </div>
            <div class="form-group centered">
              <button type="submit" class="register-button">
                Зареєструватись
              </button>
            </div>
          </form>
        </div>
        <div class="line"></div>
        <div class="have-account">
          Вже є акаунт? <a href="#/login">Увійти</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import zxcvbn from "zxcvbn";

export default {
  data() {
    return {
      userUsername: "",
      userPassword: "",
      userConfirmPassword: "",
      userEmail: "",
      userFirstName: "",
      userMiddleName: "",
      userLastName: "",
      userPhoneNumber: "",
      userBirthday: "",
      registrationUserError: "",
      registrationEmailError: "",
      registrationPhoneError: "",
      userType: "Учень",
    };
  },
  computed: {
    isValidUsername() {
      if (!/[a-zA-Z]/.test(this.userUsername)) {
        return false;
      }
      return /^[a-zA-Z0-9_]+$/.test(this.userUsername);
    },
    isValidPassword() {
      const hasNumber = /\d/.test(this.userPassword);
      const passwordResult = zxcvbn(this.userPassword);
      return passwordResult.score >= 3 && hasNumber;
    },
    isValidConfirmPassword() {
      return this.userPassword === this.userConfirmPassword;
    },
    isValidFirstName() {
      return /^([А-ЩЬЮЯҐЄІЇ][а-щьюяґєії']{1,20})([-][А-ЩЬЮЯҐЄІЇ][а-щьюяґєії']{1,20}){0,2}$/.test(
        this.userFirstName
      );
    },
    isValidMiddleName() {
      return /^([А-ЩЬЮЯҐЄІЇ][а-щьюяґєії']{1,20})([-][А-ЩЬЮЯҐЄІЇ][а-щьюяґєії']{1,20}){0,2}$/.test(
        this.userMiddleName
      );
    },
    isValidLastName() {
      return /^([А-ЩЬЮЯҐЄІЇ][а-щьюяґєії']{1,20})([-][А-ЩЬЮЯҐЄІЇ][а-щьюяґєії']{1,20}){0,2}$/.test(
        this.userLastName
      );
    },
    isValidBirthday() {
      return !!this.userBirthday;
    },
    passwordErrorMessage() {
      if (this.userPassword === "") {
        return "Введіть пароль!";
      } else if (this.userPassword.length < 8) {
        return "Пароль має містити мінімум 8 символів!";
      } else if (!/\d/.test(this.userPassword)) {
        return "Пароль має містити мінімум одне число!";
      } else if (zxcvbn(this.userPassword).score < 3) {
        return "Пароль занадто легкий. Оберіть складніший!";
      } else {
        return "Введіть правильний пароль!";
      }
    },
    isValidEmail() {
      return /^([a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,}))?$/.test(
        this.userEmail
      );
    },
    isValidPhoneNumber() {
      return /^(\+(?:[0-9] ?){12,12}[0-9]*)?$/.test(this.userPhoneNumber);
    },
  },
  methods: {
    clearRegistrationError() {
      this.registrationUserError = "";
      this.registrationEmailError = "";
      this.registrationPhoneError = "";
    },
    register() {
      if (this.areFieldsEmpty()) {
        Swal.fire({
          icon: "error",
          title: "Помилка!",
          text: "Введіть всі необхідні поля!",
        });
        return;
      }
      if (this.isFormValid()) {
        const requestData = {
          username: this.userUsername,
          password: this.userPassword,
          email: this.userEmail,
          phone_number: this.userPhoneNumber,
          first_name: this.userFirstName,
          patronymic: this.userMiddleName,
          last_name: this.userLastName,
          birthday: this.userBirthday,
          account_type: this.userType,
        };
        axios
          .post("http://127.0.0.1:8000/registration/", requestData)
          .then((response) => {
            if (response.data === "Message: user register is success!") {
              Swal.fire({
                icon: "success",
                title: "Реєстрація успішна!",
                text: "Вас було успішно зареєстровано!",
                confirmButtonText: "Увійти в профіль",
              }).then(() => {
                this.$router.push("/login");
              });
            } else if (response.data === "Error: username is already taken!") {
              this.registrationUserError = "Логін вже зайнятий!";
            } else if (response.data === "Error: email is already taken!") {
              this.registrationEmailError = "Електронна пошта вже зайнята!";
            } else if (
              response.data === "Error: phone number is already taken!"
            ) {
              this.registrationPhoneError = "Номер телефону вже зайнятий!";
            }
          })
          .catch((error) => {
            console.error("Registration failed:", error);
            Swal.fire({
              icon: "error",
              title: "Помилка під час реєстрації!",
              text: "Будь ласка, спробуйте зареєструватись пізніше!",
            });
          });
      } else {
        Swal.fire({
          icon: "error",
          title: "Помилка під час валідації!",
          text: "Заповніть всі поля правильно!",
        });
      }
    },
    areFieldsEmpty() {
      return (
        this.userUsername === "" ||
        this.userPassword === "" ||
        this.userConfirmPassword === "" ||
        this.userPhoneNumber === "" ||
        this.userFirstName === "" ||
        this.userMiddleName === "" ||
        this.userLastName === "" ||
        this.userEmail === "" ||
        this.userBirthday === "" ||
        this.userType === ""
      );
    },
    isFormValid() {
      return (
        this.isValidUsername &&
        this.isValidPassword &&
        this.isValidConfirmPassword &&
        this.isValidPhoneNumber &&
        this.isValidFirstName &&
        this.isValidMiddleName &&
        this.isValidLastName &&
        this.isValidEmail &&
        this.isValidBirthday
      );
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
  height: 100%;
  border-radius: 12px 0 0 12px;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
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
.regist-container {
  display: flex;
  align-items: center;
  width: 550px;
}
.regist-form h2 {
  font-family: "Roboto";
  text-align: center;
}
.regist-form {
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 0;
}
.input-field-select {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  transition: border-color 0.3s ease;
}

.input-field-select:focus {
  border-color: #007bff;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 5px;
}
.register-button {
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

.register-button:hover {
  background-color: #357abd;
}
.line {
  width: 100%;
  height: 1px;
  background-color: #ddd;
  margin: 20px 0;
}
</style>
