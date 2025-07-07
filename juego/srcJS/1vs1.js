const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 10;
const paddleHeight = 100;
const borderHeight = 10;
const maxSpeed = 8;

let leftPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0, color: "black" };
let rightPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0, color: "black" };
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
let leftScore = 0;
let rightScore = 0;
let maxScore = 5;
let colorEffect = false;
let gameOver = false;
let isPaused = false;
let winner = "";

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

    let extraSpeed = Math.sqrt(ball.dx ** 2 + ball.dy ** 2);
    ball.dx *= (extraSpeed + 0.01) / extraSpeed;
    ball.dy *= (extraSpeed + 0.01) / extraSpeed;

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


    //TODO: Conectar a la API
    /* //Enviar datos al servidor
    if (gameOver) {

        fetch('http://localhost:5500/api/')
        .then(response => response.json())
        .then(data => console.log('Data sent successfully:', data))
        .catch(error => console.error('Error sending data:', error.message));

    } */
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
    const minSpeed = 4; 
    const maxSpeedForColor = 18; 
    const normalizedSpeed = Math.min(1, Math.max(0, (currentSpeed - minSpeed) / (maxSpeedForColor - minSpeed)));
    
    if (!gameOver) {
        ctx.fillStyle = leftPaddle.color;
        ctx.fillRect(0, leftPaddle.y, paddleWidth, paddleHeight);
        ctx.fillStyle = rightPaddle.color;
        ctx.fillRect(canvas.width - paddleWidth, rightPaddle.y, paddleWidth, paddleHeight);
        
        ctx.fillStyle = "white";
        ctx.font = "60px Courier New";
        ctx.fillText(leftScore, canvas.width / 3, 60);
        ctx.fillText(rightScore, (canvas.width / 4) * 2.5, 60);

        if (isPaused) {
            ctx.font = "30px Courier New";
            ctx.fillText("PAUSED", canvas.width / 2 - 60, canvas.height / 2);
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

gameLoop();

