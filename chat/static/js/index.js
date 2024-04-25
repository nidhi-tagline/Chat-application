
document.querySelector("#room-input").focus();

// when enter is pressed room name from input is submitted
document.querySelector("#room-input").onkeyup = function(e) {
    if (e.key == "Enter") {
        document.querySelector("#room-connect").click();
    }
};

// Redirect to the room page when button is clicked
document.querySelector("#room-connect").onclick = function() {
    let roomName = document.querySelector("#room-input").value;
    window.location.pathname = "chat/" + roomName + "/";
}

// Redirect to the room page when a room is selected from Active rooms list
document.querySelector("#room-select").onchange = function() {
    let roomName = document.querySelector("#room-select").value.split(" (")[0];
    window.location.pathname = "chat/" + roomName + "/";
}