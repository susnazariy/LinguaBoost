<template>
  <div class="logout-page">
    <button @click="showLogoutConfirmation">Вийти</button>
  </div>
</template>

<script>
import Swal from 'sweetalert2';

export default {
  methods: {
    showLogoutConfirmation() {
      Swal.fire({
        icon: 'question',
        title: 'Ви впевнені, що хочете вийти?',
        showCancelButton: true,
        confirmButtonText: 'Так',
        cancelButtonText: 'Ні',
      }).then((result) => {
        if (result.isConfirmed) {
          this.$router.push('/').then(() => {
            this.logout();
          });
        }
      });
    },
    logout() {
      this.$store.commit('removeToken');

      localStorage.removeItem('auth_token');
      localStorage.removeItem('token');
      localStorage.removeItem('selectedDate');
      Swal.fire({
        icon: 'success',
        title: 'Успішний вихід!',
        text: 'Ви успішно вийшли з профілю!',
      }).then(() => {
        this.$router.push('/login').then(() => {
          window.location.reload();
        });
      });

    }
  },
};
</script>
  
  <style>
  .logout-page {
    max-width: 400px;
    display: flex;
    justify-content: center;
    padding: 20px;
    border-radius: 10px;
  }
  
  .logout-page h2 {
    margin-bottom: 10px;
  }
  
  .logout-page p {
    margin-bottom: 20px;
  }
  
  .logout-page button {
    font-family: 'Roboto';
    font-weight: 600;
    background-color: #dc3545;
    font-size: 16px;
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
  }
  </style>