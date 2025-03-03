<!-- pages/index.vue -->
<script setup>
const router = useRouter()
const config = useRuntimeConfig()

onMounted(() => {
  // Add error handling
  try {
    router.push('/server-setup')
  } catch (error) {
    console.error('Navigation error:', error)
  }
})
</script>

<template>
  <div>Loading...</div>
</template>