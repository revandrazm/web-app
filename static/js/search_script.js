// show search result
let input = document.querySelector("input");
input.addEventListener("keyup", () => {
	$.get("/output?q=" + input.value, (accounts) => {
		let html = "";
		for (let id in accounts) {
			let username = accounts[id].username;
			html += "<li>" + username + "</li>";
		}
		document.querySelector("#showUsername").innerHTML = html;
	});
});