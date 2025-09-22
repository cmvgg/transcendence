window.onload = async function () {
    await fetchPlayersForGame("tron");
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
let playerUsernames = [];
let playerAvatars = [];

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
        logMessage(typeof arg === 'object' ? JSON.stringify(arg) : arg);
    });
} */

/********************
 * 2. Conection API *
 ********************/

function updatePlayerNames(playerUsernames, playerAvatars) {
    const player1NameElement = document.querySelector("#player1Name");
    const player1Avatar = document.querySelector('#player1Avatar');
    const player2NameElement = document.querySelector("#player2Name");
    const player2Avatar = document.querySelector('#player2Avatar');

    if (playerUsernames.length >= 2) {
        player1NameElement.textContent = playerUsernames[0] || "Player 1";
        player2NameElement.textContent = playerUsernames[1] || "Player 2";

        player1Avatar.src = playerAvatars[0];
        player2Avatar.src = playerAvatars[1];
    } else {
        player1NameElement.textContent = "Waiting...";
        player2NameElement.textContent = "Waiting...";

        player1Avatar.src = "https://bootdey.com/img/Content/avatar/avatar3.png";
        player2Avatar.src = "https://bootdey.com/img/Content/avatar/avatar3.png";
    }
}   
    
async function fetchPlayersForGame(mode = "tron") {
    const response = await fetch(`/get_players_for_game?game_type=${mode}`);
    const data = await response.json();
    
    if (response.ok) {
        const defaultAvatar = "https://bootdey.com/img/Content/avatar/avatar3.png";
        playerUsernames = data.players.map(p => p.username);
        playerAvatars = data.players.map(p => {
            if (p.avatar && p.avatar.trim() !== "") {
                return `/media/${p.avatar}`;
            } else {
                return defaultAvatar;
            }
        });
        updatePlayerNames(playerUsernames, playerAvatars);
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

/***********
 * 3. Game *
 ***********/

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
    if (e.key.toLowerCase() === "p") {
        isPaused = !isPaused;
    }
});

function showGameOverPopup() {
    document.getElementById("winnerText").innerText = winner;
    document.getElementById("gameOverModal").style.display = "flex";
}
document.getElementById("goHome").addEventListener("click", function () {
    window.location.href = "/select";
});

function checkCollision(player) {
    if (player.x < 0 || player.x >= canvas.width || player.y < 0 || player.y >= canvas.height) {
        gameOver = true;
        winner = player === player1 ? playerUsernames[1] : playerUsernames[0];
        updateStatsOnGameOver();
        return true;
    }

    for (let i = 0; i < player.trail.length - 1; i++) {
        if (player.x === player.trail[i].x && player.y === player.trail[i].y) {
            gameOver = true;
            winner = player === player1 ? playerUsernames[1] : playerUsernames[0];
            updateStatsOnGameOver();
            return true;
        }
    }

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

async function updateStatsOnGameOver() {
    if (playerUsernames.length < 2) return;

    if (winner === playerUsernames[0]) {
        await updateUserProfile(playerUsernames[0], 1, 0);
        await updateUserProfile(playerUsernames[1], 0, 1);
        await syncTronStats();
    } else {
        await updateUserProfile(playerUsernames[1], 1, 0);
        await updateUserProfile(playerUsernames[0], 0, 1);
        await syncTronStats();
    }
}

async function updateUserProfile(username, wins, losses) {
    const response = await fetch('/update_user_profile/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ username, wins, losses })
    });
    const data = await response.json();
}

async function syncTronStats() {
    const response = await fetch('/sync_tron_stats/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    });
    const data = await response.json();
}

function update() {
    if (isPaused || gameOver) {
        return;
    }

    player1.x += player1.dx;
    player1.y += player1.dy;
    player2.x += player2.dx;
    player2.y += player2.dy;

    player1.trail.push({ x: player1.x, y: player1.y });
    player2.trail.push({ x: player2.x, y: player2.y });

    checkCollision(player1);
    checkCollision(player2);
}

function draw() {
    if (!gameOver) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

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

    ctx.fillStyle = player1.color;
    ctx.fillRect(player1.x, player1.y, 3, 3);
    ctx.fillStyle = player2.color;
    ctx.fillRect(player2.x, player2.y, 3, 3);

    if (gameOver) {
        showGameOverPopup();
    }
}

function gameLoop() {
    update();
    draw();
    if (!gameOver) {
        requestAnimationFrame(gameLoop);
    }
}
