const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Esperar a que la fuente cargue antes de dibujar
document.fonts.ready.then(() => {
  ctx.font = "20px Bit5x3";
  ctx.fillStyle = "white";
  ctx.fillText("1", canvas.width / 3, 60);
  ctx.fillText("0", (canvas.width / 4) * 2.5, 60);
});
