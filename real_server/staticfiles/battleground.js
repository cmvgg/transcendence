const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.height = 500;
canvas.width = 500;

const paddleLength = 80;
const paddleThickness = 7;

let ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    dx: 4,
    dy: 3,
    radius: 8,
    speed: 2
};

let topPaddle = { x: (canvas.width - paddleLength) / 2, dx: 0, color: "green" };
let leftPaddle = { y: (canvas.height - paddleLength) / 2, dy: 0, color: "blue" };
let rightPaddle = { y: (canvas.height - paddleLength) / 2, dy: 0, color: "red" };
let bottomPaddle = { x: (canvas.width - paddleLength) / 2, dx: 0, color: "yellow" };

let scores = {
    left: 0,
    right: 0,
    top: 0,
    bottom: 0
};

let lastTouched = null;
let isPaused = true;
let gameOver = false;
let winner = "";
let playerUsernames = []; // Almacena los nombres de los jugadores obtenidos de la API

/*********************************************
 * 1. Redirigir console.log al elemento HTML *
 *********************************************/
function logMessage(message) {
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
        logMessage(typeof arg === 'object' ? JSON.stringify(arg) : arg);
    });
}

/**************************
 * 2. Conexión con la API *
 **************************/

// Obtener jugadores para el modo "battleground"
async function fetchPlayersForGame(mode = "battleground") {
    try {
        const response = await fetch(`/get_players_for_game/?game_type=${mode}`);
        const data = await response.json();
        if (data.players && data.players.length > 0) {
            playerUsernames = data.players.map(p => p.username);
            log("Jugadores cargados:", playerUsernames);
        } else {
            log("No se pudo obtener jugadores.");
        }
    } catch (error) {
        log("Error obteniendo jugadores:", error);
    }
}

// Sincronizar estadísticas al finalizar el juego
async function syncBattlegroundStats() {
    try {
        const response = await fetch('/sync_tournament_stats/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });

        const data = await response.json();
        if (!response.ok) {
            log("Error al sincronizar estadísticas de Battleground:", data.error);
        } else {
            log("Estadísticas de Battleground sincronizadas:", data.message);
        }
    } catch (error) {
        log("Error de conexión al sincronizar estadísticas de Battleground:", error.message);
    }
}

// Actualizar el perfil de un jugador
async function updateUserProfile(username, wins, losses) {
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
            log("Error:", data);
        } else {
            log("Stats actualizadas:", data);
        }
    } catch (error) {
        log("Error de conexión:", error.message);
    }
}

// Obtener el token CSRF
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

/***********************
 * 3. Lógica del juego *
 ***********************/

document.addEventListener("keydown", (e) => {
    if (e.key === "j")
        topPaddle.dx = -5;
    if (e.key === "k")
        topPaddle.dx = 5;
    if (e.key === "w")
        leftPaddle.dy = -5;
    if (e.key === "s")
        leftPaddle.dy = 5;
    if (e.key === "ArrowUp")
        rightPaddle.dy = -5;
    if (e.key === "ArrowDown")
        rightPaddle.dy = 5;
    if (e.key === "5")
        bottomPaddle.dx = -5;
    if (e.key === "6")
        bottomPaddle.dx = 5;
    if (e.key === "p" || e.key === "P")
        isPaused = !isPaused;
});

document.addEventListener("keyup", (e) => {
    if (["j", "k"].includes(e.key))
        topPaddle.dx = 0;
    if (["w", "s"].includes(e.key))
        leftPaddle.dy = 0;
    if (["ArrowUp", "ArrowDown"].includes(e.key))
        rightPaddle.dy = 0;
    if (["5", "6"].includes(e.key))
        bottomPaddle.dx = 0;
});

function update() {
    if (isPaused || gameOver) return;

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
        updateScoreDisplay(); // Llama a esta función para actualizar las puntuaciones en el HTML
        checkGameOver();
    }
    resetBall();
}

function updateScoreDisplay() {
    document.getElementById("player1-score").innerText = `Player 1: ${scores.left}`;
    document.getElementById("player2-score").innerText = `Player 2: ${scores.right}`;
    document.getElementById("player3-score").innerText = `Player 3: ${scores.top}`;
    document.getElementById("player4-score").innerText = `Player 4: ${scores.bottom}`;
}

function checkGameOver() {
    const maxScore = 3; // Cambia esto según las reglas del juego
    for (const [player, score] of Object.entries(scores)) {
        if (score >= maxScore) {
            gameOver = true;
            winner = playerUsernames[player === "left" ? 0 : player === "right" ? 1 : player === "top" ? 2 : 3];
            updateStatsOnGameOver();
            break;
        }
    }
}

async function updateStatsOnGameOver() {
    if (playerUsernames.length < 4) return;

    for (const [player, score] of Object.entries(scores)) {
        const username = playerUsernames[player === "left" ? 0 : player === "right" ? 1 : player === "top" ? 2 : 3];
        if (username === winner) {
            await updateUserProfile(username, 1, 0);
        } else {
            await updateUserProfile(username, 0, 1);
        }
    }

    log("Sincronizando estadísticas...");
    await syncBattlegroundStats();
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
    ctx.fillRect(bottomPaddle.x, canvas.height - paddleThickness, paddleLength, paddleThickness);

    // Bola
    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.closePath();
}

function gameLoop() {
    update();
    draw();
    if (!gameOver) requestAnimationFrame(gameLoop);
}

// Inicializar el juego
resetBall();
fetchPlayersForGame("battleground").then(() => {
    gameLoop();
});


