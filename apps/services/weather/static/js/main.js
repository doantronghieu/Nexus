// Weather Service UI JavaScript

// Service endpoints configuration
const API_ENDPOINTS = {
    forecast: '/api/forecast',
    historical: '/api/historical',
    marine: '/api/marine',
    airQuality: '/api/air-quality',
    geocoding: '/api/geocoding/search',
    elevation: '/api/elevation',
    flood: '/api/flood',
    ensemble: '/api/ensemble',
    climate: '/api/climate'
};

// UI State Management
const state = {
    currentTab: 'forecast',
    loading: false
};

// UI Element References
const elements = {
    navTabs: document.querySelector('.nav-tabs'),
    forms: document.querySelectorAll('.form-section'),
    responseSection: document.querySelector('.response-section'),
    responseContent: document.querySelector('.response-content'),
    loadingIndicator: document.querySelector('.loading')
};

// Initialize the UI
document.addEventListener('DOMContentLoaded', () => {
    setupTabNavigation();
    setupFormHandlers();
    showTab(state.currentTab);
});

// Tab Navigation Setup
function setupTabNavigation() {
    elements.navTabs?.addEventListener('click', (e) => {
        if (e.target.classList.contains('nav-tab')) {
            const tabId = e.target.dataset.tab;
            showTab(tabId);
        }
    });
}

// Show Selected Tab
function showTab(tabId) {
    // Update state
    state.currentTab = tabId;
    
    // Update tab buttons
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.tab === tabId);
    });
    
    // Show selected form
    elements.forms.forEach(form => {
        form.style.display = form.dataset.tab === tabId ? 'block' : 'none';
    });
}

// Form Submission Handlers
function setupFormHandlers() {
    elements.forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
}

// Handle Form Submission
async function handleFormSubmit(event) {
    event.preventDefault();
    
    // Start loading state
    setLoading(true);
    clearResponse();
    
    try {
        const formData = new FormData(event.target);
        const endpoint = event.target.dataset.endpoint;
        
        // Prepare request data
        const data = formatRequestData(formData, endpoint);
        
        // Make API request
        const response = await makeApiRequest(endpoint, data);
        
        // Display response
        displayResponse(response);
    } catch (error) {
        displayError(error);
    } finally {
        setLoading(false);
    }
}

// Format Request Data
function formatRequestData(formData, endpoint) {
    const data = {};
    
    for (const [key, value] of formData.entries()) {
        if (value) {
            if (key.includes('.')) {
                const [parent, child] = key.split('.');
                data[parent] = data[parent] || {};
                data[parent][child] = value;
            } else {
                data[key] = value;
            }
        }
    }
    
    return data;
}

// Make API Request
async function makeApiRequest(endpoint, data) {
    const url = API_ENDPOINTS[endpoint];
    const method = ['geocoding', 'elevation'].includes(endpoint) ? 'GET' : 'POST';
    
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (method === 'GET') {
        const params = new URLSearchParams(data);
        const fullUrl = `${url}?${params}`;
        return await fetch(fullUrl, options).then(r => r.json());
    } else {
        options.body = JSON.stringify(data);
        return await fetch(url, options).then(r => r.json());
    }
}

// Display Response
function displayResponse(response) {
    const formattedResponse = JSON.stringify(response, null, 2);
    elements.responseContent.textContent = formattedResponse;
    elements.responseSection.style.display = 'block';
}

// Display Error
function displayError(error) {
    const errorAlert = document.createElement('div');
    errorAlert.className = 'alert alert-error';
    errorAlert.textContent = error.message || 'An error occurred';
    
    elements.responseSection.insertBefore(errorAlert, elements.responseContent);
    elements.responseSection.style.display = 'block';
}

// Clear Response
function clearResponse() {
    elements.responseContent.textContent = '';
    const errorAlerts = document.querySelectorAll('.alert-error');
    errorAlerts.forEach(alert => alert.remove());
}

// Set Loading State
function setLoading(loading) {
    state.loading = loading;
    elements.loadingIndicator.classList.toggle('active', loading);
}

// Utility Functions
function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function validateCoordinates(lat, lon) {
    const latitude = parseFloat(lat);
    const longitude = parseFloat(lon);
    
    if (isNaN(latitude) || latitude < -90 || latitude > 90) {
        throw new Error('Invalid latitude. Must be between -90 and 90.');
    }
    
    if (isNaN(longitude) || longitude < -180 || longitude > 180) {
        throw new Error('Invalid longitude. Must be between -180 and 180.');
    }
    
    return { latitude, longitude };
}
