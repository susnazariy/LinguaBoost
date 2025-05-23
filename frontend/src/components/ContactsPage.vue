<template>
  <div class="contacts-container">
    <section class="section section-3">
      <div class="container-main flex-col">
        <h2>Зв'яжіться з нами</h2>
        <p>
          Не соромтеся звертатися до нас у будь-який час. Ми обов'язково
          зв'яжемося з вами, як тільки зможемо!
        </p>
      </div>
    </section>

    <div class="contacts-grid" v-if="contact">
      <div class="contact-item">
        <i class="fas fa-phone contact-icon"></i>
        <h3>Телефон</h3>
        <p>{{ contact.website_phone_number }}</p>
      </div>
      <div class="contact-item">
        <i class="fas fa-map-marker-alt contact-icon"></i>
        <h3>Адреса</h3>
        <p>{{ contact.website_address }}</p>
      </div>
      <div class="contact-item">
        <i class="fas fa-envelope contact-icon"></i>
        <h3>Електронна пошта</h3>
        <p>{{ contact.website_email }}</p>
      </div>
    </div>

    <div class="map-container" v-if="contact">
      <iframe
        :src="contact.google_map"
        width="100%"
        height="400"
        style="border: 0"
        allowfullscreen=""
        loading="lazy"
      ></iframe>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ContactsPage",
  data() {
    return {
      contact: null,
    };
  },
  mounted() {
    this.fetchContactData();
  },
  methods: {
    async fetchContactData() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/home/");
        if (response.data && response.data.length > 0) {
          this.contact = response.data[0];
        }
      } catch (error) {
        console.error("Error fetching contact data:", error);
      }
    },
  },
};
</script>

<style scoped>
.contacts-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.contacts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 60px;
  width: 100%;
  max-width: 900px;
  margin-top: 40px;
}
.contact-item {
  text-align: center;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid #007bff;
}
.contact-item h3 {
  font-family: "Open Sans";
  font-style: normal;
  font-weight: 700;
  font-size: 18px;
  line-height: 27px;
  color: #1d1d1d;
}
.contact-item p {
  font-family: "Open Sans";
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 18px;
  color: #282828;
}
.contact-icon {
  font-size: 40px;
  margin-bottom: 10px;
  color: #007bff;
}
.map-container {
  margin-top: 40px;
  width: 100%;
}
.section-3 {
  background-image: url("../assets/section3-bg.png");
  background-size: cover;
  background-position: center;
  padding: 50px 0;
  color: white;
  width: 100%;
}
.container-main {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}
.flex-col h2 {
  font-family: "Roboto";
  font-style: normal;
  font-weight: 700;
  font-size: 40px;
  line-height: 60px;
  margin: 10px 0;
  text-align: justify;
}

.flex-col p {
  font-family: "Open Sans";
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  line-height: 30px;
  color: white;
  text-align: justify;
}
</style>
