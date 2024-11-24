<script setup lang="ts">
import { defineProps, defineEmits, ref } from 'vue';
import type { Task } from '../types';

const props = defineProps<{
    tasks: Task[];
    selectedTaskId: number | null;
}>();

const emit = defineEmits<{
    (e: 'selectTask', task: Task): void;
    (e: 'toggleCompletion', taskId: number): void;
    (e: 'editTask', task: Task, newTitle: string): void;
}>();

const selectTask = (task: Task) => {
    emit('selectTask', task);
};

const toggleCompletion = (taskId: number) => {
    emit('toggleCompletion', taskId);
};

// State to track which task is being edited
const editingTaskId = ref<number | null>(null);
const editingTitle = ref<string>('');

// Function to start editing only if the task is selected
const handleTitleClick = (task: Task) => {
    if (props.selectedTaskId === task.id) {
        startEditing(task);
    } else {
        selectTask(task);
    }
}

const startEditing = (task: Task) => {
    editingTaskId.value = task.id;
    editingTitle.value = task.title;
};

const finishEditing = (task: Task) => {
    if (editingTitle.value.trim() !== '') {
        emit('editTask', task, editingTitle.value.trim());
    }
    editingTaskId.value = null;
    editingTitle.value = '';
};

const cancelEditing = () => {
    editingTaskId.value = null;
    editingTitle.value = '';
};
</script>

<template>
    <div class="border-r border-zinc-700 w-1/4 bg-eerie-black p-4 overflow-y-scroll scrollbar">
        <h2 class="text-xl font-semibold text-white mb-4">Tasks</h2>
        <ul>
            <li v-for="task in tasks" :key="task.id" @click="!editingTaskId && selectTask(task)"
                class="flex items-center p-2 mb-2 rounded cursor-pointer hover:bg-gray-700 transition-colors" :class="{
                    'bg-gray-700': task.id === selectedTaskId,
                    'opacity-50': task.completed
                }">
                <!-- Checkbox -->
                <input type="checkbox" :id="`task-${task.id}`" :checked="task.completed"
                    @change.stop="toggleCompletion(task.id)" @click.stop
                    class="peer form-checkbox h-4 w-4 text-blue-600" />

                <!-- Task Title or Edit Input -->
                <div class="ml-2 flex-1">
                    <template v-if="editingTaskId === task.id">
                        <input v-model="editingTitle" @keyup.enter="finishEditing(task)" @blur="finishEditing(task)"
                            @keyup.escape="cancelEditing"
                            class="w-full bg-transparent border-blue-600 text-white focus:outline-none"
                            autofocus />
                    </template>
                    <template v-else>
                        <span class="text-white peer-checked:line-through float-left" @click.stop="handleTitleClick(task)">
                            {{ task.title }}
                        </span>
                    </template>
                </div>
            </li>
        </ul>
    </div>
</template>
