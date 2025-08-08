window.onload = async function () {
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let playerUsername = "";

// 👇 Fetch del jugador humano
async function fetchPlayer() {
	try {
		const response = await fetch("http://localhost:8000/get_players_for_game?game_type=1vsIA");
		const data = await response.json();
		if (data.players && data.players.length > 0) {
			playerUsername = data.players[0].username;
			console.log("Jugador cargado:", playerUsername);
		} else {
			console.error("No se pudo obtener jugador.");
		}
	} catch (error) {
		console.error("Error obteniendo jugador:", error);
	}
}

// 👇 Enviar stats al backend
async function updateUserProfile(username, wins, losses) {
	try {
		await fetch("http://localhost:8000/update_user_profile/", {
			method: "POST",
			headers: {"Content-Type": "application/json"},
			body: JSON.stringify({username, wins, losses})
		});
	} catch (error) {
		console.error("Error actualizando perfil:", error);
	}
}

await fetchPlayer(); // Esperamos al jugador antes de arrancar

const paddleWidth = 3;
const paddleHeight = 30;
const borderHeight = 5;
const maxBallSpeed = 8;

const AI_CONFIG = {
	speed: 3, reactionThreshold: 10, difficultyLevel: 'medium',
	difficulties: {
		easy: { speedMultiplier: 0.2, reactionThreshold: 15 },
		medium: { speedMultiplier: 0.0001, reactionThreshold: 10 },
		hard: { speedMultiplier: 0.7, reactionThreshold: 5 }
	}
};

let leftPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0, color: "white" };
let rightPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0, color: "white" };

let angle;
do {
	angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
} while (Math.abs(Math.cos(angle)) > 0.99);

let directionX = Math.random() < 0.5 ? 1 : -1;
let directionY = Math.random() < 0.5 ? 1 : -1;

let ball = {
	x: canvas.width / 2,
	y: canvas.height / 2,
	dx: directionX * 2 * Math.cos(angle),
	dy: directionY * 2 * Math.sin(angle),
	radius: 3, speed: 2
};

let leftScore = 0;
let rightScore = 0;
let maxScore = 5;
let colorEffect = false;
let gameOver = false;
let isPaused = true;
let winner = "";

const difficultySelect = document.getElementById('difficultySelect');
AI_CONFIG.difficultyLevel = difficultySelect.value;

document.addEventListener("keydown", (e) => {
	if (!isPaused) {
		if (e.key === "w") leftPaddle.dy = -5;
		if (e.key === "s") leftPaddle.dy = 5;
	}
});
document.addEventListener("keyup", (e) => {
	if (e.key === "w" || e.key === "s") leftPaddle.dy = 0;
});
document.addEventListener("keydown", (e) => {
	if (e.key === "p" || e.key === "P") isPaused = !isPaused;
});

document.getElementById("pauseButton").addEventListener("click", () => isPaused = true);
document.getElementById("startButton").addEventListener("click", () => isPaused = false);

difficultySelect.addEventListener('change', (e) => {
	AI_CONFIG.difficultyLevel = e.target.value;
	updateAIDifficulty();
});

function updateAIDifficulty() {
	const difficulty = AI_CONFIG.difficulties[AI_CONFIG.difficultyLevel];
	AI_CONFIG.reactionThreshold = difficulty.reactionThreshold;
	//cambiar la velocidad
	rightPaddle.speed = AI_CONFIG.speed + difficulty.speedMultiplier;
}

function predictBallY() {
	if (ball.dx <= 0) return ball.y;
	let tempX = ball.x, tempY = ball.y, tempDx = ball.dx, tempDy = ball.dy;
	while (tempX < canvas.width - paddleWidth) {
		tempX += tempDx;
		tempY += tempDy;
		if (tempY - ball.radius < borderHeight || tempY + ball.radius > canvas.height - borderHeight)
			tempDy *= -1;
	}
	return tempY;
}

function moveAI() {
	if (isPaused) return;
	let center = rightPaddle.y + paddleHeight / 2;
	let targetY = predictBallY();
	if (Math.abs(center - targetY) > AI_CONFIG.reactionThreshold) {
		if (center < targetY) rightPaddle.y += rightPaddle.speed;
		else rightPaddle.y -= rightPaddle.speed;
	}
}

function update() {
	if (gameOver || isPaused) return;

	ball.dx *= 1.005;
	ball.dy *= 1.005;

	leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle.y + leftPaddle.dy));
	moveAI();
	rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle.y));

	ball.x += ball.dx;
	ball.y += ball.dy;

	if (ball.y - ball.radius < borderHeight || ball.y + ball.radius > canvas.height - borderHeight)
		ball.dy *= -1;

	if (ball.dx < 0 &&
		ball.x - ball.radius <= paddleWidth &&
		ball.y > leftPaddle.y && ball.y < leftPaddle.y + paddleHeight)
	{
		ball.dx *= -1;
		ball.x = paddleWidth + ball.radius + 0.1;
	}

	if (ball.dx > 0 &&
		ball.x + ball.radius >= canvas.width - paddleWidth &&
		ball.y > rightPaddle.y && ball.y < rightPaddle.y + paddleHeight)
	{
		ball.dx *= -1;
		ball.x = canvas.width - paddleWidth - ball.radius - 0.1;
	}

	if (ball.x - ball.radius < 0) {
		rightScore++;
		checkGameOver();
	} else if (ball.x + ball.radius > canvas.width) {
		leftScore++;
		checkGameOver();
	}
}

async function checkGameOver() {
    if (leftScore >= maxScore) {
        gameOver = true;
        winner = "¡Has ganado!";
        await updateUserProfile(playerUsername, 1, 0); // Actualizar estadísticas del jugador
        await updateUsersInTournament(playerUsername, 1, 0); // Actualizar UsersInTournament
        await syncTournamentStats(); // Sincronizar datos con TournamentStats
    } else if (rightScore >= maxScore) {
        gameOver = true;
        winner = "La IA ha ganado...";
        await updateUserProfile(playerUsername, 0, 1); // Actualizar estadísticas del jugador
        await updateUsersInTournament(playerUsername, 0, 1); // Actualizar UsersInTournament
        await syncTournamentStats(); // Sincronizar datos con TournamentStats
    }

    if (gameOver) {
        alert(winner);
    } else {
        resetBall();
    }
}

// Nueva función para actualizar UsersInTournament
async function updateUsersInTournament(username, wins, losses) {
    try {
        const response = await fetch('/update_user_profile/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ username, wins, losses })
        });

        const data = await response.json();
        if (!response.ok) {
            console.error("Error actualizando UsersInTournament:", data);
        } else {
            console.log("UsersInTournament actualizado:", data);
        }
    } catch (error) {
        console.error("Error al actualizar UsersInTournament:", error.message);
    }
}

// Función para sincronizar datos con TournamentStats
async function syncTournamentStats() {
    try {
        const response = await fetch('/sync_tournament_stats/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });
        const data = await response.json();
        console.log(data.message || "Sincronización completada.");
    } catch (error) {
        console.error("Error al sincronizar estadísticas:", error.message);
    }
}

function resetBall() {
	ball.x = canvas.width / 2;
	ball.y = canvas.height / 2;
	ball.speed = 2;
	ball.radius = 3;
	let angle;
	do {
		angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
	} while (Math.abs(Math.cos(angle)) > 0.99);
	let directionX = Math.random() < 0.5 ? 1 : -1;
	let directionY = Math.random() < 0.5 ? 1 : -1;
	ball.dx = directionX * ball.speed * Math.cos(angle);
	ball.dy = directionY * ball.speed * Math.sin(angle);
}

function draw() {
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	if (!gameOver) {
		ctx.fillStyle = leftPaddle.color;
		ctx.fillRect(0, leftPaddle.y, paddleWidth, paddleHeight);
		ctx.fillStyle = "white";
		ctx.fillRect(canvas.width - paddleWidth, rightPaddle.y, paddleWidth, paddleHeight);

		ctx.font = "20px Courier New";
		ctx.fillText(leftScore, canvas.width / 3, 20);
		ctx.fillText(rightScore, (canvas.width / 4) * 2.5, 20);

		if (isPaused) {
			ctx.font = "20px Courier New";
			ctx.fillText("PAUSADO", canvas.width / 2 - 50, canvas.height / 2);
		}

		ctx.beginPath();
		ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
		ctx.fillStyle = "white";
		ctx.fill();
	}
}

function gameLoop() {
	if (!gameOver) {
		update();
		draw();
		requestAnimationFrame(gameLoop);
	}
}

updateAIDifficulty();
gameLoop();
};
