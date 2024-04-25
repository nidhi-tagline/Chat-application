const roomName = JSON.parse(document.getElementById("room-name").textContent);

let chatLog = document.getElementById("chat-log")
let chatMessageInput = document.getElementById("chat-message-input")
let chatMessageSend = document.getElementById("chat-message-send")
let onlineUsersSelector = document.getElementById("online-users-selector")


// function to add user to online users list
function onlineUsersSelectorAdd(value) {
    if (document.querySelector("option[value='" + value + "']")) return;
    let newOption = document.createElement("option");
    newOption.value = value;
    newOption.innerHTML = value;
    onlineUsersSelector.appendChild(newOption);
}

// function to remove user from online users list
function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption) {
        oldOption.remove();
    }
}

chatMessageInput.focus()

// when enter key is pressed message is sent
chatMessageInput.onkeyup = function(e) {
    if (e.key == 'Enter') {
        chatMessageSend.click();
    }
};

// when click send button message sent to websocket
chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) return;
    chatSocket.send(JSON.stringify({
        "message": chatMessageInput.value,
    }));
    chatMessageInput.value = "";
};

let chatSocket = null;

// function to connect to websocket
function connect() {
    chatSocket = new WebSocket("ws://"
    + window.location.host
    + "/ws/chat/"
    + roomName
    + "/"
    );

    // when websocket is opened and message is sent
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        // switch case to handle different types of messages according to type
        switch (data.type) {
            // display message in chat log
            case "chat_message":
                chatLog.value += data.message + "  -" + data.user + "\n";
                break;

            // display list of online users in online users list
            case "user_list":
                for (let i = 0; i < data.users.length; i++) {
                    onlineUsersSelectorAdd(data.users[i])
                }
                break;

            // display message in chat log when new user joins
            case "user_join":
                chatLog.value += data.user + " joined the room.\n";
                onlineUsersSelectorAdd(data.user)
                break;

            // display message in chat log when user leaves
            case "user_leave":
                chatLog.value += data.user + " left the room.\n";
                onlineUsersSelectorRemove(data.user)
                break;

            default:
                console.error("Unknown message type!");
                break;
        }
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    // when websocket is closed
    chatSocket.onclose = function(e) {
        console.log("Websocket connection closed unexpectedly.");
    };

    // if error encountered then close websocket and log error
    chatSocket.onerror = function(err) {
        console.log("error encountered:" + err.message);
        chatSocket.close();
    }
}

connect();