# Nuxt Mapbox Application

A modern web application built with Nuxt.js that provides an interactive map interface using Mapbox GL JS. The application automatically detects the user's location and allows for real-time tracking of coordinates and zoom levels.

## Features

- 🗺️ Interactive Mapbox map integration
- 📍 Automatic user location detection
- 🔄 Real-time coordinate and zoom level updates
- 🎯 "Get My Location" functionality
- 🎨 Clean, responsive UI with a semi-transparent control panel
- 🧭 Navigation controls (zoom, rotate, pitch)
- 📏 Scale control
- 📱 Mobile-friendly design

## Prerequisites

Before you begin, ensure you have installed:

- Node.js (v16 or later)
- npm or yarn
- A Mapbox account and access token

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-name>
```

2. Install dependencies:
```bash
npm install
npx nuxi@latest module add tailwindcss
npx nuxi@latest module add nuxt-mapbox
npm install --save-dev mapbox-gl
```

3. Set up environment variables:
   - Copy the `.env.example` file to `.env`
   - Add your Mapbox access token to the `.env` file:
```bash
NUXT_PUBLIC_MAPBOX_ACCESS_TOKEN=your_mapbox_access_token_here
```

4. Start the development server:
```bash
npm run dev
```

5. Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
├── components/
│   ├── LoadingOverlay.vue    # Loading screen component
│   └── MapComponent.vue      # Main map component
├── composables/
│   └── useLocation.ts        # Location handling logic
├── pages/
│   └── index.vue            # Main application page
├── .env                     # Environment variables (not in git)
├── .env.example            # Example environment variables
├── nuxt.config.ts          # Nuxt configuration
└── README.md               # This file
```

## Components

### MapComponent
The main component that renders the Mapbox map and handles map-related interactions.

Props:
- `initialLocation`: Object containing initial coordinates and zoom level

Events:
- `update:location`: Emitted when map center or zoom changes

### LoadingOverlay
A simple overlay component shown while getting the user's location.

## Composables

### useLocation
A composable that handles all location-related logic.

Functions:
- `getCurrentLocation()`: Gets the user's current location
- `initLocation()`: Initializes location on app start
- `updateLocation(newLocation)`: Updates the stored location

## Environment Variables

Required environment variables:
- `NUXT_PUBLIC_MAPBOX_ACCESS_TOKEN`: Your Mapbox access token

## Development

### Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Launch production server
npm run start

# Lint code
npm run lint
```

### Adding New Features

1. Components should be added to the `components/` directory
2. Shared logic should be added as composables in `composables/`
3. Environment variables should be documented in `.env.example`

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is open-source and available under the MIT License.

## Acknowledgments

- Built with [Nuxt.js](https://nuxt.com/)
- Maps powered by [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/)
- Using [nuxt-mapbox](https://github.com/AlexLavoie42/nuxt-mapbox) module

## Support

For support, please create an issue in the repository or contact the maintainers.