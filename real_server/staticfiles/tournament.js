/**********************
 * 1. Tournament
 **********************/
class Tournament {
    constructor(players) {
        this.players = players.slice();
        this.matches = this.createBracket(this.players);
        this.currentRound = 0;
        this.currentMatchIndex = 0;
    }

    createBracket(players) {
        let matches = [];
        if (players.length % 2 !== 0) {
            players.push("BYE");
        }
        for (let i = 0; i < players.length; i += 2) {
            matches.push({
                player1: players[i],
                player2: players[i + 1],
                winner: null,
            });
        }
        return [matches];
    }

    getCurrentMatch() {
        const currentMatches = this.matches[this.currentRound];
        if (this.currentMatchIndex >= currentMatches.length) {
            return null;
        }
        return currentMatches[this.currentMatchIndex];
    }

    setWinner(winner) {
        const match = this.getCurrentMatch();
        if (!match) return;
        match.winner = winner;
        this.currentMatchIndex++;
        if (this.currentMatchIndex >= this.matches[this.currentRound].length) {
            this.generateNextRound();
        }
        renderBracket(this.matches);
    }

    generateNextRound() {
        const winners = this.matches[this.currentRound].map(match => match.winner).filter(winner => winner !== "BYE");

        if (winners.length === 1) {
            return;
        }
        let nextRoundMatches = [];
        if (winners.length % 2 !== 0) {
            winners.push("BYE");
        }
        for (let i = 0; i < winners.length; i += 2) {
            nextRoundMatches.push({
                player1: winners[i],
                player2: winners[i + 1],
                winner: null,
            });
        }
        this.matches.push(nextRoundMatches);
        this.currentRound++;
        this.currentMatchIndex = 0;
    }

    isTournamentOver() {
        const lastRound = this.matches[this.matches.length - 1];
        return lastRound.length === 1 && lastRound[0].winner !== null;
    }
}

/*********************************************
 * 2. Redirigir console.log al elemento HTML *
 *********************************************/
/*
function logMessage(message) {
    const logDiv = document.getElementById("log");
    const p = document.createElement("p");

    const safeMessage = typeof message === "string" ? message : JSON.stringify(message);

    p.innerHTML = safeMessage.replace(/\n/g, "<br>");
    logDiv.appendChild(p);
    logDiv.scrollTop = logDiv.scrollHeight;
}

const originalConsoleLog = console.log;
function log(...args) {
    originalConsoleLog(...args);
    args.forEach(arg => {
        logMessage(typeof arg === "object" ? JSON.stringify(arg) : arg);
    });
}
*/

/**********
 * 3. Game*
 **********/
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
    dx: (directionX * 2 * Math.cos(angle)),
    dy: (directionY * 2 * Math.sin(angle)),
    radius: 3, speed: 2
};
let leftPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0 };
let rightPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0 };
let leftScore = 0;
let rightScore = 0;
let maxScore = 5;
let gameOver = false;
let isPaused = true;
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
    if (e.key.toLowerCase() === "p")
        isPaused = !isPaused;
});

document.addEventListener("keyup", (e) => {
    if (e.key === "w" || e.key === "s")
        leftPaddle.dy = 0;
    if (e.key === "ArrowUp" || e.key === "ArrowDown")
        rightPaddle.dy = 0;
});

function showGameOverPopup(winnerName) {
    document.getElementById("winnerText").innerText = winnerName;
    document.getElementById("gameOverModal").style.display = "flex";
}
document.getElementById("goHome").addEventListener("click", function () {
    window.location.href = "/select";
});

function update() {
    if (gameOver || isPaused) return;

    const speedIncrease = 0.003;

    ball.speed += speedIncrease;

    const angle = Math.atan2(ball.dy, ball.dx);
    ball.dx = Math.cos(angle) * ball.speed;
    ball.dy = Math.sin(angle) * ball.speed;

    ball.x += ball.dx;
    ball.y += ball.dy;

    leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle.y + leftPaddle.dy));
    rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle.y + rightPaddle.dy));

    if (ball.y - ball.radius < borderHeight || ball.y + ball.radius > canvas.height - borderHeight) {
        ball.dy *= -1;
    }

    if (ball.x - ball.radius < paddleWidth && ball.y > leftPaddle.y && ball.y < leftPaddle.y + paddleHeight)
        ball.dx *= -1;
    if (ball.x + ball.radius > canvas.width - paddleWidth && ball.y > rightPaddle.y && ball.y < rightPaddle.y + paddleHeight)
        ball.dx *= -1;

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
        currentMatch.winner = currentMatch.player1;

        endMatch();
    } else if (rightScore >= maxScore) {
        gameOver = true;
        currentMatch.winner = currentMatch.player2;

        endMatch();
    } else {
        resetBall();
    }
}

function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.radius = 3;
    ball.speed = 2;

    let angle;
    do {
        angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
    } while (Math.abs(Math.cos(angle)) > 0.99);

    let directionX = Math.random() < 0.5 ? 1 : -1;
    let directionY = Math.random() < 0.5 ? 1 : -1;

    ball.dx = directionX * ball.speed * Math.cos(angle);
    ball.dy = directionY * ball.speed * Math.sin(angle);
}

function resetGameForNextMatch() {
    leftScore = 0;
    rightScore = 0;
    gameOver = false;
    isPaused = true;
    leftPaddle.y = (canvas.height - paddleHeight) / 2;
    rightPaddle.y = (canvas.height - paddleHeight) / 2;
    resetBall();
    currentMatch = tournament.getCurrentMatch();
    if (!currentMatch) {
        return;
    }

    updatePlayerNames(currentMatch, playerAvatarsMap);
    gameLoop();
}

function draw() {
    ctx.fillStyle = "white";
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillRect(0, leftPaddle.y, paddleWidth, paddleHeight);
    ctx.fillRect(canvas.width - paddleWidth, rightPaddle.y, paddleWidth, paddleHeight);
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();

    ctx.font = "20px Courier New";
    ctx.fillText(leftScore, canvas.width / 3, 20);
    ctx.fillText(rightScore, (canvas.width / 4) * 2.5, 20);

    if (isPaused) {
        ctx.font = "20px Courier New";
        ctx.fillText("PAUSED", canvas.width / 2 - 40, canvas.height / 2);
    }
}

function gameLoop() {
    update();
    draw();
    if (!gameOver) {
        requestAnimationFrame(gameLoop);
    }
}

/*********************
 * 6. Conection  API *
 *********************/
async function endMatch() {
    if (!currentMatch) return;

    const winnerName = currentMatch.winner;
    const loserName = currentMatch.player1 === winnerName ? currentMatch.player2 : currentMatch.player1;
    const isFinal = tournament.isTournamentOver();

    const response = await fetch('/submit_tournament_match/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ winner: winnerName, loser: loserName, is_final: isFinal })
    });

    const data = await response.json();

    tournament.setWinner(winnerName);
    if (!tournament.isTournamentOver()) {
        resetGameForNextMatch();
    }else {
        showGameOverPopup(winnerName);
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

/*************
 * 7. Render *
 *************/
function renderBracket(matchesByRound) {
    const bracketContainer = document.getElementById("bracket");
    bracketContainer.innerHTML = '';
    matchesByRound.forEach((round, roundIndex) => {
        const roundDiv = document.createElement("div");
        roundDiv.classList.add("round");
        round.forEach(match => {
            const matchDiv = document.createElement("div");
            matchDiv.classList.add("match");
            const p1 = document.createElement("div");
            p1.textContent = match.player1 || "BYE";
            if (match.winner === match.player1) p1.classList.add("winner");
            const p2 = document.createElement("div");
            p2.textContent = match.player2 || "BYE";
            if (match.winner === match.player2) p2.classList.add("winner");
            matchDiv.appendChild(p1);
            matchDiv.appendChild(p2);
            roundDiv.appendChild(matchDiv);
        });
        bracketContainer.appendChild(roundDiv);
    });
}

const defaultAvatar = "https://bootdey.com/img/Content/avatar/avatar3.png";
let playerAvatarsMap = {};  // Mapa global para acceder a los avatares

function updatePlayerNames(currentMatch, avatars = {}) {
    const player1NameElement = document.querySelector("#player1Name");
    const player1Avatar = document.querySelector("#player1Avatar");
    const player2NameElement = document.querySelector("#player2Name");
    const player2Avatar = document.querySelector("#player2Avatar");

    if (currentMatch) {
        player1NameElement.textContent = currentMatch.player1 || "BYE";
        player2NameElement.textContent = currentMatch.player2 || "BYE";

        player1Avatar.src = avatars[currentMatch.player1] || defaultAvatar;
        player2Avatar.src = avatars[currentMatch.player2] || defaultAvatar;
    } else {
        player1NameElement.textContent = "Waiting...";
        player2NameElement.textContent = "Waiting...";
        player1Avatar.src = defaultAvatar;
        player2Avatar.src = defaultAvatar;
    }
}

/*****************
 * 8. Tournament *
 *****************/
document.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch('/get_tournament_players/');
    const data = await response.json();
    if (!response.ok) {
        return;
    }

    const playerNames = data.players.map(p => p.username);

    // Crear el mapa de avatares
    playerAvatarsMap = {};
    data.players.forEach(p => {
        playerAvatarsMap[p.username] = (p.avatar && p.avatar.trim() !== "")
            ? `${p.avatar}`
            : defaultAvatar;
    });

    tournament = new Tournament(playerNames);
    currentMatch = tournament.getCurrentMatch();
    renderBracket(tournament.matches);
    if (currentMatch) {
        updatePlayerNames(currentMatch, playerAvatarsMap);
        resetGameForNextMatch();
    }
});
