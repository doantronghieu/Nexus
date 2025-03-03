import { ref } from "vue";

export const useLocation = () => {
	const loading = ref(true);
	const location = ref({
		lng: 0,
		lat: 0,
		zoom: 13,
	});

	const getCurrentLocation = () => {
		if ("geolocation" in navigator) {
			return new Promise((resolve, reject) => {
				navigator.geolocation.getCurrentPosition(
					(position) => {
						location.value = {
							lng: position.coords.longitude,
							lat: position.coords.latitude,
							zoom: 13,
						};
						resolve(location.value);
					},
					(error) => {
						console.error("Error getting location:", error);
						reject(error);
					}
				);
			});
		} else {
			return Promise.reject(
				new Error("Geolocation is not supported by your browser")
			);
		}
	};

	const initLocation = async () => {
		try {
			await getCurrentLocation();
			loading.value = false;
		} catch (error) {
			console.error("Failed to get initial location:", error);
			loading.value = false;
		}
	};

	const updateLocation = (newLocation) => {
		location.value = newLocation;
	};

	return {
		loading,
		location,
		getCurrentLocation,
		initLocation,
		updateLocation,
	};
};
