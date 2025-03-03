// Map related types
export interface Location {
	lng: number;
	lat: number;
	zoom: number;
}

export interface Marker {
	lng: number;
	lat: number;
}

export interface RouteData {
	distance: number;
	duration: number;
	geometry: {
		coordinates: [number, number][];
		type: string;
	};
	legs: {
		steps: {
			maneuver: {
				instruction: string;
				location: [number, number];
			};
		}[];
	}[];
}

export interface SearchResult {
	mapbox_id: string;
	name: string;
	full_address: string;
	distance: number;
	place_formatted?: string;
	coordinates?: {
		longitude: number;
		latitude: number;
	};
}

export interface CachedPlace {
	mapbox_id: string;
	name: string;
	place_formatted: string;
}
