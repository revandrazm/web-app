var update = function () {
    document.querySelector("#time").innerHTML = moment().format("HH:mm:ss A");
 };

$(document).ready(function(){
    setInterval(update, 100);
});