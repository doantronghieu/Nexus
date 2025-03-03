<template>
  <div>
    <LoadingOverlay v-if="loading" />
    <MapComponent
      v-else
      :initial-location="location"
      @update:location="updateLocation"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useLocation } from '~/composables/useLocation';

const {
  loading,
  location,
  initLocation,
  updateLocation
} = useLocation();

onMounted(() => {
  initLocation();
});
</script>