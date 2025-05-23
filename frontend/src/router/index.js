import { createRouter, createWebHashHistory } from "vue-router";
import store from "../store";

// usual
import Home from "../components/HomePage.vue";
import Contacts from "../components/ContactsPage.vue";
import NotFound from "../components/NotFound.vue";

// auth
import Login from "../components/auth/LoginCom.vue";
import Register from "../components/auth/RegisterCom.vue";

import userStudent from "../components/userStudent/ProfileCom.vue";
import ProfileSettingsStudent from "../components/userStudent/profile/ProfileDetails.vue";
import StudentCourses from "../components/userStudent/profile/CreatedCourses.vue";

import userTeacher from "../components/userTeacher/ProfileCom.vue";
import ProfileSettingsTeacher from "../components/userTeacher/profile/ProfileDetails.vue";
import CreatedCourses from "../components/userTeacher/profile/CreatedCourses.vue";
import CourseRequests from "../components/userTeacher/profile/CourseRequests.vue";

import userAdmin from "../components/userAdmin/ProfileCom.vue";
import ProfileSettingsAdmin from "../components/userAdmin/profile/ProfileDetails.vue";
import ProfileLink from "../components/userAdmin/profile/ProfileLink.vue";

// courses
import Courses from "../components/course/CoursesPage.vue";
import CourseDetails from "@/components/course/CourseDetails.vue";
import addCourse from "@/components/course/addCourse.vue";
import EditCourseInfo from "@/components/course/EditCourse.vue";
import SidebarMenuCourse from "@/components/course/SidebarMenuCourse.vue";

//lessons
import LessonsList from "../components/course/lesson/LessonsList.vue";

import SidebarMenuExerStud from "@/components/course/studentLesson/SidebarMenuExer.vue";

// exercise
import SidebarMenuExer from "@/components/course/lesson/exercise/SidebarMenuExer.vue";
import UpdateExercise from "../components/course/lesson/exercise/updateExercise/UpdateExercise.vue";

import AddExercise from "../components/course/lesson/exercise/exerciseCreation/AddExercise.vue";
import AddListening from "../components/course/lesson/exercise/exerciseCreation/AddListening.vue";
import AddReading from "../components/course/lesson/exercise/exerciseCreation/AddReading.vue";
import AddRules from "../components/course/lesson/exercise/exerciseCreation/AddRules.vue";
import AddVocabulary from "../components/course/lesson/exercise/exerciseCreation/AddVocabulary.vue";
import AddWarmUp from "../components/course/lesson/exercise/exerciseCreation/AddWarmUp.vue";

// test
import SidebarMenuTests from "@/components/course/lesson/tests/SidebarMenuTests.vue";

import CreateTestQuestion from "../components/course/lesson/tests/testCreation/CreateTestQuestion.vue";
import UpdateTestQuestion from "../components/course/lesson/tests/updateTest/UpdateTestQuestion.vue";

import Test from "../components/course/studentLesson/updateTest/TestQuestion.vue";
import CourseQuestion from "../components/course/studentLesson/updateTest/CourseQuestion.vue";

import TestPage from "../components/course/lesson/exercise/updateExercise/UpdateAddWarmUp.vue";

const routes = [
  { path: "/", component: Home, meta: { title: "Головна | LinguaBoost" } },
  { path: "/login", component: Login, meta: { title: "Логін | LinguaBoost" } },
  {
    path: "/register",
    component: Register,
    meta: { title: "Реєстрація | LinguaBoost" },
  },
  {
    path: "/profile-student",
    component: userStudent,
    meta: {
      title: "Профіль | LinguaBoost",
      requiresAuth: true,
      roles: ["Учень"],
    },
    children: [
      { path: "settings", component: ProfileSettingsStudent },
      { path: "courses", component: StudentCourses },
      { path: "requests", component: CourseRequests },
    ],
  },
  {
    path: "/profile-teacher",
    component: userTeacher,
    meta: {
      title: "Профіль | LinguaBoost",
      requiresAuth: true,
      roles: ["Викладач"],
    },
    children: [
      { path: "settings", component: ProfileSettingsTeacher },
      { path: "courses", component: CreatedCourses },
      { path: "requests", component: CourseRequests },
    ],
  },
  {
    path: "/profile-admin",
    component: userAdmin,
    meta: {
      title: "Профіль | LinguaBoost",
      requiresAuth: true,
      roles: ["Адміністратор"],
    },
    children: [
      { path: "settings", component: ProfileSettingsAdmin },
      { path: "link", component: ProfileLink },
    ],
  },
  {
    path: "/:pathMatch(.*)*",
    component: NotFound,
    meta: { title: "Сторінки не знайдено | LinguaBoost" },
  },
  {
    path: "/courses",
    component: Courses,
    meta: { title: "Курси | LinguaBoost" },
  },
  {
    path: "/course/:id",
    component: CourseDetails,
    meta: { title: "Деталі курсу | LinguaBoost" },
  },
  {
    path: "/add-course",
    component: addCourse,
    meta: { title: "Створення курсу | LinguaBoost" },
  },
  {
    path: "/change-course/:id",
    component: SidebarMenuCourse,
    meta: { title: "Редагування курсу | LinguaBoost" },
    children: [
      {
        path: "edit",
        component: EditCourseInfo,
        meta: { title: "Редагування курсу | LinguaBoost" },
      },
      {
        path: "lessons-list",
        component: LessonsList,
        meta: { title: "Список занять | LinguaBoost" },
      },
    ],
  },
  {
    path: "/lesson/:id",
    component: SidebarMenuExerStud,
    meta: { title: "Редагування курсу | LinguaBoost" },
  },
  {
    path: "/test/:id",
    component: Test,
    meta: { title: "Проходження тесту | LinguaBoost" },
  },
  {
    path: "/course-test/:id",
    component: CourseQuestion,
    meta: { title: "Проходження фінального тесту | LinguaBoost" },
  },
  {
    path: "/created-tests/:id",
    component: SidebarMenuTests,
    meta: { title: "Перегляд тестів заняття | LinguaBoost" },
  },
  {
    path: "/created-exercises/:id",
    component: SidebarMenuExer,
    meta: { title: "Перегляд вправ заняття | LinguaBoost" },
  },
  {
    path: "/update-exercise/:category-:id",
    name: "update-exercise",
    component: UpdateExercise,
    props: true,
  },
  {
    path: "/add-exercise/:id?",
    component: AddExercise,
    children: [
      {
        path: "",
        redirect: (to) => `/add-exercise/${to.params.id || ""}/warm_up`,
      },
      { path: "warm_up", component: AddWarmUp },
      { path: "listening", component: AddListening },
      { path: "reading", component: AddReading },
      { path: "rules", component: AddRules },
      { path: "vocabulary", component: AddVocabulary },
    ],
  },
  {
    path: "/create-question/:id?",
    component: CreateTestQuestion,
  },
  {
    path: "/update-question/:category-:id",
    name: "update-question",
    component: UpdateTestQuestion,
    props: true,
  },

  {
    path: "/test",
    component: TestPage,
    meta: { title: "Тестування | LinguaBoost" },
  },
  {
    path: "/contacts",
    component: Contacts,
    meta: { title: "Контакти | LinguaBoost" },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return { top: 0, behavior: "smooth" };
  },
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;
  const account_type = store.getters.account_type;

  if ((to.path === "/login" || to.path === "/register") && isAuthenticated) {
    next("/");
    return;
  }

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next("/login");
    } else if (
      to.matched.some(
        (record) =>
          record.meta.roles && !record.meta.roles.includes(account_type)
      )
    ) {
      next("/");
    } else {
      next();
    }
  } else {
    next();
  }
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || "LinguaBoost";
  next();
});

export default router;
