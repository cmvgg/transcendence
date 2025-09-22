window.onload = async function () {
    await fetchPlayersForGame("1vs1");
    resetBall();
    gameLoop();
};

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 3;
const paddleHeight = 30;
const borderHeight = 5;

let leftPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0, color: "white" };
let rightPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0, color: "white" };

let ball = { x: 0, y: 0, dx: 0, dy: 0, radius: 3, speed: 2 };
let leftScore = 0;
let rightScore = 0;
let maxScore = 5;
let gameOver = false;
let isPaused = true;
let winner = "";
let playerUsernames = [];
let playerAvatars = [];
const defaultAvatar = "https://bootdey.com/img/Content/avatar/avatar3.png";

/**************************
 * 2. console.log to HTML *
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

        player1Avatar.src = defaultAvatar;
        player2Avatar.src = defaultAvatar;
    }
}   
    
async function fetchPlayersForGame(mode = "1vs1") {
    const response = await fetch(`/get_players_for_game?game_type=${mode}`);
    const data = await response.json();
    if (response.ok) {
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

document.addEventListener("keydown", (e) => {
    if (e.key === "w")
        leftPaddle.dy = -5;
    if (e.key === "s")
        leftPaddle.dy = 5;
    if (e.key === "ArrowUp")
        rightPaddle.dy = -5;
    if (e.key === "ArrowDown")
        rightPaddle.dy = 5;
    if (e.key.toLowerCase() === "p")
        isPaused = !isPaused;
});
document.addEventListener("keyup", (e) => {
    if (["w", "s"].includes(e.key)) leftPaddle.dy = 0;
    if (["ArrowUp", "ArrowDown"].includes(e.key)) rightPaddle.dy = 0;
});
function showGameOverPopup() {
    document.getElementById("winnerText").innerText = winner;
    document.getElementById("gameOverModal").style.display = "flex";
}
document.getElementById("goHome").addEventListener("click", function () {
    window.location.href = "/select";
});

function update() {
    if (gameOver || isPaused)
        return;

    ball.x += ball.dx;
    ball.y += ball.dy;

    leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle.y + leftPaddle.dy));
    rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle.y + rightPaddle.dy));

    if (ball.y - ball.radius < borderHeight || ball.y + ball.radius > canvas.height - borderHeight)
        ball.dy *= -1;

    if (ball.dx < 0 && ball.x - ball.radius < paddleWidth && ball.y > leftPaddle.y && ball.y < leftPaddle.y + paddleHeight)
        ball.dx *= -1;
    if (ball.dx > 0 && ball.x + ball.radius > canvas.width - paddleWidth && ball.y > rightPaddle.y && ball.y < rightPaddle.y + paddleHeight)
        ball.dx *= -1;

    if (ball.x - ball.radius < 0) {
        rightScore++;
        checkGameOver();
    } else if (ball.x + ball.radius > canvas.width) {
        leftScore++;
        checkGameOver();
    }
}

async function checkGameOver() {
    if (playerUsernames.length < 2) {
        return;
    }

    if (leftScore >= maxScore) {
        gameOver = true;
        winner = playerUsernames[0];
        await updateUserProfile(playerUsernames[0], 1, 0, leftScore);
        await updateUserProfile(playerUsernames[1], 0, 1, rightScore);
        await sync1vs1Stats();
    } else if (rightScore >= maxScore) {
        gameOver = true;
        winner = playerUsernames[1];
        await updateUserProfile(playerUsernames[1], 1, 0, rightScore);
        await updateUserProfile(playerUsernames[0], 0, 1, leftScore);
        await sync1vs1Stats();
    } else {
        resetBall();
    }
    if (gameOver == true) {
        showGameOverPopup();
    }
}

async function sync1vs1Stats() {
    const response = await fetch('/sync_1vs1_stats/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    });
    const data = await response.json();
}

function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    let angle;
    do {
        angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
    } while (Math.abs(Math.cos(angle)) > 0.99);

    const dirX = Math.random() < 0.5 ? 1 : -1;
    const dirY = Math.random() < 0.5 ? 1 : -1;

    ball.dx = dirX * ball.speed * Math.cos(angle);
    ball.dy = dirY * ball.speed * Math.sin(angle);
}

function draw() {
    ctx.fillStyle = "white";
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillRect(0, leftPaddle.y, paddleWidth, paddleHeight);
    ctx.fillRect(canvas.width - paddleWidth, rightPaddle.y, paddleWidth, paddleHeight);

    ctx.font = "20px monospace";
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

function gameLoop() {
    update();
    draw();
    if (!gameOver) requestAnimationFrame(gameLoop);
}

async function updateUserProfile(username, wins, losses, score) {
    const response = await fetch('/update_user_profile/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ username, wins, losses, score })
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