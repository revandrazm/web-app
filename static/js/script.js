document.querySelectorAll("input").forEach(item => {
    item.addEventListener("keydown", function() {
        document.querySelector("#error-message").innerHTML = "<br>";
    });
});