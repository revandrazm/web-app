var update = function () {
    document.querySelector("#time").innerHTML = moment().format("h:mm:ss A");
 };

$(document).ready(function(){
    setInterval(update, 100);
});