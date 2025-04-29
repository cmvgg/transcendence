/**********************
 * 1. Lógica del Torneo
 **********************/
class Tournament {
	constructor(players) {
		this.players = players.slice();
		this.match = this.createBracket(this.players);
		this.currentRound = 0;
	}
  
	//Crea el bracket inicial; si la cantidad es impar, se agrega "BYE"
	createBracket(players) {
		let matches = [];
		if (players.length % 2 !== 0) {
			players.push("BYE");
		}
		for (let i = 0; i < players.length; i += 2) {
			matches.push({
				player1: players[i],
				player2: players[i + 1],
				winner: null
			});
		}
		return [matches]; // Cada elemento del array representa una ronda
	}
  
	//Devuelve el partido actual de la ronda actual
	getCurrentMatch() {
		const currentMatches = this.match[this.currentRound];
		return currentMatches.find(match => match.winner === null);
	}
  
	//Registra el ganador en el partido y, si la ronda abaca, genera la siguiente ronda
	setWinner(winner) {
		const match = this.getCurrentMatch();
		if (!match)
			return;
		match.winner = winner;
		log(`Partido finalizado: ${match.player1} vs ${match.player2} - Ganador: ${winner}\n`);

		//Si la ronda actual acabó, generar la siguiente ronda
		if (this.match[this.currentRound].every(m => m.winner !== null)) {
			this.generateNextRound();
		}
	}
  
	generateNextRound() {
		const winners = this.match[this.currentRound].map(match => match.winner);
		if (winners.length === 1) {
			log(`\n\n¡El campeón del torneo es ${winners[0]}!`);
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
				winner: null
			});
		}
		this.match.push(nextRoundMatches);
		this.currentRound++;
		log(`Iniciando ronda ${this.currentRound + 1}`);
		const nextMatch = this.getCurrentMatch();
		//log(`Próximo partido: ${nextMatch.player1} vs ${nextMatch.player2}`);
	}
  
	isTournamentOver() {
		const lastRound = this.match[this.match.length - 1];
		return lastRound.length === 1 && lastRound[0].winner !== null;
	}
  }
  
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

document.addEventListener("keydown", (e) => {
	if (e.key === "w") leftPaddle.dy = -5;
	if (e.key === "s") leftPaddle.dy = 5;
	if (e.key === "ArrowUp") rightPaddle.dy = -5;
	if (e.key === "ArrowDown") rightPaddle.dy = 5;
	if (e.key.toLowerCase() === "p") isPaused = !isPaused;
});
document.addEventListener("keyup", (e) => {
	if (e.key === "w" || e.key === "s") leftPaddle.dy = 0;
	if (e.key === "ArrowUp" || e.key === "ArrowDown") rightPaddle.dy = 0;
});
//Boton de pausa
document.getElementById("pauseButton").addEventListener("click", () => {
	isPaused = !isPaused;
});
document.getElementById("goHome").addEventListener("click", () => {
	document.getElementById("goHome").disabled = true;
	window.location.href = "../templates/index";
});

function update() {
	if (gameOver || isPaused)
		return;

	//Mover paletas
	leftPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, leftPaddle.y + leftPaddle.dy));
	rightPaddle.y = Math.max(0, Math.min(canvas.height - paddleHeight, rightPaddle.y + rightPaddle.dy));

	//Mover la pelota
	ball.x += ball.dx;
	ball.y += ball.dy;

	//Rebote en los bordes
	if (ball.y - ball.radius < borderHeight || ball.y + ball.radius > canvas.height - borderHeight)
		ball.dy *= -1;

	//Rebote en las paletas (básico)
	if (ball.x - ball.radius < paddleWidth && ball.y > leftPaddle.y && ball.y < leftPaddle.y + paddleHeight)
		ball.dx *= -1;
	if (ball.x + ball.radius > canvas.width - paddleWidth && ball.y > rightPaddle.y && ball.y < rightPaddle.y + paddleHeight)
		ball.dx *= -1;

	//Verificar si la pelota toca los lados
	if (ball.x - ball.radius < 0) {
		rightScore++;
		checkGameOver();
	} else if (ball.x + ball.radius > canvas.width) {
		leftScore++;
		checkGameOver();
	}
}

//Verifica si llegó al puntaje máximo para finalizar el partido
function checkGameOver() {
	if (leftScore >= maxScore) {
		gameOver = true;
		winner = currentMatch.player1;
		endMatch();
	} else if (rightScore >= maxScore) {
		gameOver = true;
		winner = currentMatch.player2;
		endMatch();
	} else {
		resetBall();
	}
}


function resetBall() {
	ball.x = canvas.width / 2;
	ball.y = canvas.height / 2;
	ball.dx = (Math.random() > 0.5 ? 4 : -4);
	ball.dy = (Math.random() > 0.5 ? 4 : -4);
}

//Reinicia el juego para el siguiente partido del torneo
function resetGameForNextMatch() {
	leftScore = 0;
	rightScore = 0;
	gameOver = false;
	isPaused = false;
	leftPaddle.y = (canvas.height - paddleHeight) / 2;
	rightPaddle.y = (canvas.height - paddleHeight) / 2;
	resetBall();
	currentMatch = tournament.getCurrentMatch();
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
	//log("ejecutando gameLoop");
	update();
	draw();
	if (!gameOver) {
		requestAnimationFrame(gameLoop);
	} else {
		log("Partido terminado");
	}
}


/* const players = ["Bob", "Alice", "Charlie", "David"];
const tournament = new Tournament(players); */
//startTournament();
/* let currentMatch = tournament.getCurrentMatch();
log("Inicio del torneo");
log("Jugadores: " + players);
log(`Primer partido: ${currentMatch.player1} vs ${currentMatch.player2}\n`);

gameLoop(); */
/***********************
 * 5. Conexión con API *
***********************/

let tournament = null;
const tournament_id = document.getElementById('tournamentId').value;
//log("Tournament ID:", tournament_id);

document.addEventListener("DOMContentLoaded", async () => {
	const players = await fetchPlayers();
	log("\n==== GARGANDO TORNEO ====");
	if (players.length >= 2) {
		tournament = new Tournament(players);
		let currentMatch = tournament.getCurrentMatch();
		if (!currentMatch) {
			log("No hay partidos disponibles.");
			return;
		}
		log("Inicio del torneo");
		log(`Primer partido: ${currentMatch.player1} vs ${currentMatch.player2}\n`);
		gameLoop();
	} else {
		log("No hay suficientes jugadores para iniciar el torneo.");
	}
});

async function fetchPlayers() {
	try {
		const response = await fetch('/get_players/');
		if (response.ok) {
			const players = await response.json();
            log("\n==== JUGADORES DEL TORNEO ====");
            players.forEach(player => log(`Nombre: ${player.alias}`));
            return players.map(player => player.alias);
		} else {
			log("Error al obtener los jugadores.");
			return [];
		}
	} catch (error) {
		log(`Error de conexión: ${error.message}`);
		return [];
	}
}


async function verifyOrCreateTournament() {
    const tournamentId = document.getElementById('tournamentId').value;

    try {
        const response = await fetch(`/tournaments/${tournamentId}/`);
        
        if (response.ok) {
            const tournament = await response.json();
            log(`Torneo encontrado: ID ${tournament.id}, Nombre: ${tournament.name}`);
        } else if (response.status === 404) {
            log(`Torneo con ID ${tournamentId} no encontrado. Creando uno nuevo...`);

            const createResponse = await fetch('/create-tournament/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });

            if (createResponse.ok) {
                const newTournament = await createResponse.json();
                log(`Torneo creado con éxito: ID ${newTournament.tournament_id}, Nombre: ${newTournament.message}`);
                document.getElementById('tournamentId').value = newTournament.tournament_id;
            } else {
                const errorText = await createResponse.text();
                log(`Error al crear el torneo: ${errorText}`);
            }
        } else {
            log(`Error al verificar el torneo: ${response.statusText}`);
        }
    } catch (error) {
        log(`Error de conexión: ${error.message}`);
    }
}

async function submitTournamentResults() {
    const allMatches = tournament.match.flat();
    const results = [];

	allMatches.forEach(match => {
		if (match.winner && match.winner !== "BYE" && match.player1 && match.player2) {
			const loser = match.winner === match.player1 ? match.player2 : match.player1;
			if (loser && loser !== "BYE") {
				results.push({
					winner: match.winner,
					loser: loser
				});
			}
		}
	});

    try {
        const response = await fetch('tournament-results/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
				tournament_id: tournament_id,
                name: `Torneo de Pong ${new Date().toLocaleDateString()}`,
                results: results
            })
        });
		if (response.ok) {
			const responseData = await response.json();
			log("¡Torneo guardado correctamente!");
			log("Respuesta del servidor:", responseData);
        } else {
			const errorData = await response.text();
            log(`Error al guardar el torneo: ${JSON.stringify(errorData)}`);
        }
    } catch (error) {
        log(`Error de conexión: ${error.message}`);
    }
}

//Función para obtener el valor de una cookie por su nombre (Sin acabar)
async function loadTournamentParticipants() {
	try {
		const response = await fetch('get_players/?tournament_id=' + tournament_id);
		
		if (response.ok) {
			const players = await response.json();
			log("\n==== JUGADORES DEL TORNEO ====");

			if (players && players.length > 0) {
				players.forEach(player => {
					log(`Nombre: ${player.alias} - Victorias: ${player.wins}, Derrotas: ${player.losses}`);
				});

				//const tournament = new Tournament(participants.map(p => p.alias));
                //startTournament(tournament);
			} else {
				log("No hay jugadores registrados en el torneo.");
			}
		} else {
			log("Error al cargar los jugadores del torneo.");
		}
	} catch (error) {
		log(`Error de conexión: ${error.message}`);
	}
}

function getCookie(name) {
	let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function loadTournamentHistory() {
	try {
		const response = await fetch('/tournaments/');
        
        if (response.ok) {
			const data = await response.json();
            log("\n==== HISTORIAL DE TORNEOS ====");
            
            if (data.results && data.results.length > 0) {
				data.results.forEach(tournament => {
					const date = new Date(tournament.start_date).toLocaleString();
                    log(`ID: ${tournament.id} | Nombre: ${tournament.name} | Fecha: ${date}`);
                });
            } else {
				log("No hay torneos registrados.");
            }
        } else {
			log("Error al cargar el historial de torneos.");
        }
    } catch (error) {
		log(`Error de conexión: ${error.message}`);
    }
}

async function loadPlayerRanking() {
	try {
		const response = await fetch('/users/');
        
        if (response.ok) {
			const data = await response.json();
            log("\n==== RANKING DE JUGADORES ====");
            
            if (data.results && data.results.length > 0) {
                const sortedPlayers = [...data.results].sort((a, b) => b.wins - a.wins);
                
                sortedPlayers.forEach((player, index) => {
					log(`${index + 1}. ${player.alias} - Victorias: ${player.wins}, Derrotas: ${player.losses}`);
                });
            } else {
				log("No hay jugadores registrados.");
            }
        } else {
			log("Error al cargar el ranking de jugadores.");
        }
    } catch (error) {
		log(`Error de conexión: ${error.message}`);
    }
}

//Finaliza el partido, notifica al torneo y, si aún no termina el torneo, reinicia para el siguiente partido
//Si el torneo terminó, envía los resultados al backend 
function endMatch() {
	tournament.setWinner(winner);

	if (tournament.isTournamentOver()) {
		log("\n¡EL TORNEO HA FINALIZADO!");
		log(`El campeón es: ${winner}`);
		loadTournamentParticipants();
		submitTournamentResults();
	} else {
		setTimeout(resetGameForNextMatch, 2000);
		gameLoop();
	}
}

function addBackendButtons() {
	let controlsDiv = document.getElementById("gameControls");
    
    if (!controlsDiv) {
		controlsDiv = document.createElement("div");
        controlsDiv.id = "gameControls";
		
        const canvas = document.getElementById("gameCanvas");
        if (canvas && canvas.parentNode) {
			canvas.parentNode.insertBefore(controlsDiv, canvas.nextSibling);
        } else {
			document.body.appendChild(controlsDiv);
        }
    }
	
    if (!document.getElementById("historyButton")) {
		const historyButton = document.createElement("button");
        historyButton.id = "historyButton";
        historyButton.textContent = "Ver Historial";
        historyButton.className = "game-button";
        historyButton.addEventListener("click", loadTournamentHistory);
        controlsDiv.appendChild(historyButton);
    }
    
    if (!document.getElementById("rankingButton")) {
		const rankingButton = document.createElement("button");
        rankingButton.id = "rankingButton";
        rankingButton.textContent = "Ver Ranking";
        rankingButton.className = "game-button";
        rankingButton.addEventListener("click", loadPlayerRanking);
        controlsDiv.appendChild(rankingButton);
    }
}

document.addEventListener("DOMContentLoaded", addBackendButtons);
