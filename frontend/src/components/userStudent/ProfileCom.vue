<template>
  <div class="profile-back">
    <div class="profile-left">
      <div class="profile-picture-section">
        <img
          :src="getuserPhoto(user.photo)"
          alt=""
          class="profile-picture-preview"
        />
        <UploadPhoto />
      </div>
      <nav class="sidebars">
        <ul>
          <li>
            <router-link to="/profile-student/settings">
              <i class="fas fa-cogs"></i> Налаштування профілю
            </router-link>
          </li>
          <li>
            <router-link to="/profile-student/courses">
              <i class="fas fa-graduation-cap"></i> Мої курси
            </router-link>
          </li>
        </ul>
      </nav>
      <div class="logout-div">
        <logoutComp />
      </div>
    </div>
    <div class="profile-right">
      <div class="hello" style="max-height: calc(75vh); overflow-y: auto">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import UploadPhoto from "./UploadPhoto.vue";
import logoutComp from "../auth/LogoutComp.vue";
import { mapGetters } from "vuex";
import axios from "axios";

export default {
  computed: {
    ...mapGetters(["isAuthenticated"]),
  },
  data() {
    return {
      token: "",
      targetImagePath: "@/../../backend/user_images/",
      user: {
        photo: "",
        image: "",
      },
    };
  },
  components: {
    logoutComp,
    UploadPhoto,
  },
  mounted() {
    const token = this.$store.state.token;
    this.token = this.$store.state.token;

    axios
      .get("http://127.0.0.1:8000/profile/", {
        headers: {
          Authorization: `Token ${token}`,
        },
      })
      .then((response) => {
        this.responseData = response.data.user_info;
        const info = this.parseData(this.responseData);
        this.user.username = info.username;

        this.user.photo = info.image;
        this.getuserPhoto();
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  },
  methods: {
    getuserPhoto(photo) {
      try {
        const photoPath = photo
          ? photo.split("images/profile_images/")[1]
          : null;
        return photoPath
          ? require(`@/../../backend/images/profile_images/${photoPath}`)
          : "https://thumb.ac-illust.com/b1/b170870007dfa419295d949814474ab2_t.jpeg";
      } catch (error) {
        console.error("Error loading user photo:", error);
        return "https://thumb.ac-illust.com/b1/b170870007dfa419295d949814474ab2_t.jpeg";
      }
    },
    parseData(data) {
      const parsedData = {};
      data[0].forEach((item) => {
        const [key, value] = item.split(":").map((str) => str.trim());
        parsedData[key] = value;
      });
      return parsedData;
    },
  },
};
</script>

<style>
.logout-div {
  display: flex;
  justify-content: space-around;
}

.logout-page h2 {
  margin-bottom: 10px;
}

.logout-page p {
  margin-bottom: 20px;
}

.logout-page a {
  font-family: "Roboto";
  background-color: #220e5b;
  font-size: 16px;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}
.logout-page a:hover {
  border-bottom: 0;
}
.profile-back {
  background-color: #e9eaed;
  display: flex;
  padding: 20px;
}
.profile-left,
.profile-right {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0px 0px 3px 3px rgba(0, 0, 0, 0.1);
}
.profile-left {
  width: 450px;
  margin-right: 20px;
  height: 80vh;
}
.profile-right {
  width: 100%;
}
.sidebars i {
  font-size: 18px;
  width: 24px;
  text-align: center;
  padding-right: 10px;
}
</style>
