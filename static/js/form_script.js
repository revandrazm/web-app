// clear id: error-message on keydown on any input
document.querySelectorAll("input").forEach(item => {
	item.addEventListener("keydown", function() {
		document.querySelector("#error-message").innerHTML = "<br>";
	});
});