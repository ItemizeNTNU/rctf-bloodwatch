import http from "http";
import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import { Server } from "socket.io";

let total_tasks = 0;
let scoreboard = [];
let dev = process.env.DEV || false;
// dev = false;
console.log("DEV MODE:", dev);

const app = express();
app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Configuring json response
app.set("json spaces", 2);

const server = http.createServer(app);
const io = new Server(server, {
	cors: {
		origin: "*",
	},
});

const winners = { top1: null, top2: null, top3: null };

const updateScoreboard = (socket) => {
	try {
		socket.emit("update-scoreboard", scoreboard);

		// Check and save top3 solvers
		if (scoreboard[0]?.total_solves >= total_tasks && !winners.top1) {
			winners.top1 = scoreboard[0];
			io.emit("full-clear", 1);
		}
		if (scoreboard[1]?.total_solves >= total_tasks && !winners.top2) {
			winners.top2 = scoreboard[1];
			io.emit("full-clear", 2);
		}
		if (scoreboard[2]?.total_solves >= total_tasks && !winners.top3) {
			winners.top3 = scoreboard[2];
			io.emit("full-clear", 3);
		}
	} catch (_err) {
		console.log("error: couldn't update scoreboard :c");
	}
};
updateScoreboard(io);

io.on("connection", (socket) => {
	console.log(`Socket ${socket.id} connected`);

	updateScoreboard(socket);

	socket.on("disconnect", () => {
		console.log("User disconnected");
	});
});

app.post("/score", (req, res) => {
	const { score } = req.body;
	scoreboard = score;
	updateScoreboard(io);
	res.json({ status: 0 });
});

app.post("/blood", (req, res) => {
	const { team, challenge } = req.body;
	io.emit("blood", { team: team, challenge: challenge });
	updateScoreboard(io);
	res.json({ status: 0 });
});

app.post("/pwn", (req, res) => {
	const { team, challenge } = req.body;
	io.emit("pwn", { team: team, challenge: challenge });
	updateScoreboard(io);
	res.json({ status: 0 });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, "0.0.0.0", () => {
	console.log(`Listening on *:${PORT}`);
});
