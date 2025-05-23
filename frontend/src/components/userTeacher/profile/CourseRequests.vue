<template>
  <div class="course-requests">
    <h2>Заявки на курси</h2>

    <div v-if="requests.length === 0" class="no-requests">
      Наразі немає заявок. ❗
    </div>

    <table v-else>
      <thead>
        <tr>
          <th>Назва курсу</th>
          <th>Ім'я користувача</th>
          <th>Дата та час заявки</th>
          <th>Статус</th>
          <th>Дії</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request.id">
          <td>{{ request.course_name }}</td>
          <td>{{ request.student_fullname }}</td>
          <td>{{ formatDate(request.application_datetime) }}</td>
          <td :class="statusClass(request.application_status)">
            {{ request.application_status }}
          </td>
          <td>
            <button
              @click="
                changeStatus(
                  request.id,
                  'Підтверджено',
                  request.student,
                  request.course
                )
              "
              :disabled="request.application_status !== 'В обробці'"
              class="accept"
            >
              ✅ Прийняти
            </button>
            <button
              @click="changeStatus(request.id, 'Відхилено')"
              :disabled="request.application_status !== 'В обробці'"
              class="reject"
            >
              ❌ Відхилити
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      requests: [],
    };
  },
  mounted() {
    this.fetchRequests();
  },
  computed: {
    ...mapGetters(["isAuthenticated"]),
  },
  methods: {
    async fetchRequests() {
      const token = this.$store.state.token;
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/student_applications_data/",
          {
            headers: { Authorization: `Token ${token}` },
          }
        );
        this.requests = response.data.student_applications_data;
      } catch (error) {
        console.error("Помилка отримання заявок:", error);
      }
    },
    async changeStatus(id, newStatus, studentId = null, courseId = null) {
      const token = this.$store.state.token;
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/change_application_status/",
          { application_id: id, new_status: newStatus },
          { headers: { Authorization: `Token ${token}` } }
        );

        if (response.status === 200) {
          this.requests = this.requests.map((req) =>
            req.id === id ? { ...req, application_status: newStatus } : req
          );

          if (newStatus === "Підтверджено" && studentId && courseId) {
            await this.addStudentToCourse(studentId, courseId);
          }
        }
      } catch (error) {
        console.error("Помилка оновлення статусу:", error);
      }
    },
    async addStudentToCourse(studentId, courseId) {
      const token = this.$store.state.token;
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/add_student_to_course/",
          { student_id: studentId, course_id: courseId },
          { headers: { Authorization: `Token ${token}` } }
        );

        if (response.status === 200) {
          console.log(
            `✅ Студента ID ${studentId} додано до курсу ID ${courseId}`
          );
        }
      } catch (error) {
        console.error("Помилка додавання студента до курсу:", error);
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString("uk-UA", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
    statusClass(status) {
      return {
        "status-pending": status === "В обробці",
        "status-accepted": status === "Підтверджено",
        "status-rejected": status === "Відхилено",
      };
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@700&family=Open+Sans:wght@400&display=swap");

.course-requests {
  padding: 20px;
  font-family: "Open Sans", sans-serif;
}

h2 {
  font-family: "Roboto", sans-serif;
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

.no-requests {
  text-align: center;
  font-size: 18px;
  color: #666;
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  font-family: "Open Sans", sans-serif;
}

th {
  background: #f4f4f4;
}

button {
  margin: 5px;
  padding: 8px 15px;
  border: none;
  cursor: pointer;
  font-family: "Open Sans", sans-serif;
  font-weight: 600;
  border-radius: 5px;
  transition: background 0.3s;
}

.accept {
  background: #4caf50;
  color: white;
}

.accept:hover {
  background: #45a049;
}

.reject {
  background: #ff837a;
  color: white;
}

.reject:hover {
  background: #e56c61;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.status-pending {
  color: orange;
}

.status-accepted {
  color: green;
}

.status-rejected {
  color: red;
}
</style>
