// JavaScript to handle sending and displaying messages (with avatars)
/*
 Variables
*/
let chatSocket = null;
/*
Functions
*/
function validateForm() {
  var selectElement = document.getElementById("movie-input");

  // Check if an option other than the default is selected
  if (selectElement.value.trim()) {
    alert("Please select an option before submitting the form.");
    return false; // Prevent form submission
  }

  // Continue with form submission if an option is selected
  return true;
}
function create_UUID4() {
  return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, (c) =>
    (
      c ^
      (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
    ).toString(16)
  );
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var conversationId = "";
var messageText = "";
var roomName = "";
var roomName = create_UUID4();
var chatURL = "ws://" + window.location.host + "/ws/chat/" + roomName + "/";
var convURL =
  "http://" + window.location.host + "/chat/ajax/create-conversation/";

var recURL = "http://" + window.location.host + "/movie/ajax/recommend-movies/";

document.addEventListener("DOMContentLoaded", function () {
  const messageInput = document.getElementById("message-input");
  const sendButton = document.getElementById("send-button");
  const chatMessages = document.querySelector(".chat-messages");
  const recommendButton = document.getElementById("recommend-button");
  const recommendMovie = document.getElementById("recommended-movies");
  /*
Code for talk to me button
*/

  document.querySelector("#open-chat-button").onclick = function (e) {
    // add code for starting conversation
    if (conversationId === "") {
      payload = { status: "Active" };

      fetch(convURL, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFTOKEN": getCookie("csrftoken"),
          "Content-type": "application/json",
        },
        body: JSON.stringify({ agentId: 1 }),
      })
        .then((response) => response.json())
        .then((data) => {
          conversationId = data.id;
        });
    }
  };

  sendButton.addEventListener("click", function () {
    const messageText = messageInput.value.trim();
    messageJSON = {
      message: messageText,
      conversationId: conversationId,
    };

    const chatSocket = new WebSocket(
      "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
    );

    // Event handler for when the WebSocket connection is established
    chatSocket.addEventListener("open", (event) => {
      console.log("WebSocket connection opened:", event);

      // Send a message to the WebSocket server
      chatSocket.send(
        JSON.stringify({
          message: messageJSON,
        })
      );
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
    // Event handler for when a message is received from the WebSocket server
    chatSocket.addEventListener("message", (event) => {
      console.log("Message from server:", event.data);
      botMessage = JSON.parse(event.data);
      // You can handle the received message here
      if (event.data !== "") {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message");
        messageDiv.innerHTML = `
            <div class="d-flex flex-row justify-content-end mb-4">
            <div class="p-3 me-3 border" style="border-radius: 15px; background-color: #fbfbfb;">
                <p class="small mb-0">${botMessage["message"]}</p>
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
  });

  messageInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      sendButton.click();
    }
  });
  // movieInput.addEventListener("input", function () {
  //   var movieInputValue = movieInput.value;
  //   console.log(movieInputValue);
  //   const movieTitle = movieInputValue.trim();
  // });
  recommendButton.addEventListener("click", function (event) {
    const movieInputValue = document.getElementById("movie-input");
    console.log(movieInputValue.value);
    var movieTitle = movieInputValue.value.trim();
    console.log(movieTitle);
    if (movieTitle !== "") {
      fetch(recURL, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFTOKEN": getCookie("csrftoken"),
          "Content-type": "application/json",
        },
        body: JSON.stringify({ movieTitle: movieTitle }),
      })
        .then((response) => response.json())
        .then((data) => {
          rec_movie_list = data.list;
          if (rec_movie_list !== "") {
            var parentDiv = document.getElementById("recommended-movies");
            try {
              var childDivs = parentDiv.getElementsByClassName("movie");
              while (childDivs.length > 0) {
                childDivs[0].remove();
              }
            } catch (error) {
              // Code to handle the exception
              console.error("An error occurred:", error.message);
            }
            const recommendationLableDiv =
              document.getElementById("movie-search-title");
            recommendationLableDiv.innerHTML = `
            <h1 class="h3 mb-0 text-gray-800">Movies matching to your search..</h1>`;
            for (let i = 0; i < Object.entries(rec_movie_list).length; i++) {
              const movieDiv = document.createElement("div");
              movieDiv.classList.add("movie");
              imdb_url =
                "https://www.imdb.com/title/" + rec_movie_list[i]["imdb_id"];
              movieDiv.innerHTML = `
              <a href=${imdb_url} target="_blank" class="btn btn-light btn-icon-split">
                                        <span class="icon text-gray-600">
                                            <i class="fas fa-arrow-right"></i>
                                        </span>
                                        <span class="text">${rec_movie_list[i]["title"]}</span>
              </a>
                              `;
              recommendMovie.appendChild(movieDiv);
            }
          }
        });
    } else {
      alert("Please select an option before submitting the form.");
    }
  });
});
