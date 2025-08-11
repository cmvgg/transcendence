const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleLength = 30;
const paddleThickness = 3;

let ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    dx: 4,
    dy: 3,
    radius: 3,
    speed: 2
};

let leftPaddle = { y: (canvas.height - paddleLength) / 2, dy: 0, color: "blue" };
let rightPaddle = { y: (canvas.height - paddleLength) / 2, dy: 0, color: "red" };
let topPaddle = { x: (canvas.width - paddleLength) / 2, dx: 0, color: "green" };
let bottomPaddle = { x: (canvas.width - paddleLength) / 2, dx: 0, color: "yellow" };

let scores = {
    left: 0,
    right: 0,
    top: 0,
    bottom: 0
};

let lastTouched = null;
let isPaused = false;

document.addEventListener("keydown", (e) => {
    if (e.key === "w")
        leftPaddle.dy = -5;
    if (e.key === "s")
        leftPaddle.dy = 5;
    if (e.key === "ArrowUp")
        rightPaddle.dy = -5;
    if (e.key === "ArrowDown")
        rightPaddle.dy = 5;
    if (e.key === "a")
        topPaddle.dx = -5;
    if (e.key === "d")
        topPaddle.dx = 5;
    if (e.key === "j")
        bottomPaddle.dx = -5;
    if (e.key === "l")
        bottomPaddle.dx = 5;
    if (e.key === "p" || e.key === "P")
        isPaused = !isPaused;
});

document.addEventListener("keyup", (e) => {
    if (["w", "s"].includes(e.key))
        leftPaddle.dy = 0;
    if (["ArrowUp", "ArrowDown"].includes(e.key))
        rightPaddle.dy = 0;
    if (["a", "d"].includes(e.key))
        topPaddle.dx = 0;
    if (["j", "l"].includes(e.key))
        bottomPaddle.dx = 0;
});

function update() {
    if (isPaused) return;

    // Movimiento paletas
    leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleLength, leftPaddle.y + leftPaddle.dy));
    rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleLength, rightPaddle.y + rightPaddle.dy));
    topPaddle.x = Math.max(0, Math.min(canvas.width - paddleLength, topPaddle.x + topPaddle.dx));
    bottomPaddle.x = Math.max(0, Math.min(canvas.width - paddleLength, bottomPaddle.x + bottomPaddle.dx));

    // Movimiento bola
    ball.x += ball.dx;
    ball.y += ball.dy;

    // Colisión con paletas verticales
    if (ball.dx < 0 && ball.x - ball.radius <= paddleThickness) {
        if (ball.y > leftPaddle.y && ball.y < leftPaddle.y + paddleLength) {
            ball.dx *= -1;
            lastTouched = "left";
        }
    }

    if (ball.dx > 0 && ball.x + ball.radius >= canvas.width - paddleThickness) {
        if (ball.y > rightPaddle.y && ball.y < rightPaddle.y + paddleLength) {
            ball.dx *= -1;
            lastTouched = "right";
        }
    }

    // Colisión con paletas horizontales
    if (ball.dy < 0 && ball.y - ball.radius <= paddleThickness) {
        if (ball.x > topPaddle.x && ball.x < topPaddle.x + paddleLength) {
            ball.dy *= -1;
            lastTouched = "top";
        }
    }

    if (ball.dy > 0 && ball.y + ball.radius >= canvas.height - paddleThickness) {
        if (ball.x > bottomPaddle.x && ball.x < bottomPaddle.x + paddleLength) {
            ball.dy *= -1;
            lastTouched = "bottom";
        }
    }

    // Goles
    if (ball.x - ball.radius < 0) {
        score("left");
    } else if (ball.x + ball.radius > canvas.width) {
        score("right");
    } else if (ball.y - ball.radius < 0) {
        score("top");
    } else if (ball.y + ball.radius > canvas.height) {
        score("bottom");
    }
}

function score(sideMissed) {
    if (lastTouched && lastTouched !== sideMissed) {
        scores[lastTouched]++;
    }
    resetBall();
}

function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.speed = 2;

    let angle;
    do {
        angle = Math.random() * 2 * Math.PI;
    } while (Math.abs(Math.cos(angle)) < 0.2 || Math.abs(Math.sin(angle)) < 0.2);

    ball.dx = ball.speed * Math.cos(angle);
    ball.dy = ball.speed * Math.sin(angle);
    lastTouched = null;
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Paletas
    ctx.fillStyle = leftPaddle.color;
    ctx.fillRect(0, leftPaddle.y, paddleThickness, paddleLength);

    ctx.fillStyle = rightPaddle.color;
    ctx.fillRect(canvas.width - paddleThickness, rightPaddle.y, paddleThickness, paddleLength);

    ctx.fillStyle = topPaddle.color;
    ctx.fillRect(topPaddle.x, 0, paddleLength, paddleThickness);

    ctx.fillStyle = bottomPaddle.color;
    ctx.fillRect(bottomPaddle.x, canvas.height - paddleThickness, paddleLength, 3);

    // Bola
    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.closePath();

    // Puntajes
    /* ctx.fillStyle = "white";
    ctx.font = "10px Arial";
    ctx.fillText(`Izquierda (Azul): ${scores.left}`, 30, 20);
    ctx.fillText(`Derecha (Rojo): ${scores.right}`, canvas.width / 2 + 20, 20);
    ctx.fillText(`Arriba (Verde): ${scores.top}`, canvas.width / 2 + 20, canvas.height - 10);
    ctx.fillText(`Abajo (Amarillo): ${scores.bottom}`, canvas.width / 2 - 100, canvas.height - 10); */
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

resetBall();
gameLoop();


