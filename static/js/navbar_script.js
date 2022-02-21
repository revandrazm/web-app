// open new tab on click
function openNewTab(link) {
    window.open(link, "_blank")
}

// show time in id: time
var update = function () {
    document.querySelector("#time").innerHTML = moment().format("h:mm:ss A");
 };

$(document).ready(function(){
    setInterval(update, 100);
});