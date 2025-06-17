<template>
  <div class="chat-container">
    <div class="chat-history">
      <div v-for="(msg, i) in messages" :key="i" class="chat-message" :class="msg.role">
        <strong>{{ msg.role === 'user' ? 'Tú' : 'Asistente' }}:</strong>
        <p>{{ msg.text }}</p>
      </div>
      <div ref="bottomAnchor"></div>
    </div>
    <form @submit.prevent="sendMessage" class="chat-input">
      <input
        v-model="userInput"
        type="text"
        placeholder="Write here..."
        class="input"
      />
      <button type="submit" class="btn">Send</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInput: '',
      messages: [
        {
          role: 'bot',
          text: "👋 Hi! I'm your virtual assistant. You can ask me about the products in the catalog, such as prices, stock, or whether they are fragile. Type your question below."
        }
      ]
    };
  },
  methods: {
    async sendMessage() {
      const question = this.userInput.trim();
      if (!question) return;

      this.messages.push({ role: 'user', text: question });
      this.userInput = '';
      this.$nextTick(this.scrollToBottom);

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question })
        });
        const data = await res.json();
        this.messages.push({ role: 'bot', text: data.response });
        this.$nextTick(this.scrollToBottom);
      } catch (error) {
        this.messages.push({ role: 'bot', text: "Error while consulting the assistant." });
        this.$nextTick(this.scrollToBottom);
      }
    },
    scrollToBottom() {
      const el = this.$refs.bottomAnchor;
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  max-width: 600px;
  height: 100%;
  max-height: 500px;
  padding: 1rem;
  background: #1f2937;
  color: white;
  border: 1px solid #374151;
  border-radius: 1rem;
  overflow: hidden;
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.chat-message {
  max-width: 80%;
  padding: 0.5rem 0.75rem;
  border-radius: 0.75rem;
  word-wrap: break-word;
  white-space: pre-wrap;
  line-height: 1.4;
  font-size: 0.9rem;
  text-align: left;
}

.chat-message.user {
  align-self: flex-end;
  background-color: #2563eb;
  color: white;
  border-bottom-right-radius: 0;
  text-align: right;
}

.chat-message.bot {
  align-self: flex-start;
  background-color: #374151;
  color: #fcd34d;
  border-bottom-left-radius: 0;
  text-align: left;
}

.chat-input {
  display: flex;
  gap: 0.5rem;
}

.input {
  flex: 1;
  padding: 0.5rem;
  background: #374151;
  border: none;
  border-radius: 0.375rem;
  color: white;
}

.btn {
  padding: 0.5rem 1rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 0.375rem;
}

.chat-message {
  animation: fadeIn 0.25s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
