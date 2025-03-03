<template>
  <div class="map-wrapper">
    <div class="sidebar">
      <h2>Map Controls</h2>
      <div class="coordinates">
        Longitude: {{ location.lng.toFixed(4) }} | 
        Latitude: {{ location.lat.toFixed(4) }} | 
        Zoom: {{ location.zoom.toFixed(2) }}
      </div>
      <button @click="getCurrentLocation">Get My Location</button>
    </div>
    
    <MapboxMap
      map-id="main-map"
      :options="mapOptions"
      @update:center="updateCenter"
      @update:zoom="updateZoom"
      class="map-container"
    >
      <MapboxGeolocateControl position="top-right" />
      <MapboxNavigationControl position="top-right" />
      <MapboxScaleControl position="bottom-right" />
    </MapboxMap>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  initialLocation: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['update:location']);

const location = ref({ ...props.initialLocation });

// Watch for changes in initialLocation prop
watch(() => props.initialLocation, (newLocation) => {
  location.value = { ...newLocation };
}, { deep: true });

const mapOptions = computed(() => ({
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [location.value.lng, location.value.lat],
  zoom: location.value.zoom,
  container: 'main-map'
}));

const updateCenter = (center) => {
  location.value.lng = center.lng;
  location.value.lat = center.lat;
  emit('update:location', location.value);
};

const updateZoom = (zoom) => {
  location.value.zoom = zoom;
  emit('update:location', location.value);
};

const getCurrentLocation = () => {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        location.value = {
          lng: position.coords.longitude,
          lat: position.coords.latitude,
          zoom: 13
        };
        emit('update:location', location.value);
      },
      (error) => {
        console.error("Error getting location:", error);
        alert("Unable to get your location. Please check your browser settings.");
      }
    );
  } else {
    alert("Geolocation is not supported by your browser");
  }
};
</script>

<style scoped>
.map-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.map-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
}

.sidebar {
  position: absolute;
  top: 0;
  left: 0;
  margin: 12px;
  background-color: rgba(35, 55, 75, 0.9);
  color: #fff;
  padding: 6px 12px;
  font-family: monospace;
  z-index: 1;
  border-radius: 4px;
}

.coordinates {
  margin: 12px 0;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>