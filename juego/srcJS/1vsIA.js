const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 10;
const paddleHeight = 100;
const borderHeight = 10;
const paddleSpeed = 5;
const maxBallSpeed = 8;
const maxScore = 5;
//Configuracion para la IA
const AI_CONFIG = {
    speed: 3, reactionThreshold: 10, difficultyLevel: 'medium',
    difficulties: {
        easy: {speedMultiplier: 0.7, reactionThreshold: 15},
        medium: {speedMultiplier: 1.0, reactionThreshold: 10},
        hard: {speedMultiplier: 1.3, reactionThreshold: 5}
    }
};
let ball = {x: canvas.width / 2, y: canvas.height / 2, dx: 4, dy: 4, radius: 7, speed: 4, color: "blue"};
let leftPaddle = {y: (canvas.height - paddleHeight) / 2, dy: 0, color: "red", speed: paddleSpeed};
let rightPaddle = {y: (canvas.height - paddleHeight) / 2, speed: AI_CONFIG.speed, color: "blue"};
let leftScore = 0;
let rightScore = 0;
let gameOver = false;
let isPaused = false;
let winner = "";

//Dificultad de la IA
const difficultySelect = document.getElementById('difficultySelect');
AI_CONFIG.difficultyLevel = difficultySelect.value;

//Control de teclado
document.addEventListener("keydown", (e) => {
    if (!isPaused) {
        if (e.key === "w") leftPaddle.dy = -leftPaddle.speed;
        if (e.key === "s") leftPaddle.dy = leftPaddle.speed;
    }
});
document.addEventListener("keyup", (e) => {
    if (e.key === "w" || e.key === "s")
        leftPaddle.dy = 0;
});
document.addEventListener("keydown", (e) => {
    if (e.key === "p" || e.key === "P")
        isPaused = !isPaused;
});
//Boton de pausa
document.getElementById("pauseButton").addEventListener("click", () => {
    isPaused = !isPaused;
});
//Cambiar la dificultad de la IA
difficultySelect.addEventListener('change', (e) => {
    AI_CONFIG.difficultyLevel = e.target.value;
    updateAIDifficulty();
});

function updateAIDifficulty() {
    const difficulty = AI_CONFIG.difficulties[AI_CONFIG.difficultyLevel];
    AI_CONFIG.reactionThreshold = difficulty.reactionThreshold;
    rightPaddle.speed = AI_CONFIG.speed * difficulty.speedMultiplier;
}
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

//Prediccion de la IA
function predictBallY() {
    if (ball.dx <= 0)
        return ball.y;

    let tempX = ball.x;
    let tempY = ball.y;
    let tempDx = ball.dx;
    let tempDy = ball.dy;

    while (tempX < canvas.width - paddleWidth) {
        tempX += tempDx;
        tempY += tempDy;

        if (tempY - ball.radius < borderHeight || tempY + ball.radius > canvas.height - borderHeight)
            tempDy *= -1;
    }
    return tempY;
}

function moveAI() {
    if (isPaused)
        return;
    let center = rightPaddle.y + paddleHeight / 2;
    let targetY = predictBallY();

    if (Math.abs(center - targetY) > AI_CONFIG.reactionThreshold) {
        if (center < targetY) {
            rightPaddle.y += rightPaddle.speed;
        } else {
            rightPaddle.y -= rightPaddle.speed;
        }
    }
}

function update() {
    let prevBallX = ball.x;
    let prevBallY = ball.y;
    
    if (gameOver || isPaused)
        return;

    //Mover paletas
    leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle.y + leftPaddle.dy));
    moveAI();
    rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle.y));

    //Mover la pelota
    ball.x += ball.dx;
    ball.y += ball.dy;

    //Rebote en los bordes
    if (ball.y - ball.radius < borderHeight || ball.y + ball.radius > canvas.height - borderHeight) {
        ball.dy *= -1;
    }

    //Rebote en las paletas
    if(ball.dx < 0) {
        if (prevBallX + ball.radius > paddleWidth && ball.x - ball.radius <= paddleWidth && ball.y + ball.radius > leftPaddle.y && ball.y - ball.radius < leftPaddle.y + paddleHeight) {    
            ball.dx *= -1;
            ball.dx = ball.dx + (1 - (50 - ball.y) / 100);
            ball.dx *= (ball.dx < 0 ? -0.8 : 0.8); 
        }
    }
    if (ball.dx > 0) { 
        if (prevBallX - ball.radius < canvas.width - paddleWidth && ball.x + ball.radius >= canvas.width - paddleWidth &&
            ball.y + ball.radius > rightPaddle.y && ball.y - ball.radius < rightPaddle.y + paddleHeight) {
            ball.dx *= -1;
            ball.dx = ball.dx + -(1 - (50 - ball.y) / 100);
            ball.dx *= (ball.dx < 0 ? 0.8 : -0.8); 
        }
    }

    //Verificar si la pelota toca los lados
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
        winner = "¡Has ganado!";
    } else if (rightScore >= maxScore) {
        gameOver = true;
        winner = "La IA ha ganado...";
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
    if (Math.random() > 0.5) {
        ball.dx = ball.speed * 1;
    } else {
        ball.dx = ball.speed * -1;
    }
    if (Math.random() > 0.5) {
        ball.dy = 4 * ball.speed * 1;
    } else {
        ball.dy = 4 * ball.speed * -1;
    }
}

function resetGame() {
    leftScore = 0;
    rightScore = 0;
    gameOver = false;
    winner = "";
    isPaused = false;
    updateAIDifficulty();
    leftPaddle = {y: (canvas.height - paddleHeight) / 2, dy: 0, speed: paddleSpeed};
    rightPaddle = {y: (canvas.height - paddleHeight) / 2, speed: AI_CONFIG.speed};
    resetBall();
    gameLoop();
}

//Dibujar juego
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white";
    let min = 0;
    let max = 600;
    let random = Math.floor(Math.random() * (max - min + 3)) + min;
    
    if (!gameOver) {
        ctx.fillRect(0, leftPaddle.y, paddleWidth, paddleHeight);
        ctx.fillRect(canvas.width - paddleWidth, rightPaddle.y, paddleWidth, paddleHeight);
        const currentSpeed = ball.dx;
        const minSpeed = 4; 
        const maxBallSpeedForColor = 18; 
        const normalizedSpeed = Math.min(1, Math.max(0, (currentSpeed - minSpeed) / (maxBallSpeedForColor - minSpeed)));
        const hue = random - (normalizedSpeed);
        const ballColor = `hsl(${hue}, 100%, 50%)`;
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
        ctx.fillStyle = ballColor
        ctx.fill();

        ctx.font = "60px Courier New";
        ctx.fillText(leftScore, canvas.width / 3, 60);
        ctx.fillText(rightScore, (canvas.width / 4) * 2.5, 60);

        if (isPaused) {
            ctx.font = "30px Courier New";
            ctx.fillText("PAUSED", canvas.width / 2 - 60, canvas.height / 2);
        }
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