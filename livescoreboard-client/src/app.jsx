import { useState, useEffect } from "preact/hooks";
import { useAutoAnimate } from "@formkit/auto-animate/react";
import { useReward } from "react-rewards";
import io from "socket.io-client";
import Score from "./components/Score";
import Popup from "./components/Popup";
import ownage from "./ownage.mp3";
import blood from "./blood.mp3";
import pwn from "./pwn.mp3";
import "./app.scss";

const useAudio = (url) => {
	const [audio] = useState(new Audio(url));
	const [playing, setPlaying] = useState(false);

	const toggle = () => {
		audio.load();
		audio.play();
		setPlaying(true);
	};

	useEffect(() => {
		audio.addEventListener("ended", () => setPlaying(false));
		return () => audio.removeEventListener("ended", () => setPlaying(false));
	}, [setPlaying]);

	return [playing, toggle];
};

const max = 12;
const colors = ["#f6dc43", "#bdcccc", "#a88834"];
const App = () => {
	const [socket, setSocket] = useState(null);
	const [scoreboard, setScoreboard] = useState([]);
	const [parent] = useAutoAnimate();
	const [scoreboard1] = useAutoAnimate();
	const [scoreboard2] = useAutoAnimate();
	const [playing1, toggle1] = useAudio(ownage);
	const [playing2, toggle2] = useAudio(blood);
	const [playing3, toggle3] = useAudio(pwn);
	const [nums, setNums] = useState([]);
	const [last, setLast] = useState(0);
	const [blood2, setBlood2] = useState([]);
	const [pwn2, setPwn2] = useState([]);
	const { reward, _isAnimating } = useReward("rewardId", "confetti", {
		elementCount: 100,
		startVelocity: 45,
		spread: 90,
		lifetime: 300,
		elementSize: 10,
	});

	useEffect(() => {
		const newSocket = io(`http://${window.location.hostname}:3000`);
		// const newSocket = io(`https://livescoreboard.ctf.itemize.no`);
		setSocket(newSocket);
		return () => newSocket.close();
	}, []);

	useEffect(() => {
		if (!socket) return;
		socket.on("update-scoreboard", (scoreboard) => {
			console.log("update", scoreboard);
			setScoreboard(scoreboard);
		});
		socket.on("full-clear", (num) => {
			console.log("Top", num);
			setNums((nums) => [...nums, num]);
		});

		socket.on("blood", (info) => {
			console.log("Blood", info);
			setNums((nums) => [...nums, 10]);
			setBlood2((blood2) => [...blood2, info]);
		});

		socket.on("pwn", (info) => {
			console.log("Pwn");
			setNums((nums) => [...nums, -10]);
			setPwn2((pwn2) => [...pwn2, info]);
		});

		return () => {
			socket.off("update-scoreboard");
			socket.off("full-clear");
			socket.off("blood");
			socket.off("pwn");
		};
	}, [socket, setScoreboard, setNums]);

	useEffect(() => {
		if (nums.length === 0 || playing3 || playing2 || playing1) return;
		if (!(nums[0] < 0)) return;
		setNums((nums) => {
			if (nums.length >= 1 && !playing3) {
				reward();
				toggle3();
			}
			return nums.slice(1);
		});
	}, [playing3, playing2, playing1, nums, setNums]);

	useEffect(() => {
		if (nums.length === 0 || playing2 || playing1) return;
		if (!(nums[0] >= 4)) return;
		setNums((nums) => {
			if (nums.length >= 1 && !playing2) {
				reward();
				toggle2();
			}
			return nums.slice(1);
		});
	}, [playing2, playing1, nums, setNums]);

	useEffect(() => {
		if (nums.length === 0 || playing1) return;
		if (!(nums[0] >= 0 && nums[0] <= 3)) return;
		setNums((nums) => {
			if (nums.length >= 1 && !playing1) {
				reward();
				toggle1();
				setLast(nums[0] - 1);
			}
			return nums.slice(1);
		});
	}, [playing1, nums, setNums]);

	return (
		<div>
			<h1>Scoreboard - Nybegynnerkurs CTF 2022</h1>
			<span id="rewardId" class="reward" />
			{playing1 && nums.length >= 0 && (
				<Popup color={colors[last]} text={"Full-clear!"} svg="cup" />
			)}
			{playing2 && nums.length >= 0 && (
				<Popup color={"tomato"} text={`First blood!`} svg="blood" />
			)}
			<div
				class={`scoreboard ${scoreboard.length > max ? "split" : ""}`}
				ref={parent}
			>
				<div ref={scoreboard1}>
					<Score user={{ name: "Name", score: "Score", placement: "No" }} />
					{scoreboard.slice(0, max).map((user, placement) => (
						<Score user={{ ...user, placement: placement + 1 }} key={user.id} />
					))}
				</div>
				<div ref={scoreboard2} hidden={scoreboard.length <= max}>
					<Score user={{ name: "Name", score: "Score", placement: "No" }} />
					{scoreboard.slice(max, max * 2).map((user, placement) => (
						<Score
							user={{ ...user, placement: placement + 1 + max }}
							key={user.id}
						/>
					))}
				</div>
			</div>
		</div>
	);
};
export default App;
