// JavaScript to handle sending and displaying messages (with avatars)
let chatName = "";
let chatSocket = null;
let chatWindowUrl = window.location.href;

document.addEventListener("DOMContentLoaded", function () {
  const messageInput = document.getElementById("message-input");
  const sendButton = document.getElementById("send-button");
  const chatMessages = document.querySelector(".chat-messages");

  sendButton.addEventListener("click", function () {
    const messageText = messageInput.value.trim();
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
      sendButton.click();
    }
  });
});

// Replace 'ws://example.com' with the WebSocket server URL you want to connect to
const socket = new WebSocket(`ws://${window.location.host}/ws/chat/`);

// Event handler for when the WebSocket connection is established
socket.addEventListener("open", (event) => {
  console.log("WebSocket connection opened:", event);

  // Send a message to the WebSocket server
  const message = "Hello, WebSocket!";
  socket.send(message);
});

// Event handler for when a message is received from the WebSocket server
socket.addEventListener("message", (event) => {
  console.log("Message from server:", event.data);

  // You can handle the received message here
});

// Event handler for handling WebSocket errors
socket.addEventListener("error", (event) => {
  console.error("WebSocket error:", event);
});

// Event handler for when the WebSocket connection is closed
socket.addEventListener("close", (event) => {
  if (event.wasClean) {
    console.log("WebSocket connection closed cleanly:", event);
  } else {
    console.error("WebSocket connection abruptly closed:", event);
  }
});
