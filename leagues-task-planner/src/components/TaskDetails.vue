<script setup lang="ts">
import { watch, ref } from 'vue';
import type { Task } from '../types';

const props = defineProps<{
    task: Task | null;
}>();

const detailCompleted = ref<boolean[]>([]);

// Initialize the detailCompleted array when the task changes
watch(() => props.task, (newTask) => {
    if (newTask && newTask.details.length) {
        detailCompleted.value = newTask.details.map(() => false);
    } else {
        detailCompleted.value = [];
    }
});
</script>

<template>
    <div class="task-details w-3/4 bg-neutral-900 p-4">
        <h2 v-if="task" class="text-l font-bold text-white mb-4">{{ task.title }}</h2>
        <ul v-if="task && task.details.length">
            <li class="py-1 px-2 flex items-center" v-for="(detail, index) in task.details" :key="index">
                <input type="checkbox" :id="`detail-${index}`" v-model="detailCompleted[index]"
                    class="form-checkbox h-4 w-4 text-green-500" />
                <label :for="`detail-${index}`" class="ml-2 text-white">
                    {{ detail }}
                </label>
            </li>
        </ul>
        <p v-else class="border rounded-l border-gray-100 m-10 p-5 text-gray-400">Select a task to view details.</p>
    </div>
</template>

<style scoped>
.task-details label {
    margin-left: 0.5rem;
    cursor: pointer;
}

.task-details input[type="checkbox"]:checked+label {
    text-decoration: line-through;
    color: gray;
}
</style>