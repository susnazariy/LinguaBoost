<template>
  <div id="app" class="container">
    <Header />
    <router-view class="main-content" />
    <Footer />
  </div>
</template>

<script>
import Header from "./components/HeaderComp.vue";
import Footer from "./components/FooterComp.vue";

export default {
  components: {
    Header,
    Footer,
  },
};
</script>

<style>
html,
body {
  height: 100%;
  margin: 0;
  display: flex;
  flex-direction: column;
}

body {
  padding-top: 60px;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.main-content {
  flex: 1;
}
</style>
