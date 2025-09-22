window.onload = async function () {
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    await fetchPlayersForGame("battleground");
    gameLoop();

    /***********
     * Variables
     ***********/
    window.gameCanvas = canvas;
    window.ctx = ctx;
};

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.height = 500;
canvas.width = 500;

const paddleLength = 80;
const paddleThickness = 7;

let ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    dx: 2,
    dy: 2,
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
    const players = [
        { nameEl: "#player1Name", avatarEl: "#player1Avatar" },
        { nameEl: "#player2Name", avatarEl: "#player2Avatar" },
        { nameEl: "#player3Name", avatarEl: "#player3Avatar" },
        { nameEl: "#player4Name", avatarEl: "#player4Avatar" },
    ];

    players.forEach((p, i) => {
        const nameEl = document.querySelector(p.nameEl);
        const avatarEl = document.querySelector(p.avatarEl);
        if (playerUsernames[i]) {
            nameEl.textContent = playerUsernames[i];
            avatarEl.src = playerAvatars[i];
        } else {
            nameEl.textContent = "Waiting...";
            avatarEl.src = "https://bootdey.com/img/Content/avatar/avatar3.png";
        }
    });
}

async function fetchPlayersForGame(mode = "battleground") {
    const response = await fetch(`/get_players_for_game/?game_type=${mode}`);
    const data = await response.json();
    if (data.players && data.players.length > 0) {
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

async function syncBattlegroundStats() {
    const response = await fetch('/sync_tournament_stats/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    });

    const data = await response.json();
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

function showGameOverPopup() {
    document.getElementById("winnerText").innerText = winner;
    document.getElementById("gameOverModal").style.display = "flex";
}
document.getElementById("goHome").addEventListener("click", function () {
    window.location.href = "/select";
});

function update() {
    if (isPaused || gameOver) return;

    leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleLength, leftPaddle.y + leftPaddle.dy));
    rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleLength, rightPaddle.y + rightPaddle.dy));
    topPaddle.x = Math.max(0, Math.min(canvas.width - paddleLength, topPaddle.x + topPaddle.dx));
    bottomPaddle.x = Math.max(0, Math.min(canvas.width - paddleLength, bottomPaddle.x + bottomPaddle.dx));

    ball.x += ball.dx;
    ball.y += ball.dy;

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
        updateScoreDisplay();
        checkGameOver();
    }
    resetBall();
}

function updateScoreDisplay() {
    document.getElementById("player1-score").innerText = `Player 1: ${scores.left}`;
    document.getElementById("player2-score").innerText = `Player 2: ${scores.top}`;
    document.getElementById("player3-score").innerText = `Player 3: ${scores.right}`;
    document.getElementById("player4-score").innerText = `Player 4: ${scores.bottom}`;
}

function checkGameOver() {
    const maxScore = 3;
    for (const [player, score] of Object.entries(scores)) {
        if (score >= maxScore) {
            gameOver = true;
            winner = playerUsernames[player === "left" ? 0 : player === "right" ? 1 : player === "top" ? 2 : 3];
            updateStatsOnGameOver();
            showGameOverPopup();
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

    ctx.fillStyle = leftPaddle.color;
    ctx.fillRect(0, leftPaddle.y, paddleThickness, paddleLength);
    ctx.fillStyle = rightPaddle.color;
    ctx.fillRect(canvas.width - paddleThickness, rightPaddle.y, paddleThickness, paddleLength);
    ctx.fillStyle = topPaddle.color;
    ctx.fillRect(topPaddle.x, 0, paddleLength, paddleThickness);
    ctx.fillStyle = bottomPaddle.color;
    ctx.fillRect(bottomPaddle.x, canvas.height - paddleThickness, paddleLength, paddleThickness);
    
    ctx.fillStyle = "white";

    if (isPaused) {
        ctx.font = "40px Courier New";
        ctx.fillText("PAUSED", canvas.width / 2 - 70, canvas.height / 2);
    }
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.closePath();
}


async function gameLoop() {
    await update();
    draw();
    if (!gameOver) requestAnimationFrame(gameLoop);
}

