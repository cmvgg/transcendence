const canvas = document.getElementById("tronCanvas");
const ctx = canvas.getContext("2d");

let player1 = {
	x: 0,
	y: canvas.height / 2,
	dx: 2,
	dy: 0,
	color: "blue",
	trail: []
};
let player2 = {
	x: canvas.width - 20,
	y: canvas.height / 2,
	dx: -2,
	dy: 0,
	color: "red",
	trail: []
};
let gameOver = false;
let isPaused = false;
let winner = "";

document.addEventListener("keydown", (e) => {
	if (e.key === "w" && player1.dy === 0) {
		player1.dx = 0;
		player1.dy = -2;
	}
	if (e.key === "a" && player1.dx === 0) {
		player1.dx = -2;
		player1.dy = 0;
	}
	if (e.key === "d" && player1.dx === 0) {
		player1.dx = 2;
		player1.dy = 0;
	}
	if (e.key === "s" && player1.dy === 0) {
		player1.dx = 0;
		player1.dy = 2;
	}
	if (e.key === "ArrowUp" && player2.dy === 0) {
		player2.dx = 0;
		player2.dy = -2;
	}
	if (e.key === "ArrowLeft" && player2.dx === 0) {
		player2.dx = -2;
		player2.dy = 0;
	}
	if (e.key === "ArrowRight" && player2.dx === 0) {
		player2.dx = 2;
		player2.dy = 0;
	}
	if (e.key === "ArrowDown" && player2.dy === 0) {
		player2.dx = 0;
		player2.dy = 2;
	}
	if (e.key === "p" || e.key === "P")
		isPaused = !isPaused
});

function checkCollision(player) {
	//Colision con las paredes
	if(player.x < 0 || player.x >= canvas.width || player.y < 0 || player.y >= canvas.height) {
		gameOver = true;
		if (player === player1) {
			winner = "Player 2";
		} else {
			winner = "Player 1";
		}
		return true;
	}

	//Colision con su propia estela
	for (let i = 0; i < player.trail.length - 1; i++) {
		if (player.x === player.trail[i].x && player.y === player.trail[i].y) {
			gameOver = true;
			if (player === player1) {
				winner = "Player 2";
			} else {
				winner = "Player 1";
			}
			return true;
		}
	}

	//Colision con la estela del otro jugador
	let otherPlayer;
	if (player === player1) {
		otherPlayer = player2;
	} else {
		otherPlayer = player1;
	}
	for (let i = 0; i < otherPlayer.trail.length; i++) {
		if (player.x === otherPlayer.trail[i].x && player.y === otherPlayer.trail[i].y) {
			gameOver = true;
			if (player === player1) {
				winner = "Player 2";
			} else {
				winner = "Player 1";
			}
			return true;
		}
	}

	return false;
}

function update() {
	if (isPaused || gameOver) {
		return ;
	}

	//Actualizar la posición de los jugadores
	player1.x += player1.dx;
	player1.y += player1.dy;
	player2.x += player2.dx;
	player2.y += player2.dy;

	//Agregar la posición actual a la estela
	player1.trail.push({x: player1.x, y: player1.y});
	player2.trail.push({x: player2.x, y: player2.y});

	checkCollision(player1);
	checkCollision(player2);
}

function draw() {
	ctx.clearRect(0, 0, canvas.width, canvas.height);

	// Dibujar trayectorias sin huecos
	for (let i = 1; i < player1.trail.length; i++) {
		ctx.strokeStyle = player1.color;
		ctx.lineWidth = 2;
		ctx.beginPath();
		ctx.moveTo(player1.trail[i - 1].x + 1.5, player1.trail[i - 1].y + 1.5);
		ctx.lineTo(player1.trail[i].x + 1.5, player1.trail[i].y + 1.5);
		ctx.stroke();
	}
	for (let i = 1; i < player2.trail.length; i++) {
		ctx.strokeStyle = player2.color;
		ctx.lineWidth = 2;
		ctx.beginPath();
		ctx.moveTo(player2.trail[i - 1].x + 1.5, player2.trail[i - 1].y + 1.5);
		ctx.lineTo(player2.trail[i].x + 1.5, player2.trail[i].y + 1.5);
		ctx.stroke();
	}

	// Dibujar jugadores más pequeños
	ctx.fillStyle = player1.color;
	ctx.fillRect(player1.x, player1.y, 3, 3);
	ctx.fillStyle = player2.color;
	ctx.fillRect(player2.x, player2.y, 3, 3);

	if (gameOver) {
		ctx.fillStyle = "black";
		ctx.font = "30px Arial";
		ctx.fillText(winner + " wins!", canvas.width / 2 - 100, canvas.height / 2);
	}
}

function gameLoop() {
	if (!gameOver) {
		update();
		draw();
		requestAnimationFrame(gameLoop);
	}
}

gameLoop();