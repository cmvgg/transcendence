/**********************
 * 1. Lógica del Torneo
 **********************/

class Tournament {
	constructor(players) {
	  this.players = players.slice();
	  this.match = this.createBracket(this.players);
	  this.currentRound = 0;
	}
	
	//Crea el bracket inicial; si la cantidad es impar, se agrega "BYE"
	createBracket(players) {
		let matches = [];
		if (players.length % 2 !== 0) {
			players.push("BYE");
		}
		for (let i = 0; i < players.length; i += 2) {
			matches.push({
				player1: players[i],
				player2: players[i + 1],
				winner: null
			});
		}
		return [matches]; //Cada elemento del array representa una ronda
	}
	
	//Devuelve el partido actual de la ronda actual
	getCurrentMatch() {
		const currentMatches = this.match[this.currentRound];
		return currentMatches.find(match => match.winner === null);
	}
	
	//Registra el ganador en el partido y, si la ronda abaca, genera la siguiente ronda
	setWinner(winner) {
		const match = this.getCurrentMatch();
		if (!match)
			return;
		match.winner = winner;
		log(`Partido finalizado: ${match.player1} vs ${match.player2} - Ganador: ${winner}\n`);
		
		//Si la ronda actual acabó, generar la siguiente ronda
		if (this.match[this.currentRound].every(m => m.winner !== null)) {
			this.generateNextRound();
		}
	}
	
	generateNextRound() {
		const winners = this.match[this.currentRound].map(match => match.winner);
		if (winners.length === 1) {
			log(`\n\n¡El campeón del torneo es ${winners[0]}!`);
			return;
		}
		
		let nextRoundMatches = [];
		if (winners.length % 2 !== 0) {
			winners.push("BYE");
		}
		for (let i = 0; i < winners.length; i += 2) {
			nextRoundMatches.push({
				player1: winners[i],
				player2: winners[i + 1],
				winner: null
			});
		}
		this.match.push(nextRoundMatches);
		this.currentRound++;
		log(`Iniciando ronda ${this.currentRound + 1}`);
		const nextMatch = this.getCurrentMatch();
		//log(`Próximo partido: ${nextMatch.player1} vs ${nextMatch.player2}`);
	}
	
	isTournamentOver() {
		const lastRound = this.match[this.match.length - 1];
		return lastRound.length === 1 && lastRound[0].winner !== null;
	}
}

/*********************************************
 * 2. Redirigir console.log al elemento HTML *
*********************************************/
function logMessage(message) {
	const logDiv = document.getElementById("log");
	const p = document.createElement("p");
	p.innerHTML = message.replace(/\n/g, "<br>"); // Reemplaza \n por <br>
	logDiv.appendChild(p);
	logDiv.scrollTop = logDiv.scrollHeight;
}

const originalConsoleLog = console.log;
function log(...args) {
	originalConsoleLog(...args);
	args.forEach(arg => {
		logMessage(typeof arg === 'object' ? JSON.stringify(arg) : arg);
	});
}


/***********************
 * 3. Lógica del Juego *
***********************/
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 10;
const paddleHeight = 100;
const borderHeight = 10;

let leftPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0 };
let rightPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0 };
let angle;
do {
	angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
} while (Math.abs(Math.cos(angle)) > 0.99);
let directionX = Math.random() < 0.5 ? 1 : -1;
let directionY = Math.random() < 0.5 ? 1 : -1;
let ball = {
	x: canvas.width / 2,
    y: canvas.height / 2,
    dx: directionX * 4 * Math.cos(angle),
    dy: directionY * 4 * Math.sin(angle),
    radius: 7,
    speed: 6
};
let leftScore = 0;
let rightScore = 0;
let maxScore = 5;
let gameOver = false;
let isPaused = false;
let winner = "";

document.addEventListener("keydown", (e) => {
	if (e.key === "w") leftPaddle.dy = -5;
	if (e.key === "s") leftPaddle.dy = 5;
	if (e.key === "ArrowUp") rightPaddle.dy = -5;
	if (e.key === "ArrowDown") rightPaddle.dy = 5;
	if (e.key.toLowerCase() === "p") isPaused = !isPaused;
});
document.addEventListener("keyup", (e) => {
	if (e.key === "w" || e.key === "s") leftPaddle.dy = 0;
	if (e.key === "ArrowUp" || e.key === "ArrowDown") rightPaddle.dy = 0;
});
//Boton de pausa
document.getElementById("pauseButton").addEventListener("click", () => {
	isPaused = !isPaused;
});
document.getElementById("goHome").addEventListener("click", () => {
	window.location.href = "../index.html";
});

function update() {
	let prevBallX = ball.x;
    let prevBallY = ball.y;

	if (gameOver || isPaused)
		return;
	
	let extraSpeed = Math.sqrt(ball.dx ** 2 + ball.dy ** 2);
    ball.dx *= (extraSpeed + 0.01) / extraSpeed;
    ball.dy *= (extraSpeed + 0.01) / extraSpeed;
	
	leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle.y + leftPaddle.dy));
	rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle.y + rightPaddle.dy));
	
	ball.x += ball.dx;
	ball.y += ball.dy;
	
	if (ball.y - ball.radius < borderHeight || ball.y + ball.radius > canvas.height - borderHeight)
		ball.dy *= -1;
	
	//Rebote en las paletas con efecto
	if(ball.dx < 0) {
		if (prevBallX + ball.radius > paddleWidth && ball.x - ball.radius <= paddleWidth && ball.y + ball.radius > leftPaddle.y
            && ball.y - ball.radius < leftPaddle.y + paddleHeight) {   
				ball.dx *= -1;
				ball.dy += (1 - (50 - (leftPaddle.y - ball.y)) / 100);
				ball.x = paddleWidth + ball.radius + 0.1;
			}
		}
		if (ball.dx > 0) { 
			if (prevBallX - ball.radius < canvas.width - paddleWidth && ball.x + ball.radius >= canvas.width - paddleWidth
				&& ball.y + ball.radius > rightPaddle.y && ball.y - ball.radius < rightPaddle.y + paddleHeight) {
					ball.dx *= -1;
            ball.dy += (1 - (50 - (rightPaddle.y - ball.y)) / 100);
            ball.x = canvas.width - paddleWidth - ball.radius - 0.1;
        }
    }
	
	if (ball.x - ball.radius < 0) {
		rightScore++;
		checkGameOver();
	} else if (ball.x + ball.radius > canvas.width) {
		leftScore++;
		checkGameOver();
	}
}

//Verifica si llegó al puntaje máximo para finalizar el partido
function checkGameOver() {
	if (leftScore >= maxScore) {
		gameOver = true;
		winner = currentMatch.player1;
		endMatch();
	} else if (rightScore >= maxScore) {
		gameOver = true;
		winner = currentMatch.player2;
		endMatch();
	} else {
		resetBall();
	}
}


function resetBall() {
	ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.speed = 4;
    ball.radius = 7;
	
    let angle;
    do {
		angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
    } while (Math.abs(Math.cos(angle)) > 0.99);
	
    let directionX = Math.random() < 0.5 ? 1 : -1;
    let directionY = Math.random() < 0.5 ? 1 : -1;
	
    ball.dx = directionX * ball.speed * Math.cos(angle);
    ball.dy = directionY * ball.speed * Math.sin(angle);
}

//Reinicia el juego para el siguiente partido del torneo
function resetGameForNextMatch() {
	leftScore = 0;
	rightScore = 0;
	gameOver = false;
	isPaused = false;
	leftPaddle.y = (canvas.height - paddleHeight) / 2;
	rightPaddle.y = (canvas.height - paddleHeight) / 2;
	resetBall();
	currentMatch = tournament.getCurrentMatch();
	log(`\nNuevo partido: ${currentMatch.player1} vs ${currentMatch.player2}`);
	gameLoop();
}

//Finaliza el partido, notifica al torneo y, si aún no termina el torneo, reinicia para el siguiente partido
function endMatch() {
	tournament.setWinner(winner);
	if (!tournament.isTournamentOver()) {
		setTimeout(resetGameForNextMatch, 2000);
	}
}

function draw() {
	ctx.fillStyle = "white";
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.fillRect(0, leftPaddle.y, paddleWidth, paddleHeight);
	ctx.fillRect(canvas.width - paddleWidth, rightPaddle.y, paddleWidth, paddleHeight);
	ctx.beginPath();
	ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
	ctx.fill();
	
	ctx.font = "60px Courier New";
	ctx.fillText(leftScore, canvas.width / 3, 60);
	ctx.fillText(rightScore, (canvas.width / 4) * 2.5, 60);
	
	if (isPaused) {
		ctx.font = "30px Courier New";
		ctx.fillText("PAUSED", canvas.width / 2 - 60, canvas.height / 2);
	}
}

function gameLoop() {
	update();
	draw();
	if (!gameOver) {
		requestAnimationFrame(gameLoop);
	}
}

//Inicio del torneo
const players = ["Bob", "Alice", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi"];
const tournament = new Tournament(players);
let currentMatch = tournament.getCurrentMatch();
//log("Inicio del torneo");
//log("Jugadores: " + players);
//log(`Primer partido: ${currentMatch.player1} vs ${currentMatch.player2}\n`);

gameLoop();



/***************************
* 4. Lógica del Formulario *
***************************/

/* const modelName = document.getElementById('django.contrib.auth.models.User').dataset.modelName;
const form = document.getElementById(modelName + '_tournament'); */

/* console.log("Formulario de Torneo");

const modelStart = document.getElementById('django.contrib.auth.models.Tournament' + '_start');
const modelEnd = document.getElementById('django.contrib.auth.models' + '_end');

console.log(modelStart); */
//console.log(modelStart.value);

