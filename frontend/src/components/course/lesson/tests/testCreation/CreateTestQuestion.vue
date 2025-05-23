<template>
  <div class="task-selection-container">
    <aside class="sidebar">
      <h2>Типи завдань</h2>
      <ul>
        <li
          v-for="(task, key) in tasks"
          :key="key"
          class="sidebar-item"
          @click="selectTask(key)"
        >
          <a :class="{ 'active-link': confirmedTaskType === key }">
            <i :class="task.iconClass"></i>
            <span>{{ task.title }}</span>
          </a>
        </li>
      </ul>
    </aside>

    <div class="task-content">
      <component v-if="confirmedTaskType" :is="taskComponent" />
    </div>
  </div>
</template>

<script>
import TranslateWordTask from "./TranslateWordTask.vue";
import OneManyTask from "./OneManyTask.vue";
import FixSentenceTask from "./FixSentenceTask.vue";
import AccordanceTask from "./AccordanceTask.vue";
import SequenceTask from "./SequenceTask.vue";

export default {
  components: {
    TranslateWordTask,
    OneManyTask,
    FixSentenceTask,
    AccordanceTask,
    SequenceTask,
  },
  data() {
    return {
      selectedTaskType: null,
      confirmedTaskType: null,
      tasks: {
        translate_word_task: {
          title: "Переклад слова",
          iconClass: "fas fa-language",
        },
        one_many_task: {
          title: "Один до багатьох",
          iconClass: "fas fa-exchange-alt",
        },
        fix_sentence_task: {
          title: "Виправити речення",
          iconClass: "fas fa-edit",
        },
        accordance_task: {
          title: "Відповідність",
          iconClass: "fas fa-check-circle",
        },
        sequence_task: {
          title: "Послідовність",
          iconClass: "fas fa-sort-amount-down",
        },
      },
    };
  },
  computed: {
    taskComponent() {
      const components = {
        translate_word_task: TranslateWordTask,
        one_many_task: OneManyTask,
        fix_sentence_task: FixSentenceTask,
        accordance_task: AccordanceTask,
        sequence_task: SequenceTask,
      };
      return components[this.confirmedTaskType] || null;
    },
  },
  mounted() {
    this.confirmedTaskType = Object.keys(this.tasks)[0];
  },
  methods: {
    selectTask(taskType) {
      this.confirmedTaskType = taskType;
    },
  },
};
</script>

<style scoped>
.sidebar i {
  font-size: 18px;
  width: 24px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.task-content {
  margin: 0 auto;
  padding: 20px 40px 0 40px;
  overflow-y: auto;
  width: 700px;
}
.task-content-container {
  margin-bottom: 20px;
}
.task-selection-container {
  box-sizing: content-box;

  display: flex;
  justify-content: space-between;
  width: 1100px;
  margin: 0 auto;
  font-family: "Roboto", "Open Sans", sans-serif;
}

.sidebar {
  width: 300px;
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
