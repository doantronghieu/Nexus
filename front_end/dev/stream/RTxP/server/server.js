import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import * as mediasoup from 'mediasoup';
import NodeMediaServer from 'node-media-server';
import { config } from './config.js';
import os from 'os';

class MediaServer {
  constructor() {
    this.workers = [];
    this.nextWorkerIndex = 0;
    this.rooms = new Map();
    this.peers = new Map();
    
    this.app = express();
    this.httpServer = createServer(this.app);
    this.io = new Server(this.httpServer, {
      cors: {
        origin: '*',
        methods: ['GET', 'POST']
      }
    });
    
    this.app.use(express.json());
    this.setupSocketHandlers();
    this.initializeMediaSoup();
    this.initializeRTMP();
    this.setupRoutes();
  }

  setupSocketHandlers() {
    this.io.on('connection', (socket) => {
      console.log('Client connected:', socket.id);

      socket.on('create-room', async (data, callback) => {
        try {
          const { roomId } = data;
          const router = await this.createRouter();
          this.rooms.set(roomId, { router, peers: new Map() });
          callback({ success: true, roomId });
        } catch (error) {
          callback({ success: false, error: error.message });
        }
      });

      socket.on('join-room', async (data, callback) => {
        try {
          const { roomId, peerId } = data;
          const roomData = this.rooms.get(roomId);
          
          if (!roomData) {
            throw new Error('Room not found');
          }

          const transport = await this.createWebRtcTransport(roomData.router);
          roomData.peers.set(peerId, { transport, socket });
          
          callback({
            success: true,
            routerRtpCapabilities: roomData.router.rtpCapabilities,
            transportOptions: {
              id: transport.id,
              iceParameters: transport.iceParameters,
              iceCandidates: transport.iceCandidates,
              dtlsParameters: transport.dtlsParameters,
            },
          });
        } catch (error) {
          callback({ success: false, error: error.message });
        }
      });

      socket.on('disconnect', () => {
        console.log('Client disconnected:', socket.id);
      });
    });
  }

  async initializeMediaSoup() {
    try {
      const { numWorkers = os.cpus().length } = config.mediasoup;

      for (let i = 0; i < numWorkers; i++) {
        const worker = await mediasoup.createWorker({
          logLevel: config.mediasoup.worker.logLevel,
          logTags: config.mediasoup.worker.logTags,
          rtcMinPort: config.mediasoup.worker.rtcMinPort,
          rtcMaxPort: config.mediasoup.worker.rtcMaxPort,
        });

        worker.on('died', () => {
          console.error(`mediasoup Worker ${worker.pid} died`);
          setTimeout(() => process.exit(1), 2000);
        });

        this.workers.push(worker);
      }
    } catch (error) {
      console.error('Failed to initialize mediasoup:', error);
      process.exit(1);
    }
  }

  initializeRTMP() {
    const nms = new NodeMediaServer(config.rtmp);
    nms.run();
  }

  setupRoutes() {
    this.app.post('/api/create-room', async (req, res) => {
      try {
        const { roomId } = req.body;
        const router = await this.createRouter();
        this.rooms.set(roomId, { router, peers: new Map() });
        res.status(200).json({ roomId });
      } catch (error) {
        console.error('Error creating room:', error);
        res.status(500).json({ error: error.message });
      }
    });

    this.app.post('/api/join-room', async (req, res) => {
      try {
        const { roomId, peerId } = req.body;
        const roomData = this.rooms.get(roomId);
        
        if (!roomData) {
          throw new Error('Room not found');
        }

        const transport = await this.createWebRtcTransport(roomData.router);
        roomData.peers.set(peerId, { transport });
        
        res.status(200).json({
          routerRtpCapabilities: roomData.router.rtpCapabilities,
          transportOptions: {
            id: transport.id,
            iceParameters: transport.iceParameters,
            iceCandidates: transport.iceCandidates,
            dtlsParameters: transport.dtlsParameters,
          },
        });
      } catch (error) {
        console.error('Error joining room:', error);
        res.status(500).json({ error: error.message });
      }
    });
  }

  async createRouter() {
    const worker = this.workers[this.nextWorkerIndex];
    this.nextWorkerIndex = (this.nextWorkerIndex + 1) % this.workers.length;
    return await worker.createRouter({ mediaCodecs: config.mediasoup.router.mediaCodecs });
  }

  async createWebRtcTransport(router) {
    return await router.createWebRtcTransport({
      ...config.mediasoup.webRtcTransport,
      enableUdp: true,
      enableTcp: true,
      preferUdp: true,
    });
  }

  async start() {
    const port = process.env.PORT || 3000;
    this.httpServer.listen(port, () => {
      console.log(`Server listening on port ${port}`);
    });
  }
}

const server = new MediaServer();
server.start();