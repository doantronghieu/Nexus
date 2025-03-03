import { ref } from 'vue'
import mapboxgl from 'mapbox-gl'

export const useMap = () => {
  // Map and Markers refs
  const map = ref(null)
  const currentMarker = ref(null)
  const destinationMarker = ref(null)

  // Location state
  const loading = ref(true)
  const location = ref({
    lng: 0,
    lat: 0,
    zoom: 13
  })
  const isLocationOverridden = ref(false)
  const manualLocation = ref(null)

  // Map initialization
  const initializeMap = async (container, initialLocation) => {
    const config = useRuntimeConfig()
    mapboxgl.accessToken = config.public.mapboxAccessToken

    map.value = new mapboxgl.Map({
      container,
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [initialLocation.lng, initialLocation.lat],
      zoom: initialLocation.zoom
    })

    map.value.addControl(new mapboxgl.NavigationControl(), 'top-right')
    map.value.addControl(new mapboxgl.ScaleControl({ maxWidth: 100, unit: 'metric' }))

    await new Promise(resolve => map.value.on('load', resolve))

    return map.value
  }

  // Marker handling
  const updateCurrentLocationMarker = (location) => {
		if (!map.value) {
			console.warn("Map not initialized");
			return null;
		}

		try {
			if (currentMarker.value) {
				currentMarker.value.remove();
			}

			currentMarker.value = new mapboxgl.Marker({
				color: "#3887be",
				scale: 1.2,
				draggable: true,
			})
				.setLngLat([location.lng, location.lat])
				.addTo(map.value);

			return currentMarker.value;
		} catch (error) {
			console.error("Error updating current location marker:", error);
			return null;
		}
	};

  const updateDestinationMarker = (location) => {
    if (destinationMarker.value) {
      destinationMarker.value.remove()
    }

    destinationMarker.value = new mapboxgl.Marker({
      color: '#f30',
      scale: 1.2
    })
    .setLngLat([location.lng ?? location.longitude, location.lat ?? location.latitude])
    .addTo(map.value)

    return destinationMarker.value
  }

  // Route handling
  const drawRoute = (geometry) => {
    const geojson = {
      type: 'Feature',
      properties: {},
      geometry
    }

    if (map.value.getSource('route')) {
      map.value.getSource('route').setData(geojson)
    } else {
      map.value.addLayer({
        id: 'route',
        type: 'line',
        source: {
          type: 'geojson',
          data: geojson
        },
        layout: {
          'line-join': 'round',
          'line-cap': 'round'
        },
        paint: {
          'line-color': '#3887be',
          'line-width': 5,
          'line-opacity': 0.75
        }
      })
    }
  }

  const clearRoute = () => {
    if (destinationMarker.value) {
      destinationMarker.value.remove()
      destinationMarker.value = null
    }

    if (map.value.getLayer('route')) {
      map.value.removeLayer('route')
    }
    if (map.value.getSource('route')) {
      map.value.removeSource('route')
    }
  }

  // Location handling
  const getCurrentLocation = async () => {
		try {
			const config = useRuntimeConfig();
			const response = await fetch(`${config.public.apiBaseUrl}/api/location`, {
				method: "GET",
				headers: {
					accept: "application/json",
				},
			});

			if (!response.ok) {
				throw new Error("Failed to fetch location");
			}

			const data = await response.json();
			return {
				lng: data.coordinates.longitude,
				lat: data.coordinates.latitude,
				zoom: 15,
			};
		} catch (error) {
			console.error("Error fetching location:", error);
			showNotification("Failed to get current location", "error");
			return null;
		}
	};

  const setManualLocation = (loc) => {
    manualLocation.value = loc
    isLocationOverridden.value = true
    location.value = loc
  }

  const resetLocationOverride = () => {
    isLocationOverridden.value = false
    manualLocation.value = null
    getCurrentLocation()
  }

  // API functions
  const api = {
    places: {
      search: async (params) => {
        const config = useRuntimeConfig()
        const searchParams = new URLSearchParams(params)
        const response = await fetch(`${config.public.apiBaseUrl}/api/search/?${searchParams}`)
        if (!response.ok) throw new Error('Search failed')
        return response.json()
      },
      getDetails: async (id) => {
        const config = useRuntimeConfig()
        const response = await fetch(`${config.public.apiBaseUrl}/api/retrieve/${id}`)
        if (!response.ok) throw new Error('Failed to get place details')
        return response.json()
      },
      getStoredPlaces: async () => {
        const config = useRuntimeConfig()
        const response = await fetch(`${config.public.apiBaseUrl}/api/stored-places`)
        if (!response.ok) throw new Error('Failed to get stored places')
        return response.json()
      }
    },
    directions: {
      getRoute: async (params) => {
        const config = useRuntimeConfig()
        const searchParams = new URLSearchParams(params)
        const response = await fetch(`${config.public.apiBaseUrl}/api/directions/?${searchParams}`)
        if (!response.ok) throw new Error('Failed to get directions')
        return response.json()
      },
      getStoredDirections: async () => {
        const config = useRuntimeConfig()
        const response = await fetch(`${config.public.apiBaseUrl}/api/stored-directions`)
        if (!response.ok) throw new Error('Failed to get stored directions')
        return response.json()
      }
    }
  }

  return {
    // Map state
    map,
    currentMarker,
    destinationMarker,
    loading,
    location,
    isLocationOverridden,
    manualLocation,

    // Map functions
    initializeMap,
    updateCurrentLocationMarker,
    updateDestinationMarker,
    drawRoute,
    clearRoute,

    // Location functions
    getCurrentLocation,
    setManualLocation,
    resetLocationOverride,

    // API
    api
  }
}