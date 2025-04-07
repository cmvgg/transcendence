/*
Cambiar a 4vs4 y no 2vs2
*/

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 10;
const paddleHeight = 100;
const borderHeight = 10;
const maxSpeed = 8;

let ball = {x: canvas.width / 2, y: canvas.height / 2, dx: 4, dy: 4, radius: 7, speed: 4};
let leftPaddle1 = { y: canvas.height / 4, dy: 0, color: "blue" };
let leftPaddle2 = { y: canvas.height / 2, dy: 0, color: "green" };
let rightPaddle1 = { y: canvas.height / 4, dy: 0, color: "red" };
let rightPaddle2 = { y: canvas.height / 2, dy: 0, color: "yellow" };
//let rightPaddle2 = { y: (canvas.height - paddleHeight) / 2, dy: 0, color: "yellow" };
let leftScore = 0;
let rightScore = 0;
//let upScore = 0;
//let downScore = 0;
let maxScore = 5;
let gameOver = false;
let isPaused = false;
let winner = "";

function showGameOverPopup() {
    document.getElementById("winnerText").innerText = winner;
    document.getElementById("gameOverModal").style.display = "flex";
}
document.getElementById("playAgain").addEventListener("click", () => {
    document.getElementById("gameOverModal").style.display = "none";
    resetGame();
});
document.getElementById("goHome").addEventListener("click", () => {
    window.location.href = "../index.html";
});
//Boton de pausa
document.getElementById("pauseButton").addEventListener("click", () => {
    isPaused = !isPaused;
});

//Manejo del teclado
document.addEventListener("keydown", (e) => {
    if (e.key === "w")
        leftPaddle1.dy = -5;
    if (e.key === "s")
        leftPaddle1.dy = 5;
	if (e.key === "t")
        leftPaddle2.dy = -5;
    if (e.key === "g")
        leftPaddle2.dy = 5;
    if (e.key === "ArrowUp")
        rightPaddle1.dy = -5;
    if (e.key === "ArrowDown")
        rightPaddle1.dy = 5;
	if (e.key === "o")
		rightPaddle2.dy = -5;
	if (e.key === "l")
		rightPaddle2.dy = 5;
    if (e.key === "p" || e.key === "P")
        isPaused = !isPaused
});
document.addEventListener("keyup", (e) => {
    if (e.key === "w" || e.key === "s")
        leftPaddle1.dy = 0;
	if (e.key === "t" || e.key === "g")
		leftPaddle2.dy = 0;
    if (e.key === "ArrowUp" || e.key === "ArrowDown")
        rightPaddle1.dy = 0;
	if (e.key === "o" || e.key === "l")
		rightPaddle2.dy = 0;
});

function update() {
	let prevBallX = ball.x;
	let prevBallY = ball.y;

	if (gameOver || isPaused)
		return;

	//Mover paletas
	leftPaddle1.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle1.y + leftPaddle1.dy));
	leftPaddle2.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle2.y + leftPaddle2.dy));
    rightPaddle1.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle1.y + rightPaddle1.dy));
    rightPaddle2.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle2.y + rightPaddle2.dy));

	//Mover la pelota
	ball.x += ball.dx;
	ball.y += ball.dy;

	//Rebote en las paletas
	if (ball.y + ball.radius >= canvas.height || ball.y - ball.radius <= 0)
		ball.dy = -ball.dy;

	//Rebote en las paletas
	if (ball.x - ball.radius < paddleWidth && ball.y > leftPaddle1.y && ball.y < leftPaddle1.y + paddleHeight)
        ball.dx *= -1;
	if (ball.x - ball.radius < paddleWidth && ball.y > leftPaddle2.y && ball.y < leftPaddle2.y + paddleHeight)
        ball.dx *= -1;
    if (ball.x + ball.radius > canvas.width - paddleWidth && ball.y > rightPaddle1.y && ball.y < rightPaddle1.y + paddleHeight)
        ball.dx *= -1;
	if (ball.x + ball.radius > canvas.width - paddleWidth && ball.y > rightPaddle2.y && ball.y < rightPaddle2.y + paddleHeight)
        ball.dx *= -1;

    //Checkeo de puntuacion
    if (ball.x - ball.radius < 0) {
        rightScore++;
        checkGameOver();
    } else if (ball.x + ball.radius > canvas.width) {
        leftScore++;
        checkGameOver();
    }
}

function checkGameOver() {
    if (leftScore >= maxScore) {
        gameOver = true;
        winner = "¡Jugador de la izquierda ha ganado!";
    } else if (rightScore >= maxScore) {
        gameOver = true;
        winner = "¡Jugador de la derecha ha ganado!";
    } /* else if (upScore >= maxScore) {
        gameOver = true;
        winner = "¡Jugador de arriba ha ganado!";
    } else if (downScore >= maxScore) {
        gameOver = true;
        winner = "¡Jugador de abajo ha ganado!";
    } */
    if (gameOver) {
        showGameOverPopup();
    } else {
        resetBall();
    }
}

function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.speed = 4;
    ball.radius = 7;
    if (Math.random() > 0.5) {
        ball.dx = ball.speed * 1;
    } else {
        ball.dx = ball.speed * -1;
    }
    if (Math.random() > 0.5) {
        ball.dy = ball.speed * 1;
    } else {
        ball.dy = ball.speed * -1;
    }
}

function resetGame() {
    leftScore = 0;
    rightScore = 0;
    gameOver = false;
    winner = "";
    isPaused = false;
    //Resetear paletas
    leftPaddle1.y = (canvas.height - paddleHeight) / 2;
    leftPaddle2.y = (canvas.height - paddleHeight) / 2;
    rightPaddle1.y = (canvas.height - paddleHeight) / 2;
    rightPaddle2.y = (canvas.height - paddleHeight) / 2;
    resetBall();
    gameLoop();
}

function draw() {
	ctx.clearRect(0, 0, canvas.width, canvas.height);

	if (!gameOver) {
		//Dibujar bordes
		ctx.fillStyle = "white";
		ctx.fillRect(0, 0, canvas.width, borderHeight);
		ctx.fillRect(0, canvas.height - borderHeight, canvas.width, borderHeight);

		//Dibujar paletas
		ctx.fillStyle = leftPaddle1.color;
		ctx.fillRect(0, leftPaddle1.y, paddleWidth, paddleHeight);
		ctx.fillStyle = leftPaddle2.color;
		ctx.fillRect(0, leftPaddle2.y, paddleWidth, paddleHeight);
		ctx.fillStyle = rightPaddle1.color;
		ctx.fillRect(canvas.width - paddleWidth, rightPaddle1.y, paddleWidth, paddleHeight);
		ctx.fillStyle = rightPaddle2.color;
		ctx.fillRect(canvas.width - paddleWidth, rightPaddle2.y, paddleWidth, paddleHeight);

		//Dibujar pelota
		ctx.beginPath();
		ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
		ctx.fill();
		ctx.closePath();

		//Dibujar marcador
		ctx.font = "30px Arial";
		ctx.fillText(leftScore, canvas.width / 4, 50);
		ctx.fillText(rightScore, canvas.width * 3 / 4, 50);
	}
}

function gameLoop() {
	update();
	draw();
	if (!gameOver)
		requestAnimationFrame(gameLoop);
}

gameLoop();