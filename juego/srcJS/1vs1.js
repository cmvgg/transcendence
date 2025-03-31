const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 10;
const paddleHeight = 100;
const borderHeight = 10;
const maxSpeed = 8;

let ball = {x: canvas.width / 2, y: canvas.height / 2, dx: 4, dy: 4, radius: 7, speed: 4};
let leftPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0, color: "blue" };
let rightPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0, color: "blue" };
let leftScore = 0;
let rightScore = 0;
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
        leftPaddle.dy = -5;
    if (e.key === "s")
        leftPaddle.dy = 5;
    if (e.key === "ArrowUp")
        rightPaddle.dy = -5;
    if (e.key === "ArrowDown")
        rightPaddle.dy = 5;
    if (e.key === "p" || e.key === "P")
        isPaused = !isPaused
});
document.addEventListener("keyup", (e) => {
    if (e.key === "w" || e.key === "s")
        leftPaddle.dy = 0;
    if (e.key === "ArrowUp" || e.key === "ArrowDown")
        rightPaddle.dy = 0;
});

//Lógica de juego
function update() {
    let prevBallX = ball.x;
    let prevBallY = ball.y;

    if (gameOver || isPaused)
        return ;

    //Mover paletas
    leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle.y + leftPaddle.dy));
    rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle.y + rightPaddle.dy));

    //Mover la pelota
    ball.x += ball.dx;
    ball.y += ball.dy;

    //Rebote en los bordes
    if (ball.y - ball.radius < borderHeight || ball.y + ball.radius > canvas.height - borderHeight)
        ball.dy *= -1; 

    //Rebote en las paletas
    /* if (ball.x - ball.radius < paddleWidth && ball.y > leftPaddle.y && ball.y < leftPaddle.y + paddleHeight)
        ball.dx *= -1;
    if (ball.x + ball.radius > canvas.width - paddleWidth && ball.y > rightPaddle.y && ball.y < rightPaddle.y + paddleHeight)
        ball.dx *= -1; */

    //Rebote en las paletas con efecto spin
    if(ball.dx < 0) {
        if (ball.x - ball.radius < paddleWidth && ball.y > leftPaddle.y && ball.y < leftPaddle.y + paddleHeight) {
        //if (prevBallX + ball.radius > paddleWidth && ball.x - ball.radius <= paddleWidth && ball.y + ball.radius > leftPaddle.y && ball.y - ball.radius < leftPaddle.y + paddleHeight) {    
            ball.dx *= -1;
            ball.dx = ball.dx + (1 - (50 - ball.y) / 100);
            ball.dx *= (ball.dx < 0 ? -1 : 1) * 0.5; 
            ball.x = paddleWidth + ball.radius + 0.1;
        }
    }
    if (ball.dx > 0) { 
        if (ball.x + ball.radius > canvas.width - paddleWidth && ball.y > rightPaddle.y && ball.y < rightPaddle.y + paddleHeight) {
        //if (prevBallX - ball.radius < canvas.width - paddleWidth && ball.x + ball.radius >= canvas.width - paddleWidth &&
        //    ball.y + ball.radius > rightPaddle.y && ball.y - ball.radius < rightPaddle.y + paddleHeight) {
            ball.dx *= -1;
            ball.dx = ball.dx + -(1 - (50 - ball.y) / 100);
            ball.dx *= (ball.dx < 0 ? 1 : -1) * 0.5; 
            ball.x = canvas.width - paddleWidth - ball.radius - 0.1;
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
        winner = "¡Jugador de la izquierda ha ganado!";
    } else if (rightScore >= maxScore) {
        gameOver = true;
        winner = "¡Jugador de la derecha ha ganado!";
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
    if (Math.random() > 0.5) {
        ball.dx = ball.speed * 1;
    } else {
        ball.dx = ball.speed * -1;
    }
    /* if (Math.random() > 0.5) {
        ball.dy = 4 * ball.speed * 1;
    } else {
        ball.dy = 4 * ball.speed * -1;
    } */
}

function resetGame() {
    leftScore = 0;
    rightScore = 0;
    gameOver = false;
    winner = "";
    isPaused = false;
    //Resetear paletas
    leftPaddle.y = (canvas.height - paddleHeight) / 2;
    rightPaddle.y = (canvas.height - paddleHeight) / 2;
    resetBall();
    gameLoop();
}

//Dibujar juego
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    //ctx.fillStyle = "white";
    let min = 0;
    let max = 600;
    let random = Math.floor(Math.random() * (max - min + 3)) + min;

    if (!gameOver) {
        ctx.fillRect(0, leftPaddle.y, paddleWidth, paddleHeight);
        ctx.fillRect(canvas.width - paddleWidth, rightPaddle.y, paddleWidth, paddleHeight);
        
        ctx.font = "60px Courier New";
        ctx.fillText(leftScore, canvas.width / 3, 60);
        ctx.fillText(rightScore, (canvas.width / 4) * 2.5, 60);
        //ctx.fillStyle = ballColor2;

        if (isPaused) {
            ctx.font = "30px Courier New";
            ctx.fillText("PAUSED", canvas.width / 2 - 60, canvas.height / 2);
        }
        
        const currentSpeed = ball.dx;
        const minSpeed = 4; 
        const maxSpeedForColor = 18; 
        const normalizedSpeed = Math.min(1, Math.max(0, (currentSpeed - minSpeed) / (maxSpeedForColor - minSpeed)));
        /* const hue = random - (normalizedSpeed);
        const ballColor = `hsl(${hue}, 100%, 50%)`; */
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
        //ctx.fillStyle = ballColor;
        ctx.fill();
        /* const minSpeed2 = 50; 
        const normalizedSpeed2 = Math.min(1, Math.max(0, (currentSpeed - minSpeed2) / (maxSpeedForColor - minSpeed)));
        const hue2 = random + 1 - (normalizedSpeed2);
        const ballColor2 = `hsl(${hue2}, 100%, 50%)`;*/
    }
}

function gameLoop() {
    update();
    draw();
    if (!gameOver) {
        requestAnimationFrame(gameLoop);
    }
}

gameLoop();
