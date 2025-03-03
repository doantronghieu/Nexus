import { defineStore } from 'pinia'
import { useWebSocketStore } from './websocket'

export const useWebRTCStore = defineStore('webrtc', {
  state: () => ({
    peerConnection: null as RTCPeerConnection | null,
    isConnected: false,
    error: null as string | null,
    isInitiator: false,
    localStream: null as MediaStream | null
  }),

  actions: {
    async initializePeerConnection() {
      try {
        // Close any existing connections
        this.closePeerConnection()

        // Create new peer connection with STUN/TURN servers
        this.peerConnection = new RTCPeerConnection({
          iceServers: [
            { urls: 'stun:stun.l.google.com:19302' },
            { urls: 'stun:stun1.l.google.com:19302' },
          ]
        })

        // Set up event handlers
        this.setupPeerConnectionHandlers()
        
        this.isInitiator = true
        this.error = null
        
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Failed to initialize WebRTC'
        console.error('WebRTC initialization error:', err)
      }
    },

    setupPeerConnectionHandlers() {
      if (!this.peerConnection) return

      const webSocketStore = useWebSocketStore()

      this.peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
          webSocketStore.sendMessage(JSON.stringify({
            type: 'webrtc',
            subtype: 'ice-candidate',
            content: event.candidate
          }))
        }
      }

      this.peerConnection.onconnectionstatechange = () => {
        if (this.peerConnection) {
          this.isConnected = this.peerConnection.connectionState === 'connected'
        }
      }

      this.peerConnection.oniceconnectionstatechange = () => {
        console.log('ICE Connection State:', this.peerConnection?.iceConnectionState)
      }
    },

    async handleSignalingMessage(message: any) {
      try {
        if (!this.peerConnection) {
          await this.initializePeerConnection()
        }

        switch (message.subtype) {
          case 'offer':
            await this.handleOffer(message.content)
            break
          case 'answer':
            await this.handleAnswer(message.content)
            break
          case 'ice-candidate':
            await this.handleIceCandidate(message.content)
            break
        }
      } catch (err) {
        console.error('Signaling error:', err)
        this.error = 'Signaling error occurred'
      }
    },

    async handleOffer(offer: RTCSessionDescriptionInit) {
      if (!this.peerConnection) return

      try {
        await this.peerConnection.setRemoteDescription(new RTCSessionDescription(offer))
        const answer = await this.peerConnection.createAnswer()
        await this.peerConnection.setLocalDescription(answer)

        const webSocketStore = useWebSocketStore()
        webSocketStore.sendMessage(JSON.stringify({
          type: 'webrtc',
          subtype: 'answer',
          content: answer
        }))
      } catch (err) {
        console.error('Error handling offer:', err)
        this.error = 'Failed to handle offer'
      }
    },

    async handleAnswer(answer: RTCSessionDescriptionInit) {
      if (!this.peerConnection) return

      try {
        await this.peerConnection.setRemoteDescription(new RTCSessionDescription(answer))
      } catch (err) {
        console.error('Error handling answer:', err)
        this.error = 'Failed to handle answer'
      }
    },

    async handleIceCandidate(candidate: RTCIceCandidateInit) {
      if (!this.peerConnection) return

      try {
        await this.peerConnection.addIceCandidate(new RTCIceCandidate(candidate))
      } catch (err) {
        console.error('Error handling ICE candidate:', err)
        this.error = 'Failed to handle ICE candidate'
      }
    },

    async addStream(stream: MediaStream) {
      if (!this.peerConnection) return

      this.localStream = stream
      stream.getTracks().forEach(track => {
        if (this.peerConnection) {
          this.peerConnection.addTrack(track, stream)
        }
      })

      if (this.isInitiator) {
        try {
          const offer = await this.peerConnection.createOffer()
          await this.peerConnection.setLocalDescription(offer)

          const webSocketStore = useWebSocketStore()
          webSocketStore.sendMessage(JSON.stringify({
            type: 'webrtc',
            subtype: 'offer',
            content: offer
          }))
        } catch (err) {
          console.error('Error creating offer:', err)
          this.error = 'Failed to create offer'
        }
      }
    },

    closePeerConnection() {
      if (this.peerConnection) {
        this.peerConnection.close()
        this.peerConnection = null
      }
      if (this.localStream) {
        this.localStream.getTracks().forEach(track => track.stop())
        this.localStream = null
      }
      this.isConnected = false
      this.error = null
    }
  }
})
