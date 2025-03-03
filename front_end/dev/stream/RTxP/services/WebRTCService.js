import { Device } from 'mediasoup-client';

export class WebRTCService {
  constructor() {
    this.device = null;
    this.producerTransport = null;
    this.videoProducer = null;
    this.audioProducer = null;
  }

  async initializeDevice(routerRtpCapabilities) {
    this.device = new Device();
    await this.device.load({ routerRtpCapabilities });
  }

  async createSendTransport(transportOptions) {
    this.producerTransport = this.device.createSendTransport(transportOptions);

    this.producerTransport.on('connect', async ({ dtlsParameters }, callback, errback) => {
      try {
        await this.connectTransport(this.producerTransport.id, dtlsParameters);
        callback();
      } catch (error) {
        errback(error);
      }
    });

    this.producerTransport.on('produce', async ({ kind, rtpParameters }, callback, errback) => {
      try {
        const { id } = await this.produce(this.producerTransport.id, kind, rtpParameters);
        callback({ id });
      } catch (error) {
        errback(error);
      }
    });
  }

  async connectTransport(transportId, dtlsParameters) {
    await fetch('/transport-connect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ transportId, dtlsParameters }),
    });
  }

  async produce(transportId, kind, rtpParameters) {
    const response = await fetch('/produce', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ transportId, kind, rtpParameters }),
    });
    return await response.json();
  }

  async startStreaming(stream) {
    try {
      // Create audio producer
      if (stream.getAudioTracks().length > 0) {
        this.audioProducer = await this.producerTransport.produce({
          track: stream.getAudioTracks()[0],
          codecOptions: {
            opusStereo: true,
            opusDtx: true,
          },
        });
      }

      // Create video producer
      if (stream.getVideoTracks().length > 0) {
        this.videoProducer = await this.producerTransport.produce({
          track: stream.getVideoTracks()[0],
          encodings: [
            { maxBitrate: 100000 },
            { maxBitrate: 300000 },
            { maxBitrate: 900000 },
          ],
          codecOptions: {
            videoGoogleStartBitrate: 1000,
          },
        });
      }
    } catch (error) {
      console.error('Error starting stream:', error);
      throw error;
    }
  }

  async stopStreaming() {
    if (this.videoProducer) {
      await this.videoProducer.close();
      this.videoProducer = null;
    }
    if (this.audioProducer) {
      await this.audioProducer.close();
      this.audioProducer = null;
    }
    if (this.producerTransport) {
      await this.producerTransport.close();
      this.producerTransport = null;
    }
  }
}

export default new WebRTCService();