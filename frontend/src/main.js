import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import store from "./store";

axios.defaults.baseURL = "http://127.0.0.1:8000";

store.commit("initializeStore");

const app = createApp(App);
app.config.globalProperties.$axios = axios;
app.use(router).use(store).mount("#app");
