<script setup lang="ts">
import { ref } from 'vue';
import TaskList from './components/TaskList.vue';
import TaskDetails from './components/TaskDetails.vue';
import type { Task } from './types';


const tasks = ref<Task[]>([
  { id: 1, title: 'Do X', details: ['Equipment A', 'Tool B'], completed: false },
  { id: 2, title: 'Do a Y', details: [], completed: false },
  { id: 3, title: 'Buy Z', details: ['Shop A', 'Product B'], completed: false },{ id: 1, title: 'Do X', details: ['Equipment A', 'Tool B'], completed: false },
  { id: 2, title: 'Do a Y', details: [], completed: false },
  { id: 3, title: 'Buy Z', details: ['Shop A', 'Product B'], completed: false },{ id: 1, title: 'Do X', details: ['Equipment A', 'Tool B'], completed: false },
  { id: 2, title: 'Do a Y', details: [], completed: false },
  { id: 3, title: 'Buy Z', details: ['Shop A', 'Product B'], completed: false },{ id: 1, title: 'Do X', details: ['Equipment A', 'Tool B'], completed: false },
  { id: 2, title: 'Do a Y', details: [], completed: false },
  { id: 3, title: 'Buy Z', details: ['Shop A', 'Product B'], completed: false },{ id: 1, title: 'Do X', details: ['Equipment A', 'Tool B'], completed: false },
  { id: 2, title: 'Do a Y', details: [], completed: false },
  { id: 3, title: 'Buy Z', details: ['Shop A', 'Product B'], completed: false },{ id: 1, title: 'Do X', details: ['Equipment A', 'Tool B'], completed: false },
  { id: 2, title: 'Do a Y', details: [], completed: false },
  { id: 3, title: 'Buy Z', details: ['Shop A', 'Product B'], completed: false },
]);

const selectedTask = ref<Task | null>(null);

const selectTask = (task: Task) => {
  selectedTask.value = task;
};

const toggleTaskCompletion = (taskId: number) => {
  const task = tasks.value.find(t => t.id === taskId);
  if (task) {
    task.completed = !task.completed;
  }
};
</script>

<template>
  <div class="flex h-screen m-8 rounded-xl overflow-hidden">
    <!-- Task List Section -->
    <TaskList 
      :tasks="tasks" 
      @selectTask="selectTask" 
      @toggleCompletion="toggleTaskCompletion"
      :selectedTaskId="selectedTask?.id" 
    />

    <!-- Task Details Section -->
    <TaskDetails :task="selectedTask" />
  </div>
</template>
