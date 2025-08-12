window.onload = async function () {
    await fetchPlayersForGame("1vs1");
    resetBall();
    gameLoop();
};

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const paddleWidth = 3;
const paddleHeight = 20; //cambiar a 30
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

/*********************************************
 * 2. Redirigir console.log al elemento HTML *
 *********************************************/
function logMessage(message) {
	const logDiv = document.getElementById("log");
	const p = document.createElement("p");
	p.innerHTML = message.replace(/\n/g, "<br>"); // Reemplaza \n por <br>
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
/* **** */

async function fetchPlayersForGame(mode = "1vs1") {
    try {
        const response = await fetch(`/get_players_for_game?game_type=${mode}`);
        const data = await response.json();
        if (response.ok) {
            playerUsernames = data.players.map(p => p.username);
            log("puta asignados:", playerUsernames);
        } else {
            log("Error obteniendo jugadores:", data.error);
        }
    } catch (err) {
        log("Error en la conexión:", err.message);
    }
}

/* document.getElementById("pauseButton").addEventListener("click", () => {
    isPaused = true;
});
document.getElementById("startButton").addEventListener("click", () => {
    isPaused = false;
}); */

document.getElementById("pauseButton").addEventListener("click", () => isPaused = true);
document.getElementById("startButton").addEventListener("click", () => isPaused = false);

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

function update() {
    if (gameOver || isPaused) return;
    
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
    console.log("Verificando si el juego ha terminado...");
    console.log(`Puntajes: Izquierdo ${leftScore}, Derecho ${rightScore}, MaxScore: ${maxScore}`);
    console.log(`puta asignados: ${playerUsernames}`);

    if (playerUsernames.length < 2) {
        console.log("No hay suficientes jugadores.");
        return;
    }

    if (leftScore >= maxScore) {
        log("El jugador izquierdo ha ganado.");
        gameOver = true;
        winner = playerUsernames[0];
        console.log(`Actualizando estadísticas para ${playerUsernames[0]} y ${playerUsernames[1]}`);
        await updateUserProfile(playerUsernames[0], 1, 0);
        await updateUserProfile(playerUsernames[1], 0, 1);
        console.log("Llamando a sync1vs1Stats...");
        await sync1vs1Stats(); // Sincronizar datos para 1vs1
    } else if (rightScore >= maxScore) {
        console.log("El jugador derecho ha ganado.");
        gameOver = true;
        winner = playerUsernames[1];
        console.log(`Actualizando estadísticas para ${playerUsernames[1]} y ${playerUsernames[0]}`);
        await updateUserProfile(playerUsernames[1], 1, 0);
        await updateUserProfile(playerUsernames[0], 0, 1);
        console.log("Llamando a sync1vs1Stats...");
        await sync1vs1Stats(); // Sincronizar datos para 1vs1
    } else {
        console.log("El juego continúa. Reiniciando la pelota.");
        resetBall();
    }
}

async function sync1vs1Stats() {
    console.log("Entrando a sync1vs1Stats...");
    try {
        const response = await fetch('/sync_1vs1_stats/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });

        const data = await response.json();
        if (!response.ok) {
            log("Error al sincronizar estadísticas 1vs1:", data.error);
        } else {
            log("Estadísticas 1vs1 sincronizadas:", data.message);
        }
    } catch (error) {
        log("Error de conexión al sincronizar estadísticas 1vs1:", error.message);
    }
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
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = leftPaddle.color;
    ctx.fillRect(0, leftPaddle.y, paddleWidth, paddleHeight);

    ctx.fillStyle = rightPaddle.color;
    ctx.fillRect(canvas.width - paddleWidth, rightPaddle.y, paddleWidth, paddleHeight);

    ctx.fillStyle = "white";
    ctx.font = "20px monospace";
    ctx.fillText(leftScore, canvas.width / 3, 20);
    ctx.fillText(rightScore, (canvas.width / 4) * 2.5, 20);

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
