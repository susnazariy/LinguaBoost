<template>
  <div class="task-selection-container">
    <main class="task-content">
      <div class="task-content-container">
        <h2 class="task-selection-title">Редагування тестового питання</h2>
        <div v-if="confirmedTaskType" class="task-container">
          <component :is="taskComponent" />
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import TranslateWordTask from "./UpdateTranslateWordTask.vue";
import OneManyTask from "./UpdateOneManyTask.vue";
import FixSentenceTask from "./UpdateFixSentenceTask.vue";
import AccordanceTask from "./UpdateAccordanceTask.vue";
import SequenceTask from "./UpdateSequenceTask.vue";

export default {
  props: ["category", "id"],
  mounted() {
    if (this.category && this.taskTypes[this.category]) {
      this.confirmedTaskType = this.category;
    } else {
      this.confirmedTaskType = Object.keys(this.taskTypes)[0];
    }
  },

  components: {
    TranslateWordTask,
    OneManyTask,
    FixSentenceTask,
    AccordanceTask,
    SequenceTask,
  },
  data() {
    return {
      confirmedTaskType: null,
      taskTypes: {
        translate_word_task: {
          label: "Переклад слова",
          component: TranslateWordTask,
          icon: "fas fa-language",
        },
        one_many_task: {
          label: "Один до багатьох",
          component: OneManyTask,
          icon: "fas fa-project-diagram",
        },
        fix_sentence_task: {
          label: "Виправити речення",
          component: FixSentenceTask,
          icon: "fas fa-pen",
        },
        accordance_task: {
          label: "Відповідність",
          component: AccordanceTask,
          icon: "fas fa-exchange-alt",
        },
        sequence_task: {
          label: "Послідовність",
          component: SequenceTask,
          icon: "fas fa-sort-amount-down",
        },
      },
    };
  },
  computed: {
    taskComponent() {
      return this.confirmedTaskType
        ? this.taskTypes[this.confirmedTaskType].component
        : null;
    },
  },
  methods: {
    confirmSelection(taskType) {
      this.confirmedTaskType = taskType;
    },
  },
};
</script>
<style scoped>
.task-content {
  margin: 0 auto;
  padding: 20px 40px 0 40px;
  overflow-y: auto;
  width: 100%;
}
.task-content-container {
  margin-bottom: 20px;
}
.task-selection-container {
  display: flex;
  width: 1100px;
  margin: 0 auto;
  font-family: "Roboto", "Open Sans", sans-serif;
}

.sidebar {
  width: 350px;
  background: #f4f4f4;
  padding: 20px;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 80vh;
  overflow-y: auto;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  margin-bottom: 10px;
}

.sidebar a {
  text-decoration: none;
  color: black;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 5px;
  transition: background 0.3s ease-in-out;
  cursor: pointer;
}

.sidebar a.active-link {
  background: #007bff;
  color: white;
}

.sidebar i {
  font-size: 18px;
}

.preview-image {
  max-width: 200px;
  margin-top: 10px;
  display: block;
  border-radius: 5px;
}

.task-selection-title {
  text-align: center;
  color: #2562e8;
  font-weight: 700;
  margin: 0;
}

.task-selection-label {
  font-size: 18px;
  font-weight: 500;
  display: block;
  margin-bottom: 10px;
}

.task-selection-dropdown {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #2562e8;
  border-radius: 5px;
  outline: none;
}

.task-selection-btn {
  display: block;
  width: 100%;
  padding: 12px;
  margin-top: 15px;
  background: #2562e8;
  color: #fff;
  font-size: 18px;
  font-weight: 500;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.task-selection-btn:hover {
  background: #1d4eb5;
}

.task-container {
  border-radius: 5px;
  background: #fff;
}
</style>
