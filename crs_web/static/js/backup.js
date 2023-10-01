// JavaScript to handle sending and displaying messages (with avatars)
/*
 Variables
*/
let chatName = "";
let chatSocket = null;
let chatWindowUrl = window.location.href;
/*
Functions
*/

function create_UUID4() {
  return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, (c) =>
    (
      c ^
      (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
    ).toString(16)
  );
}

/*
Code
*/
var roomName = create_UUID4();
var messageText = "";

console.log(roomName);

const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
);

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  document.querySelector("#chat-messages").value += data.message + "\n";
};

chatSocket.onclose = function (e) {
  console.error("Chat socket closed unexpectedly");
};

document.querySelector("#message-input").focus();
document.querySelector("#message-input").onkeyup = function (e) {
  if (e.key === "Enter") {
    // enter, return
    document.querySelector("#send-button").click();
  }
};

document.querySelector("#send-button").onclick = function (e) {
  const messageInputDom = document.querySelector("#message-input");
  const message = messageInputDom.value;
  chatSocket.send(
    JSON.stringify({
      message: message,
    })
  );
  messageInputDom.value = "";
};
///

document.addEventListener("DOMContentLoaded", function () {
  const messageInput = document.getElementById("message-input");
  const sendButton = document.getElementById("send-button");
  const chatMessages = document.querySelector(".chat-messages");

  sendButton.addEventListener("click", function () {
    const messageText = messageInput.value.trim();
    console.log(messageText);
    console.log("in sendButton.addEventListener");
    // create room here

    const chatSocket = new WebSocket(
      "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
    );

    // Event handler for when the WebSocket connection is established
    chatSocket.addEventListener("open", (event) => {
      console.log("WebSocket connection opened:", event);

      // Send a message to the WebSocket server
      chatSocket.send(
        JSON.stringify({
          message: messageText,
        })
      );
      messageText = "";
    });

    // Event handler for when a message is received from the WebSocket server
    chatSocket.addEventListener("message", (event) => {
      console.log("Message from server:", event.data);
      console.log(event);
      // You can handle the received message here
      if (event.data !== "") {
        console.log("in message div");
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message");
        messageDiv.innerHTML = `
        <div class="d-flex flex-row justify-content-end mb-4">
        <div class="p-3 me-3 border" style="border-radius: 15px; background-color: #fbfbfb;">
          <p class="small mb-0">${event.data}</p>
        </div>
        <img src="/static/images/robot.png" alt="avatar 1" style="width: 45px; height: 100%;">
        </div>
                  `;
        chatMessages.appendChild(messageDiv);
        messageInput.value = "";
      }
    });

    // Event handler for handling WebSocket errors
    chatSocket.addEventListener("error", (event) => {
      console.error("WebSocket error:", event);
    });

    // Event handler for when the WebSocket connection is closed
    chatSocket.addEventListener("close", (event) => {
      if (event.wasClean) {
        console.log("WebSocket connection closed cleanly:", event);
      } else {
        console.error("WebSocket connection abruptly closed:", event);
      }
    });

    if (messageText !== "") {
      const messageDiv = document.createElement("div");
      messageDiv.classList.add("message");
      messageDiv.innerHTML = `
                    <div class="d-flex flex-row justify-content-start mb-4">
                    <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp" alt="avatar 1" style="width: 45px; height: 100%;">
                    <div class="p-3 ms-3" style="border-radius: 15px; background-color: rgba(57, 192, 237,.2);">
                      <p class="small mb-0">${messageText}</p>
                    </div>
                    </div>
                `;
      chatMessages.appendChild(messageDiv);
      messageInput.value = "";
    }
  });

  messageInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      console.log("send button clicked");
      sendButton.click();
    }
  });
});
