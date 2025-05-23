<template>
  <section class="section section-1">
    <div class="container-main">
      <div class="left">
        <h2>Навчання онлайн ще ніколи не було настільки простим</h2>
        <p>
          LinguaBoost - цікава платформа, яка навчить вас більш інтерактивно
          вивчати англійську мову.
        </p>
        <div class="link">
          <router-link to="/courses">Почни навчання</router-link>
        </div>
      </div>
      <div class="right">
        <img src="../assets/rafiki.png" alt="Section 1 Image" />
      </div>
    </div>
  </section>

  <section class="section section-2">
    <div class="container-main">
      <div class="left">
        <img src="../assets/section2.png" alt="Section 2 Image 1" />
        <h3>З нами ви швидше опануєте мову</h3>
        <p>
          Наші навчальні матеріали, плани уроків та вправи допоможуть
          підготувати вас до різних ситуацій.
        </p>
        <div class="fact-box">
          <p class="strong">Цікавий факт:</p>
          <p>
            Чи знали ви, що ви пам'ятаєте 95% інформації, коли її детально
            переглянули, і лише 10% того, що читаєте? Спробуйте!
          </p>
        </div>
      </div>
      <div class="right section-2__box">
        <h3>Вивчати все можна онлайн, сидячи вдома</h3>
        <p>
          LinguaBoost - зручна платформа, яка допомагає учням швидко та
          ефективно вивчати англійську мову.
        </p>
      </div>
    </div>
  </section>

  <section class="section section-3">
    <div class="container-main flex-col">
      <h2>Про LinguaBoost</h2>
      <p>
        LinguaBoost – це революційний веб додаток для вивчення іноземної мови,
        що надає можливість покращувати знання, не зважаючи на те, початківець
        ви чи профі. Він робить вивчення мови доступним з будь-якого куточку
        світу. Також веб додаток надає можливість викладачам створювати власні
        курси з потрібними матеріалами та проводити заняття студентам.
      </p>
    </div>
  </section>

  <section class="section section-4">
    <div class="container-main">
      <div class="left">
        <h3>Разом ми надихаємо учнів рухатись вперед</h3>
        <p>
          Надані навчальні матеріали та уроки допоможуть підготувати учнів до
          відповідних тестів, що перевіряють знання мови та конкретних навичок,
          а саме: говоріння, читання, написання, слухання.
        </p>
      </div>
      <div class="right">
        <img src="../assets/section4-image.png" alt="Section 4 Image" />
      </div>
    </div>
  </section>

  <section class="section section-5">
    <div class="container-main">
      <div class="left">
        <img src="../assets/section5-image.png" alt="Section 5 Image" />
      </div>
      <div class="right">
        <h3>Наш шлях до вивчення англійської, крок за кроком</h3>
        <p>
          Цей шлях є ефективним і максимально корисним для користувачів. Наш
          унікальний підхід заохочує безперервний прогрес з чітким шляхом до
          покращення мовних навичок.
        </p>
      </div>
    </div>
  </section>

  <section class="section section-6">
    <div class="container-main">
      <div class="left">
        <h3>Мотивуйте інших:</h3>
        <p>
          Заохочуйте бажаючих та друзів приєднуватись до платформи LinguaBoost,
          що дозволить навчатися разом, обмінюючись отриманими знаннями з
          іноземної мови. Допомагайте іншим при виникненні проблем. Створюйте
          справжні зв'язки через мову.
        </p>
      </div>
      <div class="right">
        <img src="../assets/section6-image.png" alt="Section 6 Image" />
      </div>
    </div>
  </section>

  <section class="section section-7">
    <div class="container-main flex-col">
      <h3>Зустрічайте нашу команду</h3>
      <p>
        Наша команда складається з двох креативних викладачів, які мають досвід
        викладання та проводять заняття як для дорослих, так і для дітей. На
        заняттях завжди цікаво та весело, а матеріали курсу підбираються
        індивідуально під ваш запит.
      </p>
      <div class="teachers">
        <div class="teacher">
          <img src="../assets/Olena.jpg" alt="Olena" />
          <h4>Олена Шафран</h4>
          <div class="socials">
            <a href="mailto:olenashafran06@gmail.com" class="social-icon">
              <i class="fas fa-envelope"></i>
            </a>
            <a href="https://www.instagram.com/shafrankaa_" class="social-icon">
              <i class="fab fa-instagram"></i>
            </a>
          </div>
        </div>

        <div class="teacher">
          <img src="../assets/Nazar.png" alt="Nazar" />
          <h4>Назар Сус</h4>
          <div class="socials">
            <a href="mailto:susnazariy@gmail.com" class="social-icon">
              <i class="fas fa-envelope"></i>
            </a>
            <a href="https://www.instagram.com/sussusui/" class="social-icon">
              <i class="fab fa-instagram"></i>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {};
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0;
}

.container-main {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 70px;
}

.flex-col {
  flex-direction: column;
  gap: 20px;
}

/* Секція 1 */
.section-1 {
  background: linear-gradient(to right, #13347a, #2562e8);
  display: flex;
  padding: 50px;
  color: white;
}

.container-main .left {
  flex: 1;
}

.container-main .right {
  flex: 1;
}

.section-1 img {
  max-width: 100%;
  height: auto;
  padding: 70px 0;
}

/* Секція 2 */
.section-2 {
  background-image: url("../assets/section2-bg.png");
  background-size: 1000px;
  background-repeat: no-repeat;
  background-position: center;
  padding: 50px 0;
  display: flex;
}

.section-2 .left,
.section-2 .right {
  padding: 20px;
}

.section-2 .right img {
  max-width: 100%;
  height: auto;
}

.strong {
  font-weight: bold;
}

/* Секція 3 */
.section-3 {
  background-image: url("../assets/section3-bg.png");
  background-size: cover;
  background-position: center;
  padding: 50px;
  color: white;
}

/* Секція 4 */
.section-4 {
  display: flex;
  padding: 50px;
}

.section-4 .left,
.section-4 .right {
  flex: 1;
}

.section-4 img {
  max-width: 100%;
  height: auto;
}

/* Секція 5 */
.section-5 {
  display: flex;
  padding: 50px;
  background-image: url("../assets/section2-bg.png");
  background-size: 1000px;
  background-repeat: no-repeat;
}

.section-5 .left,
.section-5 .right {
  flex: 1;
}

.section-5 img {
  max-width: 100%;
  height: auto;
}

/* Секція 6 */
.section-6 {
  display: flex;
  padding: 50px;
}

.section-6 .left,
.section-6 .right {
  flex: 1;
}

.section-6 img {
  max-width: 100%;
  height: auto;
}

/* Секція 7 */
.section-7 {
  padding: 50px;
  background-image: url("../assets/section2-bg.png");
  background-size: 1000px;
  background-repeat: no-repeat;
  background-position: 50% 20%;
}

.teachers {
  display: flex;
  gap: 30px;
}

.teacher {
  flex: 1;
  text-align: center;
  border: 1px solid rgb(206, 206, 206);
  border-radius: 8px;
  padding: 25px;
  background-color: white;
}

.teacher img {
  max-width: 150px;
  border-radius: 50%;
}

.teacher h4 {
  font-style: normal;
  font-weight: 400;
  font-size: 22px;
  line-height: 24px;
  color: #0c0c0c;
}

.socials a {
  margin: 0 10px;
  color: #2562e8;
  text-decoration: none;
  font-size: 30px;
}

.section-1 .container-main .left h2 {
  font-family: "Roboto";
  font-style: normal;
  font-weight: 700;
  font-size: 44px;
  line-height: 66px;
  color: #ffffff;
}

.section-1 .container-main .left p {
  font-family: "Open Sans";
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  line-height: 30px;
  color: #ffffff;
}

.left .link {
  padding: 8px 16px;
  gap: 8px;
  background: #f6aa00;
  border-radius: 8px;
  width: 150px;
  text-align: center;
}
.left .link a {
  font-family: "Open Sans";
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 24px;
  color: #ffffff;
  text-decoration: none;
}

.left h3,
.right h3,
.flex-col h3 {
  font-family: "Roboto";
  font-style: normal;
  font-weight: 700;
  font-size: 40px;
  line-height: 60px;
  color: #1d1d1d;
  margin: 10px 0;
}
.left p,
.right p,
.flex-col p {
  font-family: "Open Sans";
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  line-height: 30px;
  color: #404040;
  text-align: justify;
}
.fact-box {
  border: 1px solid black;
  border-radius: 8px;
  padding: 15px;
  background-color: white;
}
.fact-box .strong {
  font-style: normal;
  font-weight: 600;
  font-size: 20px;
  line-height: 21px;
  color: #0c0c0c;
  margin-top: 0;
}

.fact-box p {
  font-style: normal;
  font-weight: 400;
  font-size: 18px;
  line-height: 25px;
  color: #404040;
  margin-bottom: 0;
  text-align: justify;
}
.section-2__box {
  border: 1px solid rgb(206, 206, 206);
  border-radius: 8px;
  padding: 15px;
  background-color: white;
}

.section-2__box h3 {
  font-style: normal;
  font-weight: 700;
  font-size: 32px;
  line-height: 48px;
  text-align: center;
  color: #0065f4;
}

.section-2__box p {
  font-style: normal;
  font-weight: 400;
  font-size: 18px;
  line-height: 27px;
  text-align: justify;
  color: #404040;
}

.section-3 .container-main {
  align-items: baseline;
  margin: 70px auto;
}

.section-3 .container-main h2 {
  font-family: "Roboto";
  font-style: normal;
  font-weight: 700;
  font-size: 56px;
  line-height: 84px;
  color: #ffffff;
  text-align: justify;
  margin: 0;
}
.section-3 .container-main p {
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  line-height: 30px;
  color: #ffffff;
  text-align: justify;
  margin: 0;
}
</style>
