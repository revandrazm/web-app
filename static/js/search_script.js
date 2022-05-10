// show search result
let input = document.querySelector("input");

input.addEventListener("keyup", () => {
	$.get("/output?q=" + input.value, (accounts) => {
		let output = "";

		for (let id in accounts) {
			let username = accounts[id].username;
			output += "<li>" + username + "</li>";
		}
		document.querySelector("#show_username").innerHTML = output;
	});
});