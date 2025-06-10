<template>
  <div class="bg-gray-900 text-white font-sans flex justify-center px-4 py-8">
    <div class="w-full max-w-5xl">
      <div
        v-if="showDeleteModal"
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 transition-opacity duration-300"
      >
        <div class="bg-gray-800 p-6 rounded-lg shadow-md w-full max-w-md transform transition-transform duration-300 scale-100">          <h3 class="text-xl font-semibold mb-4">Delete product?</h3>
          <p class="text-gray-300 mb-6">
            You are going to delete <strong>{{ productToDelete?.name }}</strong>. This action cannot be undone.
          </p>
          <div class="flex justify-center gap-4">
            <button
              class="px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded"
              @click="showDeleteModal = false"
            >
              Cancel
            </button>
            <button
              class="px-4 py-2 bg-red-600 hover:bg-red-700 rounded"
              @click="confirmDeleteProduct"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
      <div
          v-if="errorToast.show"
          class="fixed bottom-6 left-1/2 transform -translate-x-1/2 bg-red-600 text-white px-6 py-3 rounded shadow-lg z-50"
      >
          <pre class="whitespace-pre-wrap text-sm">{{ errorToast.message }}</pre>
      </div>
      <div
        v-if="successToast.show"
        class="fixed bottom-6 left-1/2 transform -translate-x-1/2 bg-green-600 text-white px-6 py-3 rounded shadow-lg z-50"
      >
        <pre class="whitespace-pre-wrap text-sm">{{ successToast.message }}</pre>
      </div>
      <h1 class="text-4xl font-bold text-center mb-10">Product catalog</h1>  
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mb-12">
        <div
          v-for="product in products"
          :key="product.id"
          class="bg-gray-800 rounded-lg p-5 shadow flex flex-col justify-between"
        >
          <div>
            <h3 class="text-xl font-semibold mb-1 text-center">
              {{ product.name }}
            </h3>
            <p class="text-sm text-gray-400">{{ product.description }}</p>
            <p
              class="text-xs inline-flex items-center gap-1 px-2 py-0.5 rounded-full mt-1"
              :class="product.is_fragile ? 'text-green-400 bg-green-900/30' : 'text-red-400 bg-red-900/30'"
              :title="product.is_fragile ? 'This product is fragile' : 'This product is not fragile'"
            >
              {{ product.is_fragile ? '✔️' : '✖️' }}
              {{ product.is_fragile ? 'Fragile' : 'Not fragile' }}
            </p>
            <p class="text-lg mt-2 font-bold">
              {{ typeof product.price === 'number' ? product.price.toFixed(2) : product.price }} €
            </p>
            <p class="text-sm">Stock: {{ product.stock }} | Sold: {{ product.sales ?? 0 }}</p>
          </div>
          <p class="text-sm text-green-400">
            Total sold: {{ (product.price * product.sales).toFixed(2) }} €
          </p>
          <div class="mt-4 flex flex-col gap-2">
            <button
              class="px-4 py-2 rounded bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 transition"
              :disabled="product.stock <= 0"
              @click="sell(product.id)"
            >
              Sell 1
            </button>
            <button
              class="px-4 py-2 rounded bg-red-600 hover:bg-red-700 transition"
              @click="askDeleteProduct(product)"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
  
      <div class="max-w-md mx-auto bg-gray-800 p-6 rounded-lg shadow">
        <h2 class="text-2xl font-semibold text-center mb-4">New product</h2>
        <form @submit.prevent="submitForm" class="space-y-4">
          <input
            v-model="newProduct.name"
            class="w-full p-2 rounded bg-gray-700 text-white"
            placeholder="Name"
            required
          />
          <input
            v-model="newProduct.description"
            class="w-full p-2 rounded bg-gray-700 text-white"
            placeholder="Description"
          />
          <input
              v-model.number="newProduct.price"
              type="number"
              step="0.01"
              class="w-full p-2 rounded bg-gray-700 text-white"
              placeholder="Price (€)"
              required
          />
          <input
            v-model.number="newProduct.stock"
            type="number"
            class="w-full p-2 rounded bg-gray-700 text-white"
            placeholder="Stock"
            required
          />
          <label class="flex items-center space-x-2 text-sm text-white">
            <input type="checkbox" v-model="newProduct.is_fragile" />
            <span>Is fragile</span>
          </label>
          <button
            type="submit"
            class="w-full bg-green-600 hover:bg-green-700 p-2 rounded text-white font-bold transition"
          >
            Create
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

if (import.meta.hot) {
  import.meta.hot.accept(() => {
    location.reload()
  })
}

const products = ref([])
const newProduct = ref({
  name: '',
  description: '',
  price: null,
  stock: null,
  is_fragile: false
})

const errorToast = ref({ show: false, message: '' })
const showDeleteModal = ref(false)
const productToDelete = ref(null)
const successToast = ref({ show: false, message: '' })


const fetchProducts = async () => {
  const res = await fetch('/api/products')
  const productList = await res.json()

  const salesRes = await fetch('/api/sales/summary')
  const salesSummary = await salesRes.json()

  productList.forEach(p => {
    p.price = parseFloat(p.price)
    const match = salesSummary.find(s => s.id === p.id)
    p.sales = match?.total_units_sold ?? 0
  })


  products.value = productList
}

const askDeleteProduct = (product) => {
  productToDelete.value = product
  showDeleteModal.value = true
}

const confirmDeleteProduct = async () => {
  const res = await fetch(`/api/products/${productToDelete.value.id}`, {
    method: 'DELETE'
  })

  if (res.ok) {
    products.value = products.value.filter(p => p.id !== productToDelete.value.id)
    successToast.value.message = "Product deleted successfully"
    successToast.value.show = true
    setTimeout(() => (successToast.value.show = false), 3000)
  } else {
    const err = await res.json()
    errorToast.value.message = "Error when deleting: " + err.detail
    errorToast.value.show = true
    setTimeout(() => (errorToast.value.show = false), 4000)
  }

  showDeleteModal.value = false
  productToDelete.value = null
}


const submitForm = async () => {
  if (
    !newProduct.value.name.trim() ||
    isNaN(newProduct.value.price) || newProduct.value.price <= 0 ||
    isNaN(newProduct.value.stock) || newProduct.value.stock < 0
  ) {
    errorToast.value.message = "Please, complete all fields correctly."
    errorToast.value.show = true
    setTimeout(() => (errorToast.value.show = false), 4000)
    return
  }

  newProduct.value.price = parseFloat(newProduct.value.price)
  newProduct.value.stock = parseInt(newProduct.value.stock)

  const res = await fetch('/api/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newProduct.value)
  })

  if (res.ok) {
    const created = await res.json()
    created.sales = 0
    products.value.push(created)
    newProduct.value = { name: '', description: '', price: null, stock: null, is_fragile: false }
  } else {
    const error = await res.json()
    const messages = error.detail.map(e => `• ${e.loc[1]}: ${e.msg}`).join("\n")
    errorToast.value.message = messages
    errorToast.value.show = true
    setTimeout(() => (errorToast.value.show = false), 4000)
  }
}

const sell = async (productId) => {
  const res = await fetch('/api/sales', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: productId, units: 1 })
  })

  if (res.ok) {
    const product = products.value.find(p => p.id === productId)
    if (product) {
      product.stock -= 1
      product.sales += 1
    }
  } else {
    const err = await res.json()
    alert("Error when selling: " + err.detail)
  }
}

onMounted(fetchProducts)
</script>
