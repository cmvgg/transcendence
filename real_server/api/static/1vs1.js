window.onload = function() {
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

const paddleWidth = 3;
const paddleHeight = 30;
const borderHeight = 5;

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
    dx: directionX * 2 * Math.cos(angle), //Antes era un 4 en vez de un 2
    dy: directionY * 2 * Math.sin(angle),
    radius: 3, speed: 2
};
let leftScore = 0;
let rightScore = 0;
let maxScore = 5; //!
let colorEffect = false;
let gameOver = false;
let isPaused = true;
let winner = "";
/*
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
});*/
document.getElementById("pauseButton").addEventListener("click", () => {
    isPaused = true;
});
document.getElementById("startButton").addEventListener("click", () => {
    isPaused = false;
});

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
    if (e.key === "b" || e.key === "B")
        colorEffect = !colorEffect
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

    let extraSpeed = Math.sqrt(ball.dx ** 2 + ball.dy ** 2); //Cambiar veloccidad de la pelota al empez
    ball.dx *= (extraSpeed + 0.00001) / extraSpeed;
    ball.dy *= (extraSpeed + 0.00001) / extraSpeed;

    //Mover paletas
    leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle.y + leftPaddle.dy));
    rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle.y + rightPaddle.dy));

    //Mover la pelota
    ball.x += ball.dx;
    ball.y += ball.dy;

    if (ball.y - ball.radius < borderHeight || ball.y + ball.radius > canvas.height - borderHeight)
        ball.dy *= -1; 

    //Rebote en las paletas con efecto spin
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

function resetGame() {
    leftScore = 0;
    rightScore = 0;
    gameOver = false;
    winner = "";
    isPaused = false;
    leftPaddle.y = (canvas.height - paddleHeight) / 2;
    rightPaddle.y = (canvas.height - paddleHeight) / 2;
    resetBall();
    gameLoop();
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let min = 0;
    let max = 600;
    let random = Math.floor(Math.random() * (max - min + 3)) + min;
    const currentSpeed = Math.sqrt(Math.pow(ball.dx, 2) + ball.dy ** 2); //ball² === ball**2
    const minSpeed = 3; 
    const maxSpeedForColor = 18; 
    const normalizedSpeed = Math.min(1, Math.max(0, (currentSpeed - minSpeed) / (maxSpeedForColor - minSpeed)));
    
    ctx.strokeStyle = "white";
    ctx.lineWidth = 1;
    const segmentHeight = 5;
    const segmentGap = 4;
    const centerX = canvas.width / 2;

    for (let y = borderHeight; y < canvas.height - borderHeight; y += segmentHeight + segmentGap) {
        ctx.beginPath();
        ctx.moveTo(centerX, y);
        ctx.lineTo(centerX, y + segmentHeight);
        ctx.stroke();
    }

    if (!gameOver) {
        ctx.fillStyle = leftPaddle.color;
        ctx.fillRect(0, leftPaddle.y, paddleWidth, paddleHeight);
        ctx.fillStyle = rightPaddle.color;
        ctx.fillRect(canvas.width - paddleWidth, rightPaddle.y, paddleWidth, paddleHeight);
        
        ctx.fillStyle = "white";
        ctx.font = "20px FreeMono";
        ctx.fillText(leftScore, canvas.width / 3, 20);
        ctx.fillText(rightScore, (canvas.width / 4) * 2.5, 20);

        if (isPaused) {
            ctx.font = "20px DejaVu Sans Mono";
            ctx.fillText("PAUSED", canvas.width / 2 - 28, canvas.height / 2 - 20);
        }
        
        let ballColor = "white";
        if (colorEffect) {
            const hue = random - (normalizedSpeed * 360);
            ballColor = `hsl(${hue}, 100%, 50%)`;
            //ball.speed = 8;
        }

        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
        ctx.fillStyle = ballColor;
        ctx.fill();
    }
}

function gameLoop() {
    update();
    draw();
    if (!gameOver)
        requestAnimationFrame(gameLoop);
}

gameLoop();}