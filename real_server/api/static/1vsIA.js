window.onload = async function () {

/**************************
 * 1. console.log to HTML *
 **************************/
/* function logMessage(message) {
    const logDiv = document.getElementById("log");
    const p = document.createElement("p");
    p.innerHTML = message.replace(/\n/g, "<br>");
    logDiv.appendChild(p);
    logDiv.scrollTop = logDiv.scrollHeight;
}

const originalConsoleLog = console.log;
function log(...args) {
    originalConsoleLog(...args);
    args.forEach(arg => {
        logMessage(typeof arg === "object" ? JSON.stringify(arg) : arg);
    });
} */

/*****************
 * Conection API *
 *****************/
let playerUsername = "";

async function fetchPlayer() {
    try {
        const response = await fetch("/get_players_for_game?game_type=1vsIA");
        const data = await response.json();
        if (response.ok && data.players && data.players.length > 0) {
            playerUsername = data.players[0].username;
        } else {
            throw new Error(data.error || "No se pudo obtener jugador.");
        }
    } catch (error) {
        throw error;
    }
}

async function updateUserProfile(username, wins, losses) {
    const response = await fetch("/update_user_profile/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ username, wins, losses }),
    });

    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || "Error al actualizar perfil.");
    }
}

async function sync1vsIAStats() {
    const response = await fetch("/sync_1vsIA_stats/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
    });

    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || "Error al sincronizar estadísticas.");
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showGameOverPopup() {
    document.getElementById("winnerText").innerText = winner;
    document.getElementById("gameOverModal").style.display = "flex";
}
document.getElementById("goHome").addEventListener("click", function () {
    window.location.href = "/select";
});

async function checkGameOver() {
    if (leftScore >= maxScore) {
        gameOver = true;
        winner = "¡You have won!";
        await updateUserProfile(playerUsername, 1, 0);
        await sync1vsIAStats();
    } else if (rightScore >= maxScore) {
        gameOver = true;
        winner = "The IA has won...";
        await updateUserProfile(playerUsername, 0, 1);
        await sync1vsIAStats();
    }

    if (gameOver) {
        //alert(winner);
        showGameOverPopup();
    } else {
        resetBall();
    }
}

await fetchPlayer();

/********
 * Game *
 ********/
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 3;
const paddleHeight = 30;
const borderHeight = 5;
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
let leftPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0, color: "white" };
let rightPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0, color: "white" };
let leftScore = 0;
let rightScore = 0;
let maxScore = 5;
let gameOver = false;
let isPaused = true;
let winner = "";
const AI_CONFIG = {
    speed: 3, reactionThreshold: 10, difficultyLevel: 'medium',
    difficulties: {
        easy: {/*  speedMultiplier: 0.1,  */reactionThreshold: 20 },
        medium: {/*  speedMultiplier: 0.3,  */reactionThreshold: 15 },
        hard: {/*  speedMultiplier: 0.7,  */reactionThreshold: 10 }
    }
};
const DIFFICULTY_SETTINGS = {
    easy: { initialSpeed: 1.5, maxSpeed: 4, growth: 1.002 },
    medium: { initialSpeed: 2.0, maxSpeed: 6, growth: 1.003 },
    hard: { initialSpeed: 2.5, maxSpeed: 8, growth: 1.004 }
};
let currentSettings = DIFFICULTY_SETTINGS[AI_CONFIG.difficultyLevel];

const difficultySelect = document.getElementById('difficultySelect');
AI_CONFIG.difficultyLevel = difficultySelect.value;

document.addEventListener("keydown", (e) => {
    if (!isPaused) {
        if (e.key === "w")
            leftPaddle.dy = -5;
        if (e.key === "s")
            leftPaddle.dy = 5;
    }
});
document.addEventListener("keyup", (e) => {
    if (e.key === "w" || e.key === "s")
        leftPaddle.dy = 0;
    if (e.key === "p" || e.key === "P")
        isPaused = !isPaused;
});


difficultySelect.addEventListener('change', (e) => {
    AI_CONFIG.difficultyLevel  = e.target.value;
    updateAIDifficulty();
});

document.getElementById("pauseButton").addEventListener("click", () => isPaused = true);
document.getElementById("startButton").addEventListener("click", () => isPaused = false);

function updateAIDifficulty() {
    const difficulty = AI_CONFIG.difficulties[AI_CONFIG.difficultyLevel];
    AI_CONFIG.reactionThreshold = difficulty.reactionThreshold;
    rightPaddle.speed = AI_CONFIG.speed;

    currentSettings = DIFFICULTY_SETTINGS[AI_CONFIG.difficultyLevel];
    resetBall();
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
        if (center < targetY)
            rightPaddle.y += rightPaddle.speed;
        else
            rightPaddle.y -= rightPaddle.speed;
    }
}

function update() {
    if (gameOver || isPaused) return;

    leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle.y + leftPaddle.dy));
    moveAI();
    rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle.y));

    ball.x += ball.dx;
    ball.y += ball.dy;

    if (ball.y - ball.radius < borderHeight || ball.y + ball.radius > canvas.height - borderHeight)
        ball.dy *= -1;

    if (ball.dx < 0 && ball.x - ball.radius <= paddleWidth && ball.y > leftPaddle.y && ball.y < leftPaddle.y + paddleHeight) {
        ball.dx *= -1;
    }

    if (ball.dx > 0 && ball.x + ball.radius >= canvas.width - paddleWidth && ball.y > rightPaddle.y && ball.y < rightPaddle.y + paddleHeight) {
        ball.dx *= -1;
    }

    if (ball.x - ball.radius < 0) {
        rightScore++;
        checkGameOver();
    } else if (ball.x + ball.radius > canvas.width) {
        leftScore++;
        checkGameOver();
    }
}

function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.radius = 3;

    let angle;
    do {
        angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
    } while (Math.abs(Math.cos(angle)) > 0.99);

    let directionX = Math.random() < 0.5 ? 1 : -1;
    let directionY = Math.random() < 0.5 ? 1 : -1;

    ball.dx = directionX * currentSettings.initialSpeed * Math.cos(angle);
    ball.dy = directionY * currentSettings.initialSpeed * Math.sin(angle);
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
            ctx.fillText("PAUSED", canvas.width / 2 - 40, canvas.height / 2);
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