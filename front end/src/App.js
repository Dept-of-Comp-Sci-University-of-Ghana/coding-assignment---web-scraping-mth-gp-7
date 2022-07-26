import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

function App() {
	const [commonWords, setCommonWords] = useState({});
	const [summary, setSummary] = useState();

	const getSummary = () => {
		axios
			.get("http://127.0.0.1:8000/summary")
			.then((res) => {
				//setCommonWords(res);
				setSummary(res);
				console.log(res);
			})
			.catch((err) => {
				console.log(err);
			});
	};

	const getCommonWords = () => {
		axios
			.get("http://127.0.0.1:8000/common-words")
			.then((res) => {
				//setCommonWords(res);
				setCommonWords(res);
			})
			.catch((err) => {
				console.log(err);
			});
	};

	useEffect(() => {
		getCommonWords();
		getSummary();
		//getImages();
	}, []);

	//console.log(commonWords.data.commonNouns);
	return (
		<div className="w-screen h-screen bg-slate-200">
			<div className=" w-full h-20 bg-white shadow-lg flex justify-center items-center">
				<p className="font-bold text-blue-700 text-xl hover:uppercase">
					Project Findings
				</p>
			</div>
			<div className="grid grid-rows-3 grid-flow-col gap-8 h-3/4 m-8">
				<div class="row-span-3 bg-white p-8 overflow-scroll scrollbar-hide">
					{/* a list of the common nouns  */}
					<div className="m-6 shadow-lg transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">
						<p className="font-bold w-full bg-slate-500 px-8 rounded-t-xl h-10 flex justify-center items-center">
							Top 10 Nouns
						</p>
						<div className=" m-2 h-60 overflow-scroll scrollbar-hide p-4 flex justify-center items-center ">
							<ul className="divide-y">
								{commonWords.data.commonNouns.map((a) => (
									<li>{a[0] + " " + a[1]}</li>
								))}
							</ul>
						</div>
					</div>
					{/* a list of the common verbs */}
					<div className="m-6 shadow-lg transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">
						<p className="font-bold w-full bg-slate-500 px-8 rounded-t-xl flex justify-center items-center h-10">
							Top 10 Verbs
						</p>
						<div className="h-60 overflow-scroll scrollbar-hide p-4 m-2 flex justify-center items-center">
							<ul className="divide-y">
								{commonWords.data.commonVerbs.map((a) => (
									<li>{a[0] + " " + a[1]}</li>
								))}
							</ul>
						</div>
					</div>
					{/* a list of the common proper nouns */}
					<div className="m-6 shadow-lg transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">
						<p className="font-bold w-full bg-slate-500 px-8 rounded-t-xl flex justify-center items-center h-10">
							Top 10 Proper Nouns
						</p>
						<div className="h-60 overflow-scroll scrollbar-hide p-4 m-2 flex justify-center items-center">
							<ul className="divide-y">
								{commonWords.data.commonPnouns.map((a) => (
									<li className="">{a[0] + " " + a[1]}</li>
								))}
							</ul>
						</div>
					</div>
				</div>
				<div className="col-span-2 bg-white shadow-lg p-4">
					<div>
						<p className="font-bold w-full bg-gray-400 hover:bg-slate-500 px-8 h-10 flex justify-center items-center text-xl">
							Summary of the Extracted Text
						</p>
					</div>
					<div class=" overflow-scroll scrollbar-hide h-3/4">
						<p className="">{summary.data}</p>
					</div>
				</div>
				<div class="row-span-2 col-span-2 grid grid-cols-2 gap-8 ">
					<div className="shadow-lg transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">
						<img
							className="w-full h-full"
							src={`http://127.0.0.1:8000/graphs-noun`}
						/>
					</div>
					<div className="shadow-lg transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300">
						<img
							className=" w-full h-full"
							src={`http://127.0.0.1:8000/graphs-pnoun`}
						/>
					</div>
				</div>
			</div>
		</div>
	);
}

export default App;
