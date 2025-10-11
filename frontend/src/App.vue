<template>
  <div class="container">
    <h1>🤖 RAG Chatbot</h1>

    <div class="upload-section">
      <h2>📄 Carica PDF</h2>
      <input type="file" @change="handleFileUpload" />
      <button @click="uploadFile" :disabled="!selectedFile || loading">
        {{ loading ? "Caricamento..." : "Carica" }}
      </button>
    </div>

    <div class="chat-section">
      <h2>💬 Chat</h2>
      <div class="chat-window">
        <div v-for="(msg, index) in messages" :key="index" class="chat-bubble" :class="msg.role">
          <strong v-if="msg.role === 'user'">Tu:</strong>
          <strong v-else>Bot:</strong> {{ msg.text }}
        </div>
      </div>
      <div class="input-row">
        <input type="text" v-model="query" placeholder="Fai una domanda..." />
        <button @click="askQuestion" :disabled="!query">Invia</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from './api'

const selectedFile = ref(null)
const loading = ref(false)
const query = ref('')
const messages = ref([])

function handleFileUpload(e) {
  selectedFile.value = e.target.files[0]
}

async function uploadFile() {
  if (!selectedFile.value) return
  loading.value = true
  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    await api.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    alert('📎 File caricato e indicizzato con successo!')
  } catch (err) {
    console.error(err)
    alert('❌ Errore nel caricamento')
  } finally {
    loading.value = false
  }
}

async function askQuestion() {
  if (!query.value) return
  messages.value.push({ role: 'user', text: query.value })

  try {
    const res = await api.get('/ask', { params: { query: query.value } })
    messages.value.push({ role: 'bot', text: res.data.answer })
  } catch (err) {
    console.error(err)
    messages.value.push({ role: 'bot', text: '❌ Errore nel server' })
  }

  query.value = ''
}
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 2rem auto;
  font-family: Arial, sans-serif;
}
.upload-section, .chat-section {
  margin-bottom: 2rem;
}
.chat-window {
  border: 1px solid #ccc;
  padding: 1rem;
  height: 300px;
  overflow-y: auto;
  background: #f9f9f9;
  margin-bottom: 1rem;
}
.chat-bubble {
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  border-radius: 10px;
}
.chat-bubble.user {
  background-color: #cce5ff;
  text-align: right;
}
.chat-bubble.bot {
  background-color: #e2e3e5;
  text-align: left;
}
.input-row {
  display: flex;
  gap: 10px;
}
input[type="text"] {
  flex: 1;
  padding: 0.5rem;
}
button {
  padding: 0.5rem 1rem;
}
</style>
