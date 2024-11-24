<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
import type { Task } from '../types';

defineProps<{
    tasks: Task[];
    selectedTaskId: number | null;
}>();

const emit = defineEmits<{
    (e: 'selectTask', task: Task): void;
    (e: 'toggleCompletion', taskId: number): void;
}>();

const selectTask = (task: Task) => {
    emit('selectTask', task);
};

const toggleCompletion = (taskId: number) => {
    emit('toggleCompletion', taskId);
};
</script>

<template>
    <div class="border-r border-zinc-700 w-1/4 bg-eerie-black p-4 overflow-y-scroll scrollbar">
        <h2 class="text-xl font-semibold text-white mb-4">Tasks</h2>
        <ul>
            <li v-for="task in tasks" :key="task.id" @click="() => selectTask(task)"
                class="flex items-center p-2 mb-2 rounded cursor-pointer hover:bg-gray-700 transition-colors" :class="{
                    'bg-gray-700': task.id === selectedTaskId,
                    'opacity-50': task.completed
                }">
                <input type="checkbox" :id="`task-${task.id}`" :checked="task.completed"
                    @change.stop="() => toggleCompletion(task.id)" class="peer form-checkbox h-4 w-4 text-blue-600" />
                <label :for="`task-${task.id}`" class="ml-2 text-white peer-checked:line-through">
                    {{ task.title }}
                </label>
            </li>
        </ul>
    </div>
</template>
