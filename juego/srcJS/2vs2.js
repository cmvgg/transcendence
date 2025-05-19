const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 10;
const paddleHeight = 100;
const borderHeight = 10;
const maxSpeed = 8;

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
    radius: 7, speed: 6
};
let leftPaddle = { y: (canvas.height - paddleHeight) / 4, dy: 0, color: "blue" };
let leftPaddle2 = { y: (canvas.height - paddleHeight) / 1.5, dy: 0, color: "green" };
let rightPaddle = { y: (canvas.height - paddleHeight) / 4, dy: 0, color: "red" };
let rightPaddle2 = { y: (canvas.height - paddleHeight) / 1.5, dy: 0, color: "yellow" };
let leftScore = 0;
let rightScore = 0;
let maxScore = 5;
let gameOver = false;
let isPaused = false;
let winner = "";

//Botones
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
document.getElementById("pauseButton").addEventListener("click", () => {
    isPaused = !isPaused;
});

//Manejo del teclado
document.addEventListener("keydown", (e) => {
    if (e.key === "w")
        leftPaddle.dy = -5;
    if (e.key === "s")
        leftPaddle.dy = 5;
    if (e.key === "ArrowUp")
        rightPaddle.dy = -5;
    if (e.key === "ArrowDown")
        rightPaddle.dy = 5;
    if (e.key === "i")
        leftPaddle2.dy = -5;
    if (e.key === "k")
        leftPaddle2.dy = 5;
    if (e.key === "8")
        rightPaddle2.dy = -5;
    if (e.key === "5")
        rightPaddle2.dy = 5;
    if (e.key === "p" || e.key === "P")
        isPaused = !isPaused
});
document.addEventListener("keyup", (e) => {
    if (e.key === "w" || e.key === "s")
        leftPaddle.dy = 0;
    if (e.key === "ArrowUp" || e.key === "ArrowDown")
        rightPaddle.dy = 0;
    if (e.key === "i" || e.key === "k")
        leftPaddle2.dy = 0;
	if (e.key === "8" || e.key === "5")
		rightPaddle2.dy = 0;
});

function update() {
    let prevBallX = ball.x;
    let prevBallY = ball.y;

    if (gameOver || isPaused)
        return;

    let extraSpeed = Math.sqrt(ball.dx ** 2 + ball.dy ** 2);
    ball.dx *= (extraSpeed + 0.01) / extraSpeed;
    ball.dy *= (extraSpeed + 0.01) / extraSpeed;

    //Mover paletas más rápido
    leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle.y + leftPaddle.dy * 1.5));
    rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle.y + rightPaddle.dy * 1.5));
    leftPaddle2.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle2.y + leftPaddle2.dy * 1.5));
    rightPaddle2.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle2.y + rightPaddle2.dy * 1.5));

    //Mover la pelota
    ball.x += ball.dx;
    ball.y += ball.dy;

    //Rebote en las paletas
    if (ball.y + ball.radius >= canvas.height || ball.y - ball.radius <= 0)
        ball.dy *= -1;

    //Rebote en las paletas
    if (ball.dx < 0) {
        if (ball.x - ball.radius < paddleWidth && ball.y > leftPaddle.y && ball.y < leftPaddle.y + paddleHeight) {
            ball.dx *= -1;
            ball.dy += (1 - (50 - (leftPaddle.y - ball.y)) / 100);
            ball.x = paddleWidth + ball.radius + 0.1;
        }
        if (ball.x - ball.radius < paddleWidth && ball.y > leftPaddle2.y && ball.y < leftPaddle2.y + paddleHeight) {
            ball.dx *= -1;
            ball.dy += (1 - (50 - (leftPaddle2.y - ball.y)) / 100);
            ball.x = paddleWidth + ball.radius + 0.1;
        }
    }
      
    if (ball.dx > 0) {
        if (ball.x + ball.radius > canvas.width - paddleWidth && ball.y > rightPaddle.y && ball.y < rightPaddle.y + paddleHeight) {
            ball.dx *= -1;
            ball.dy += (1 - (50 - (rightPaddle.y - ball.y)) / 100);
            ball.x = canvas.width - paddleWidth - ball.radius - 0.1;
        }
        if (ball.x + ball.radius > canvas.width - paddleWidth && ball.y > rightPaddle2.y && ball.y < rightPaddle2.y + paddleHeight) {
            ball.dx *= -1;
            ball.dy += (1 - (50 - (rightPaddle2.y - ball.y)) / 100);
            ball.x = canvas.width - paddleWidth - ball.radius - 0.1;
        }
    }

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
        winner = "¡Equipo de la izquierda ha ganado!";
    } else if (rightScore >= maxScore) {
        gameOver = true;
        winner = "¡Equipo de la derecha ha ganado!";
    }
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

    let angle;
    do {
        angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
    } while (Math.abs(Math.cos(angle)) > 0.99);

    let directionX = Math.random() < 0.5 ? 1 : -1;
    let directionY = Math.random() < 0.5 ? 1 : -1;

    ball.dx = directionX * ball.speed * Math.cos(angle);
    ball.dy = directionY * ball.speed * Math.sin(angle);
}

function resetGame() {
    leftScore = 0;
    rightScore = 0;
    gameOver = false;
    winner = "";
    isPaused = false;
    leftPaddle.y = (canvas.height - paddleHeight) / 4;
    leftPaddle2.y = (canvas.height - paddleHeight) / 1.5;
    rightPaddle.y = (canvas.height - paddleHeight) / 4;
    rightPaddle2.y = (canvas.height - paddleHeight) / 1.5;
    resetBall();
    gameLoop();
}

function draw() {
	ctx.clearRect(0, 0, canvas.width, canvas.height);

	if (!gameOver) {
		ctx.fillStyle = leftPaddle.color;
		ctx.fillRect(0, leftPaddle.y, paddleWidth, paddleHeight);
		ctx.fillStyle = leftPaddle2.color;
		ctx.fillRect(0, leftPaddle2.y, paddleWidth, paddleHeight);
		ctx.fillStyle = rightPaddle.color;
		ctx.fillRect(canvas.width - paddleWidth, rightPaddle.y, paddleWidth, paddleHeight);
		ctx.fillStyle = rightPaddle2.color;
		ctx.fillRect(canvas.width - paddleWidth, rightPaddle2.y, paddleWidth, paddleHeight);
        
        ctx.fillStyle = "white";
		ctx.beginPath();
		ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
		ctx.fill();
		ctx.closePath();
        
		ctx.font = "30px Arial";
		ctx.fillText(leftScore, canvas.width * 0.25, 50);
		ctx.fillText(rightScore, canvas.width * 0.75, 50);
	}
}

function gameLoop() {
	update();
	draw();
	if (!gameOver)
		requestAnimationFrame(gameLoop);
}

gameLoop();