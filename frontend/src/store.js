import { createStore } from "vuex";

export default createStore({
  state: {
    token: "",
    account_type: "",
  },
  mutations: {
    // Оновлення токена та типу акаунта
    setToken(state, { token, account_type }) {
      state.token = token;
      state.account_type = account_type;
      localStorage.setItem("auth_token", token);
      localStorage.setItem("account_type", account_type);
    },

    // Видалення токена та очищення типу акаунта
    removeToken(state) {
      state.token = "";
      state.account_type = "";
      localStorage.removeItem("auth_token");
      localStorage.removeItem("account_type");
    },

    // Ініціалізація стану з localStorage
    initializeStore(state) {
      const token = localStorage.getItem("auth_token");
      const account_type = localStorage.getItem("account_type");
      if (token) {
        state.token = token;
        state.account_type = account_type;
      }
    },
  },
  getters: {
    // Перевірка наявності токена у store
    isAuthenticated: (state) => {
      return state.token !== "";
    },
    account_type: (state) => state.account_type,
  },
  actions: {},
  modules: {},
});
