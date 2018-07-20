document.addEventListener("DOMContentLoaded", () => {
    
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    

    // scroll to the most recent chat messages once page loads
    scroll_to_bottom();

    // declare constant variables
    const name = document.querySelector("#current-user").dataset.name;
    const channel = document.querySelector("h1").dataset.channel;

    
    socket.on("connect", () => {

        // add user to user-list on connect...
        
        // Get user name from #current-user dataset
        socket.emit("new user", {"name":name, "channel":channel});

        // Fire when a message is sent
        document.querySelector("#message-form").onsubmit = () => {
            let message = document.querySelector("#text-message").value;
            socket.emit('message sent', {"message":message, "channel":channel});
            document.querySelector("#text-message").value = "";
            document.querySelector("#text-message").focus;
            return false;
        };

        document.querySelector("#channels-link").onclick= () => {
            socket.emit("user left", {"name":name, "channel":channel})   
        }
    });

    socket.on("chat updated", data => {
        const li = document.createElement("li");
        li.innerHTML = `${data.sender} ${data.timestamp} <span class="message"> ${data.content}</span> `;
        document.querySelector("#message-list").append(li);
        scroll_to_bottom();
    });

    socket.on("user added", name => {
        // create the list item to add to users list
        let userLi = document.createElement("li");
        userLi.id = name;
        userLi.innerHTML = name;
        document.querySelector("#user-list").append(userLi);
        let autoLi = document.createElement("li");
        autoLi.className = "auto-message";
        autoLi.innerHTML = `${name} joined the channel`
        document.querySelector("#message-list").append(autoLi)
        
    })

    

    socket.on("gone", name => {
        let oldLi = document.querySelector(`#${name}`)
        oldLi.parentNode.removeChild(oldLi);
        let autoLi = document.createElement("li");
        autoLi.className = "auto-message";
        autoLi.innerHTML = `${name} left the channel`
        document.querySelector("#message-list").append(autoLi)
    })
});


function scroll_to_bottom(){
    let chatbox = document.querySelector('#chat-messages');
    chatbox.scrollTop = chatbox.scrollHeight;
}

