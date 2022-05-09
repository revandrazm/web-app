// clear class: error-message on keydown on any input
document.querySelectorAll("input").forEach(item => {
	item.addEventListener("keydown", () => {
		document.querySelector(".error-message").innerHTML = "<br>";
	});
});