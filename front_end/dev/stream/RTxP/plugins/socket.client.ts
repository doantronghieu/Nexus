import { io } from 'socket.io-client';

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig();
  const socket = io(config.public.wsPath);

  return {
    provide: {
      socket: socket
    }
  };
});