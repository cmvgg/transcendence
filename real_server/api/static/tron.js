window.onload = async function () {
    /* await fetchPlayersForGame("tron"); */
    gameLoop();
};

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let player1 = {
    x: 0,
    y: canvas.height / 2,
    dx: 1,
    dy: 0,
    color: "blue",
    trail: []
};
let player2 = {
    x: canvas.width - 5,
    y: canvas.height / 2,
    dx: -1,
    dy: 0,
    color: "red",
    trail: []
};
let gameOver = false;
let isPaused = true;
let winner = "";
let playerUsernames = []; // Almacena los nombres de los jugadores obtenidos de la API

/*********************************************
 * 1. Conexión con la API *
 *********************************************/

// Obtener jugadores para el modo "tron"
async function fetchPlayersForGame(mode = "tron") {
    try {
        const response = await fetch(`/get_players_for_game?game_type=${mode}`);
        const data = await response.json();
        if (response.ok) {
            playerUsernames = data.players.map(p => p.username);
            log("Jugadores asignados:", playerUsernames);
        } else {
            log("Error obteniendo jugadores:", data.error);
        }
    } catch (err) {
        log("Error en la conexión:", err.message);
    }
}

// Actualizar estadísticas de los jugadores
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

/*********************************************
 * 2. Lógica del juego *
 *********************************************/

document.addEventListener("keydown", (e) => {
    if (e.key === "w" && player1.dy === 0) {
        player1.dx = 0;
        player1.dy = -1;
    }
    if (e.key === "a" && player1.dx === 0) {
        player1.dx = -1;
        player1.dy = 0;
    }
    if (e.key === "d" && player1.dx === 0) {
        player1.dx = 1;
        player1.dy = 0;
    }
    if (e.key === "s" && player1.dy === 0) {
        player1.dx = 0;
        player1.dy = 1;
    }
    if (e.key === "ArrowUp" && player2.dy === 0) {
        player2.dx = 0;
        player2.dy = -1;
    }
    if (e.key === "ArrowLeft" && player2.dx === 0) {
        player2.dx = -1;
        player2.dy = 0;
    }
    if (e.key === "ArrowRight" && player2.dx === 0) {
        player2.dx = 1;
        player2.dy = 0;
    }
    if (e.key === "ArrowDown" && player2.dy === 0) {
        player2.dx = 0;
        player2.dy = 1;
    }
    if (e.key === "p" || e.key === "P")
        isPaused = !isPaused;
});

function checkCollision(player) {
    // Colisión con las paredes
    if (player.x < 0 || player.x >= canvas.width || player.y < 0 || player.y >= canvas.height) {
        gameOver = true;
        winner = player === player1 ? playerUsernames[1] : playerUsernames[0];
        updateStatsOnGameOver();
        return true;
    }

    // Colisión con su propia estela
    for (let i = 0; i < player.trail.length - 1; i++) {
        if (player.x === player.trail[i].x && player.y === player.trail[i].y) {
            gameOver = true;
            winner = player === player1 ? playerUsernames[1] : playerUsernames[0];
            updateStatsOnGameOver();
            return true;
        }
    }

    // Colisión con la estela del otro jugador
    let otherPlayer = player === player1 ? player2 : player1;
    for (let i = 0; i < otherPlayer.trail.length; i++) {
        if (player.x === otherPlayer.trail[i].x && player.y === otherPlayer.trail[i].y) {
            gameOver = true;
            winner = player === player1 ? playerUsernames[1] : playerUsernames[0];
            updateStatsOnGameOver();
            return true;
        }
    }

    return false;
}

function updateStatsOnGameOver() {
    if (playerUsernames.length < 2) return;

    if (winner === playerUsernames[0]) {
        updateUserProfile(playerUsernames[0], 1, 0);
        updateUserProfile(playerUsernames[1], 0, 1);
    } else {
        updateUserProfile(playerUsernames[1], 1, 0);
        updateUserProfile(playerUsernames[0], 0, 1);
    }
}

function update() {
    if (isPaused || gameOver) {
        return;
    }

    // Actualizar la posición de los jugadores
    player1.x += player1.dx;
    player1.y += player1.dy;
    player2.x += player2.dx;
    player2.y += player2.dy;

    // Agregar la posición actual a la estela
    player1.trail.push({ x: player1.x, y: player1.y });
    player2.trail.push({ x: player2.x, y: player2.y });

    checkCollision(player1);
    checkCollision(player2);
}

function draw() {
    if (!gameOver) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    // Dibujar trayectorias
    for (let i = 1; i < player1.trail.length; i++) {
        ctx.strokeStyle = player1.color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(player1.trail[i - 1].x + 1, player1.trail[i - 1].y + 1);
        ctx.lineTo(player1.trail[i].x + 1, player1.trail[i].y + 1);
        ctx.stroke();
    }
    for (let i = 1; i < player2.trail.length; i++) {
        ctx.strokeStyle = player2.color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(player2.trail[i - 1].x + 1, player2.trail[i - 1].y + 1);
        ctx.lineTo(player2.trail[i].x + 1, player2.trail[i].y + 1);
        ctx.stroke();
    }

    // Dibujar jugadores
    ctx.fillStyle = player1.color;
    ctx.fillRect(player1.x, player1.y, 3, 3);
    ctx.fillStyle = player2.color;
    ctx.fillRect(player2.x, player2.y, 3, 3);

    if (gameOver) {
        ctx.fillStyle = "black";
        ctx.font = "30px Arial";
        ctx.fillText(winner + " wins!", canvas.width / 2 - 100, canvas.height / 2);
    }
}

function gameLoop() {
    update();
    draw();
    if (!gameOver) {
        requestAnimationFrame(gameLoop);
    }
}
