<template>
  <canvas ref="canvas" class="w-full h-24 mt-4"></canvas>
</template>

<script setup lang="ts">
const canvas = ref<HTMLCanvasElement | null>(null)
const store = useWakeWordStore()

onMounted(() => {
  if (!canvas.value) return

  const ctx = canvas.value.getContext('2d')
  if (!ctx) return

  const analyser = store.audioContext?.createAnalyser()
  if (!analyser) return

  analyser.fftSize = 2048
  const bufferLength = analyser.frequencyBinCount
  const dataArray = new Uint8Array(bufferLength)

  const draw = () => {
    if (!canvas.value || !ctx || !analyser) return

    const width = canvas.value.width
    const height = canvas.value.height

    requestAnimationFrame(draw)

    analyser.getByteTimeDomainData(dataArray)

    ctx.fillStyle = 'rgb(200, 200, 200)'
    ctx.fillRect(0, 0, width, height)
    ctx.lineWidth = 2
    ctx.strokeStyle = 'rgb(0, 0, 0)'
    ctx.beginPath()

    const sliceWidth = width / bufferLength
    let x = 0

    for (let i = 0; i < bufferLength; i++) {
      const v = dataArray[i] / 128.0
      const y = v * height / 2

      if (i === 0) {
        ctx.moveTo(x, y)
      } else {
        ctx.lineTo(x, y)
      }

      x += sliceWidth
    }

    ctx.lineTo(width, height / 2)
    ctx.stroke()
  }

  draw()
})
</script>