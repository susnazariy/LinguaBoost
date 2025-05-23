<template>
  <div class="photo-upload">
    <div class="button-container">
      <label class="custom-file-upload">
        <input
          type="file"
          ref="fileInput"
          accept="image/*"
          @change="onFileSelected"
        />
        Оберіть фото
      </label>
      <button v-if="selectedFile" class="cancel-button" @click="cancelPreview">
        Відмінити
      </button>
    </div>
    <div class="move-photo" v-if="selectedFile">
      <img
        :src="selectedFilePreview"
        alt="Selected Photo"
        class="selected-photo"
      />
    </div>
    <button class="uploa-photo" v-if="selectedFile" @click="uploadPhoto">
      Завантажити фото
    </button>
  </div>
</template>
<script>
import axios from "axios";
import { mapGetters } from "vuex";
import Swal from "sweetalert2";

export default {
  computed: {
    ...mapGetters(["isAuthenticated"]),
  },
  mounted() {
    this.token = this.$store.state.token;
  },
  methods: {
    cancelPreview() {
      this.selectedFile = null;
      this.selectedFilePreview = null;
      this.$refs.fileInput.value = "";
    },
    onFileSelected(event) {
      try {
        this.selectedFile = event.target.files[0];
        if (!this.selectedFile.type.startsWith("image/")) {
          throw new Error("Selected file is not an image");
        }

        const reader = new FileReader();
        reader.onload = () => {
          this.selectedFilePreview = reader.result;
        };
        reader.readAsDataURL(this.selectedFile);
      } catch (error) {
        console.error("Error handling file:", error);
        this.cancelPreview();
        let errorMessage = "Помилка при виборі файлу.";

        if (error.message === "Selected file is not an image") {
          errorMessage =
            "Вибраний файл не є зображенням. Виберіть файл з розширенням .jpg, .png або .jpeg.";
        }

        Swal.fire({
          icon: "error",
          title: "Помилка",
          text: errorMessage,
        });
      }
    },
    uploadPhoto() {
      const formData = new FormData();
      formData.append("image", this.selectedFile);

      axios
        .post("http://127.0.0.1:8000/image_upload/", formData, {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        })
        .then((response) => {
          console.log("Response from photo upload:", response.data);
          Swal.fire({
            icon: "success",
            title: "Фото успішно оновлено!",
          }).then(() => {
            window.location.reload();
          });
        })
        .catch((error) => {
          console.error("Error uploading photo:", error);
          Swal.fire({
            icon: "error",
            title: "Помилка.",
            text: "Фото не вдалось оновити!",
          });
        });
    },
  },
  data() {
    return {
      token: "",
      selectedFile: null,
      selectedFilePreview: null,
    };
  },
};
</script>

<style>
.button-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
.uploa-photo {
  margin-top: 10px;
}
.cancel-button {
  width: 133px;
  margin-left: 10px;
  background-color: #dc3545;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 16px;
  cursor: pointer;
}
.cancel-button:hover {
  background-color: #c0392b;
}
.photo-upload {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px 0 20px;
  border-radius: 8px;
  width: 300px;
  margin: 0 auto;
}
.move-photo {
  position: absolute;
  bottom: 120px;
}
.selected-photo {
  width: 202px;
  height: 202px;
  border: 2px solid black;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
  object-fit: cover;
  border-radius: 50%;
  background-color: #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #fff;
}
.custom-file-upload {
  cursor: pointer;
  padding: 8px 16px;
  font-size: 16px;
  font-weight: normal;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  text-align: center;
  width: 101px;
}
.custom-file-upload:hover {
  background-color: #0056b3;
  color: #fff;
}
.custom-file-upload input[type="file"] {
  display: none;
}
.uploa-photo {
  padding: 8px 16px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.uploa-photo:hover {
  background-color: #0056b3;
}
</style>
