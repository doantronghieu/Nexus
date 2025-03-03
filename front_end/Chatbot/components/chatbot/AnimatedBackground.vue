<template>
  <div class="animated-bg">
    <div v-for="n in 20" :key="n" class="circle-container">
      <div class="circle"></div>
    </div>
  </div>
</template>

<style scoped>
.animated-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1;
}
.circle-container {
  position: absolute;
  transform: translateY(0);
  animation: fall 15s infinite linear;
}
.circle {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  animation: pulse 2s infinite ease-in-out;
}
@keyframes fall {
  0% { transform: translateY(-100px) rotate(0deg); }
  100% { transform: translateY(100vh) rotate(360deg); }
}
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.5); opacity: 1; }
}

.circle-container:nth-child(2n) .circle {
  background: rgba(74, 144, 226, 0.5);
}

.circle-container:nth-child(3n) .circle {
  background: rgba(255, 107, 107, 0.5);
}

.circle-container:nth-child(1) { left: 5%; animation-delay: 0s; }
.circle-container:nth-child(2) { left: 10%; animation-delay: 2s; }
.circle-container:nth-child(3) { left: 15%; animation-delay: 4s; }
.circle-container:nth-child(4) { left: 20%; animation-delay: 6s; }
.circle-container:nth-child(5) { left: 25%; animation-delay: 8s; }
.circle-container:nth-child(6) { left: 30%; animation-delay: 10s; }
.circle-container:nth-child(7) { left: 35%; animation-delay: 12s; }
.circle-container:nth-child(8) { left: 40%; animation-delay: 14s; }
.circle-container:nth-child(9) { left: 45%; animation-delay: 16s; }
.circle-container:nth-child(10) { left: 50%; animation-delay: 18s; }
.circle-container:nth-child(11) { left: 55%; animation-delay: 20s; }
.circle-container:nth-child(12) { left: 60%; animation-delay: 22s; }
.circle-container:nth-child(13) { left: 65%; animation-delay: 24s; }
.circle-container:nth-child(14) { left: 70%; animation-delay: 26s; }
.circle-container:nth-child(15) { left: 75%; animation-delay: 28s; }
.circle-container:nth-child(16) { left: 80%; animation-delay: 30s; }
.circle-container:nth-child(17) { left: 85%; animation-delay: 32s; }
.circle-container:nth-child(18) { left: 90%; animation-delay: 34s; }
.circle-container:nth-child(19) { left: 95%; animation-delay: 36s; }
.circle-container:nth-child(20) { left: 100%; animation-delay: 38s; }
</style>