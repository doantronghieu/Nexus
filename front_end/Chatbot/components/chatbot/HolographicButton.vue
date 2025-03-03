<template>
  <button 
    @click="$emit('click')" 
    class="holographic-button"
  >
    <slot></slot>
  </button>
</template>

<style scoped>
.holographic-button {
  background: linear-gradient(45deg, rgba(74, 144, 226, 0.3), rgba(86, 55, 221, 0.3));
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  padding: 10px 20px;
  color: #fff;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.holographic-button::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    to bottom right,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(45deg);
  animation: holographic 3s linear infinite;
}

.holographic-button:hover {
  box-shadow: 0 0 15px rgba(74, 144, 226, 0.5);
}

@keyframes holographic {
  0% { transform: rotate(45deg) translateY(-100%); }
  100% { transform: rotate(45deg) translateY(100%); }
}
</style>