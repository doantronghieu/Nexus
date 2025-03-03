/**
 * OpenAI Realtime API Client
 * Handles WebRTC or WebSocket connections to the OpenAI Realtime API
 */
class RealtimeClient {
    constructor(options = {}) {
        this.options = {
            useWebRTC: true,  // WebRTC is preferred for client-side
            model: 'gpt-4o-realtime-preview-2024-12-17',
            modalities: ['text', 'audio'],
            voice: 'alloy',
            instructions: 'You are a helpful assistant.',
            useAzure: false,
            azureEndpoint: null,
            azureApiVersion: null,
            azureDeployment: null,
            ...options
        };
        
        this.token = null;
        this.peerConnection = null;
        this.dataChannel = null;
        this.socket = null;
        this.isConnected = false;
        this.eventHandlers = {};
        this.mediaStream = null;
        this.audioElement = null;
    }
    
    /**
     * Set up event listeners
     * @param {string} eventType - The event type to listen for
     * @param {Function} handler - The event handler function
     */
    on(eventType, handler) {
        if (!this.eventHandlers[eventType]) {
            this.eventHandlers[eventType] = [];
        }
        this.eventHandlers[eventType].push(handler);
    }
    
    /**
     * Emit an event to registered handlers
     * @param {string} eventType - The event type to emit
     * @param {Object} data - The event data
     */
    emit(eventType, data) {
        const handlers = this.eventHandlers[eventType] || [];
        handlers.forEach(handler => {
            try {
                handler(data);
            } catch (error) {
                console.error(`Error in ${eventType} handler:`, error);
            }
        });
    }
    
    /**
     * Connect to the OpenAI Realtime API
     * @param {string} token - The ephemeral token for authentication
     */
    async connect(token) {
        this.token = token;
        
        if (this.options.useWebRTC) {
            await this.connectWebRTC();
        } else {
            await this.connectWebSocket();
        }
    }
    
    /**
     * Connect using WebRTC (preferred for client-side)
     */
    async connectWebRTC() {
        try {
            // Create a new peer connection
            this.peerConnection = new RTCPeerConnection({
                iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
            });
            
            // Create a data channel for sending/receiving JSON
            this.dataChannel = this.peerConnection.createDataChannel('events', {
                ordered: true
            });
            
            // Set up data channel event handlers
            this.dataChannel.onopen = () => {
                this.isConnected = true;
                this.emit('connected', { type: 'data-channel' });
            };
            
            this.dataChannel.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleServerEvent(data);
                } catch (error) {
                    console.error('Error parsing data channel message:', error);
                }
            };
            
            this.dataChannel.onclose = () => {
                this.isConnected = false;
                this.emit('disconnected', { type: 'data-channel' });
            };
            
            // Set up audio track
            this.peerConnection.ontrack = (event) => {
                // Create audio element for model's audio output
                this.audioElement = new Audio();
                this.audioElement.srcObject = event.streams[0];
                this.audioElement.play();
                this.emit('audio-ready', { stream: event.streams[0] });
            };
            
            // Create offer
            const offer = await this.peerConnection.createOffer();
            await this.peerConnection.setLocalDescription(offer);
            
            // In a real implementation, we would exchange SDP with OpenAI's servers
            // For this demo, we'll simulate the connection
            
            // Simulate receiving an answer
            const simulatedAnswer = {
                type: 'answer',
                sdp: 'simulated SDP would go here'
            };
            
            // Set remote description
            await this.peerConnection.setRemoteDescription(simulatedAnswer);
            
            // For demo purposes, we'll simulate connection success
            setTimeout(() => {
                this.isConnected = true;
                this.emit('connected', { type: 'webrtc' });
            }, 1000);
            
        } catch (error) {
            console.error('Error connecting via WebRTC:', error);
            this.emit('error', { 
                type: 'connection-error',
                message: error.message,
                details: error
            });
        }
    }
    
    /**
     * Connect using WebSocket (alternative)
     */
    async connectWebSocket() {
        try {
            // In a real implementation, we would connect directly to OpenAI's or Azure OpenAI's WebSocket endpoint
            // For this demo, we'll use a simulated connection
            
            let url;
            if (this.options.useAzure) {
                // Format Azure OpenAI WebSocket URL
                let endpoint = this.options.azureEndpoint || '';
                
                // Handle different formats of endpoint URLs
                endpoint = endpoint.trim();
                
                // Remove https:// or wss:// prefix if present
                endpoint = endpoint.replace(/^(https?|wss?):(\/\/)?/, '');
                
                // Remove trailing slash if present
                endpoint = endpoint.replace(/\/$/, '');
                
                if (!endpoint) {
                    throw new Error('Azure OpenAI endpoint is required');
                }
                
                const deployment = this.options.azureDeployment || this.options.model;
                const apiVersion = this.options.azureApiVersion || '2024-02-15-preview';
                url = `wss://${endpoint}/openai/deployments/${deployment}/realtime?api-version=${apiVersion}`;
            } else {
                // Format standard OpenAI WebSocket URL
                url = `wss://api.openai.com/v1/realtime?model=${this.options.model}`;
            }
            
            this.socket = new WebSocket(url);
            
            this.socket.onopen = () => {
                this.isConnected = true;
                this.emit('connected', { type: 'websocket' });
                
                // Send initial configuration
                this.updateSession({
                    modalities: this.options.modalities,
                    instructions: this.options.instructions,
                    voice: this.options.voice
                });
            };
            
            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleServerEvent(data);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };
            
            this.socket.onclose = () => {
                this.isConnected = false;
                this.emit('disconnected', { type: 'websocket' });
            };
            
            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.emit('error', {
                    type: 'connection-error',
                    message: 'WebSocket connection error',
                    details: error
                });
            };
            
        } catch (error) {
            console.error('Error connecting via WebSocket:', error);
            this.emit('error', {
                type: 'connection-error',
                message: error.message,
                details: error
            });
        }
    }
    
    /**
     * Update session configuration
     * @param {Object} settings - Session settings to update
     */
    updateSession(settings) {
        const event = {
            type: 'session.update',
            session: settings
        };
        
        this.sendEvent(event);
    }
    
    /**
     * Send a text message to the model
     * @param {string} text - The message to send
     */
    sendTextMessage(text) {
        const event = {
            type: 'conversation.item.create',
            item: {
                type: 'message',
                role: 'user',
                content: [
                    {
                        type: 'input_text',
                        text: text
                    }
                ]
            }
        };
        
        this.sendEvent(event);
        
        // Request response
        this.createResponse();
    }
    
    /**
     * Send audio input to the model
     * @param {Blob} audioBlob - The audio blob to send
     */
    async sendAudioInput(audioBlob) {
        // Convert blob to base64
        const arrayBuffer = await audioBlob.arrayBuffer();
        const base64Audio = btoa(
            new Uint8Array(arrayBuffer)
                .reduce((data, byte) => data + String.fromCharCode(byte), '')
        );
        
        // Append audio to buffer
        const appendEvent = {
            type: 'input_audio_buffer.append',
            audio: base64Audio
        };
        
        this.sendEvent(appendEvent);
        
        // Commit audio buffer
        const commitEvent = {
            type: 'input_audio_buffer.commit'
        };
        
        this.sendEvent(commitEvent);
        
        // Request response
        this.createResponse();
    }
    
    /**
     * Request a response from the model
     * @param {Object} options - Response options
     */
    createResponse(options = {}) {
        const event = {
            type: 'response.create',
            response: options
        };
        
        this.sendEvent(event);
    }
    
    /**
     * Cancel an ongoing response
     * @param {string} responseId - Optional response ID to cancel
     */
    cancelResponse(responseId = null) {
        const event = {
            type: 'response.cancel'
        };
        
        if (responseId) {
            event.response_id = responseId;
        }
        
        this.sendEvent(event);
    }
    
    /**
     * Send an event to the server
     * @param {Object} event - The event to send
     */
    sendEvent(event) {
        if (!this.isConnected) {
            console.warn('Cannot send event: not connected');
            return;
        }
        
        // Add event ID
        event.event_id = `client-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
        
        const eventJson = JSON.stringify(event);
        
        if (this.options.useWebRTC && this.dataChannel) {
            this.dataChannel.send(eventJson);
        } else if (this.socket) {
            this.socket.send(eventJson);
        }
    }
    
    /**
     * Handle events from the server
     * @param {Object} event - The server event
     */
    handleServerEvent(event) {
        // Emit the event for listeners
        this.emit('server-event', event);
        
        // Also emit specific event types
        if (event.type) {
            this.emit(event.type, event);
        }
        
        // Handle specific event types
        switch (event.type) {
            case 'session.created':
                // Session was created
                break;
                
            case 'session.updated':
                // Session was updated
                break;
                
            case 'response.text.delta':
                // Text response delta
                break;
                
            case 'response.audio.delta':
                // Audio response delta
                break;
                
            case 'response.done':
                // Response completed
                break;
                
            case 'error':
                // Error from server
                console.error('Server error:', event.error);
                this.emit('error', event.error);
                break;
        }
    }
    
    /**
     * Start audio recording
     */
    async startAudioRecording() {
        try {
            this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // In a full implementation, we would:
            // 1. Add this track to the peer connection for WebRTC
            // 2. Or record and send chunks for WebSocket
            
            this.emit('recording-started', { stream: this.mediaStream });
            
            return this.mediaStream;
        } catch (error) {
            console.error('Error starting audio recording:', error);
            this.emit('error', {
                type: 'recording-error',
                message: error.message,
                details: error
            });
            throw error;
        }
    }
    
    /**
     * Stop audio recording
     */
    stopAudioRecording() {
        if (this.mediaStream) {
            this.mediaStream.getTracks().forEach(track => track.stop());
            this.mediaStream = null;
            this.emit('recording-stopped');
        }
    }
    
    /**
     * Disconnect from the server
     */
    disconnect() {
        if (this.mediaStream) {
            this.stopAudioRecording();
        }
        
        if (this.dataChannel) {
            this.dataChannel.close();
        }
        
        if (this.peerConnection) {
            this.peerConnection.close();
        }
        
        if (this.socket) {
            this.socket.close();
        }
        
        this.isConnected = false;
        this.emit('disconnected', { type: 'client-initiated' });
    }
}

// Export for browser environments
if (typeof window !== 'undefined') {
    window.RealtimeClient = RealtimeClient;
}
