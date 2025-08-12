/**********************
 * 1. Lógica del Torneo
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
        log(`Partido finalizado: ${match.player1} vs ${match.player2} - Ganador: ${winner}`);

        this.currentMatchIndex++;

        if (this.currentMatchIndex >= this.matches[this.currentRound].length) {
            this.generateNextRound();
        }
        renderBracket(this.matches); // Render actualizado del bracket
    }

    generateNextRound() {
        const winners = this.matches[this.currentRound].map(match => match.winner).filter(winner => winner !== "BYE");

        if (winners.length === 1) {
            log(`🏆 ¡El campeón del torneo es ${winners[0]}!`);
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
        log(`Iniciando ronda ${this.currentRound + 1}`);
    }

    isTournamentOver() {
        const lastRound = this.matches[this.matches.length - 1];
        return lastRound.length === 1 && lastRound[0].winner !== null;
    }
}

/*********************************************
 * 2. Redirigir console.log al elemento HTML *
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
        logMessage(typeof arg === "object" ? JSON.stringify(arg) : arg);
    });
}

/***********************
 * 3. Lógica del Juego *
 ***********************/
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 10;
const paddleHeight = 100;
const borderHeight = 10;
let angle;
do {
    angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
} while (Math.abs(Math.cos(angle)) > 0.99);
let directionX = Math.random() < 0.5 ? 1 : -1;
let directionY = Math.random() < 0.5 ? 1 : -1;
let ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    dx: (directionX * 4 * Math.cos(angle)),
    dy: (directionY * 4 * Math.sin(angle)),
    radius: 7, speed: 6
};
let leftPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0 };
let rightPaddle = { y: (canvas.height - paddleHeight) / 2, dy: 0 };
let leftScore = 0;
let rightScore = 0;
let maxScore = 5;
let gameOver = false;
let isPaused = false;
let winner = "";

/***********************
 * 4. Eventos y controles *
 ***********************/
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

/* document.getElementById("pauseButton").addEventListener("click", () => {
    isPaused = true;
});
document.getElementById("startButton").addEventListener("click", () => {
    isPaused = false;
}); */

/* document.getElementById("pauseButton").addEventListener("click", () => isPaused = true);
document.getElementById("startButton").addEventListener("click", () => isPaused = false); */

/* document.getElementById("goHome").addEventListener("click", () => {
    document.getElementById("goHome").disabled = true;
    window.location.href = "../templates/index";
}); */

/***********************
 * 5. Render y lógica de juego *
 ***********************/
function update() {
    if (gameOver || isPaused) return;

    leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle.y + leftPaddle.dy));
    rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle.y + rightPaddle.dy));

    ball.x += ball.dx;
    ball.y += ball.dy;

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
        log(`¡${currentMatch.winner} ha ganado el partido!`);
        endMatch();
    } else if (rightScore >= maxScore) {
        gameOver = true;
        currentMatch.winner = currentMatch.player2;
        log(`¡${currentMatch.winner} ha ganado el partido!`);
        endMatch();
    } else {
        resetBall();
    }
}

function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.dx = (Math.random() > 0.5 ? 4 : -4) * 1000;
    ball.dy = (Math.random() > 0.5 ? 4 : -4) * 1000;
}

function resetGameForNextMatch() {
    leftScore = 0;
    rightScore = 0;
    gameOver = false;
    isPaused = false;
    leftPaddle.y = (canvas.height - paddleHeight) / 2;
    rightPaddle.y = (canvas.height - paddleHeight) / 2;
    resetBall();
    currentMatch = tournament.getCurrentMatch();
    if (!currentMatch) {
        log("Error: No se pudo obtener el siguiente partido.");
        return;
    }
    log(`\nNuevo partido: ${currentMatch.player1} vs ${currentMatch.player2}`);
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

    ctx.font = "60px Courier New";
    ctx.fillText(leftScore, canvas.width / 3, 60);
    ctx.fillText(rightScore, (canvas.width / 4) * 2.5, 60);

    if (isPaused) {
        ctx.font = "30px Courier New";
        ctx.fillText("PAUSED", canvas.width / 2 - 60, canvas.height / 2);
    }
}

function gameLoop() {
    update();
    draw();
    if (!gameOver) {
        requestAnimationFrame(gameLoop);
    }
}

/***********************
 * 6. Conexión con API *
 ***********************/
async function endMatch() {
    if (!currentMatch) return;

    const winnerName = currentMatch.winner;
    const loserName = currentMatch.player1 === winnerName ? currentMatch.player2 : currentMatch.player1;
    const isFinal = tournament.isTournamentOver();

    try {
        const response = await fetch('/submit_tournament_match/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ winner: winnerName, loser: loserName, is_final: isFinal })
        });
        const data = await response.json();
        log(data.message || "Resultado reportado.");
    } catch (err) {
        log("Error al reportar el partido:", err.message);
    }

    tournament.setWinner(winnerName);
    if (!tournament.isTournamentOver()) {
        resetGameForNextMatch();
    } else {
        log(`🏆 Torneo finalizado. Campeón: ${winnerName}`);
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

/***********************
 * 7. Render Bracket Visual *
 ***********************/
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

/***********************
 * 8. Iniciar el Torneo *
 ***********************/
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch('/get_tournament_players/');
        const data = await response.json();

        if (!response.ok) {
            log("Error al obtener jugadores:", data.error);
            return;
        }

        const playerNames = data.players.map(p => p.username);
        tournament = new Tournament(playerNames);
        currentMatch = tournament.getCurrentMatch();

        renderBracket(tournament.matches);

        if (currentMatch) {
            log(`Comienza el torneo. Primer partido: ${currentMatch.player1} vs ${currentMatch.player2}`);
            resetGameForNextMatch();
        } else {
            log("Error: No hay partidos disponibles.");
        }
    } catch (err) {
        log("Error de red:", err.message);
    }
});
