<template>
  <div>
    <!-- Botón flotante -->
    <button @click="toggleChat" class="chat-toggle-btn">
      💬
    </button>

    <!-- Caja de chat emergente -->
    <div v-if="isOpen" class="chat-box-container">
      <div class="chat-header">
        <span>Asistente</span>
        <button @click="toggleChat">✖</button>
      </div>
      <ChatBox />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ChatBox from './ChatBox.vue'

const isOpen = ref(false)
const toggleChat = () => {
  isOpen.value = !isOpen.value
}
</script>

<style scoped>
.chat-toggle-btn {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  background-color: #3b82f6;
  color: white;
  font-size: 1.5rem;
  border: none;
  border-radius: 50%;
  width: 3.5rem;
  height: 3.5rem;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  cursor: pointer;
  z-index: 1000;
}

.chat-box-container {
  position: fixed;
  bottom: 6rem;
  right: 1.5rem;
  width: 320px;
  max-height: 500px;
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 1rem;
  overflow: hidden;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  color: white;
}

.chat-header {
  background-color: #2563eb;
  color: white;
  padding: 0.5rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
