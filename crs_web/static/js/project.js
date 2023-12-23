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

var recURL =
  "http://" + window.location.host + "/movie/ajax/content-recommend-movies/";
var recCollabCSi2iURL =
  "http://" +
  window.location.host +
  "/movie/ajax/collab-recommend-i2i-cosine-similarity/";
var recCollabCSu2uURL =
  "http://" +
  window.location.host +
  "/movie/ajax/collab-recommend-u2u-cosine-similarity/";
var topTrendingURL =
  "http://" + window.location.host + "/movie/ajax/top-trending-movies?genre=";

document.addEventListener("DOMContentLoaded", function () {
  const messageInput = document.getElementById("message-input");
  const sendButton = document.getElementById("send-button");
  const chatMessages = document.querySelector(".chat-messages");
  const recommendButton = document.getElementById("recommend-button");
  const recommendMovie = document.getElementById("recommended-movies");
  const topTrendingButton = document.getElementById("top-trending-button");
  const topTrendingMovies = document.getElementById("top-trending-movies");
  const recommendCollabCSi2iButton = document.getElementById(
    "recommend-collab-cs-i2i-button"
  );
  const recommendCollabCSi2iSMovie = document.getElementById(
    "recommended-collab-cs-i2i-movies"
  );
  const recommendCollabCSu2uButton = document.getElementById(
    "recommend-collab-cs-u2u-button"
  );
  const recommendCollabCSu2uSMovie = document.getElementById(
    "recommended-collab-cs-u2u-movies"
  );
  const watchedMovies = document.getElementById("watched-movies");
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
  //content filtering
  if (recommendButton) {
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
  }
  // Top trending
  if (topTrendingButton) {
    topTrendingButton.addEventListener("click", function (event) {
      const genreInputValue = document.getElementById("genre-input");
      console.log(genreInputValue.value);
      var genreTitle = genreInputValue.value.trim();
      console.log(genreTitle);
      topTrendingURLwithQuery = topTrendingURL + genreTitle;
      console.log(topTrendingURLwithQuery);
      if (genreTitle !== "") {
        fetch(topTrendingURLwithQuery, {
          method: "GET",
          credentials: "same-origin",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFTOKEN": getCookie("csrftoken"),
            "Content-type": "application/json",
          },
        })
          .then((response) => {
            if (!response.ok) {
              // Handle error for status codes outside the 200-299 range
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then((data) => {
            console.log(data);
            top_trending_list = data.movies;
            console.log("in response list");
            console.log(top_trending_list);
            if (top_trending_list) {
              var parentDiv = document.getElementById("top-trending-movies");
              try {
                var childDivs =
                  parentDiv.getElementsByClassName("trending-movie");
                while (childDivs.length > 0) {
                  childDivs[0].remove();
                }
              } catch (error) {
                // Code to handle the exception
                console.error("An error occurred:", error.message);
              }
              const topTrendingDiv =
                document.getElementById("top-trending-title");
              topTrendingDiv.innerHTML = `
              <h2 class="h3 mb-0 text-gray-800">Top 10 trending movies based on weighted ratings in ${genreTitle} ...</h2>`;
              for (
                let i = 0;
                i < Object.entries(top_trending_list).length;
                i++
              ) {
                const movieDiv = document.createElement("div");
                movieDiv.classList.add("trending-movie");
                imdb_url =
                  "https://www.imdb.com/title/" +
                  top_trending_list[i]["imdb_id"];
                movieDiv.innerHTML = `
                <a href=${imdb_url} target="_blank" class="btn btn-light btn-icon-split">
                                          <span class="icon text-gray-600">
                                              <i class="fas fa-arrow-right"></i>
                                          </span>
                                          <span class="text">${
                                            top_trending_list[i]["title"]
                                          }(${top_trending_list[i][
                  "weighted_rating"
                ].toFixed(2)})</span>
                </a>
                                `;
                topTrendingMovies.appendChild(movieDiv);
              }
            } else {
              const topTrendingDiv =
                document.getElementById("top-trending-title");
              topTrendingDiv.innerHTML = `
              <h2 class="h3 mb-0 text-gray-800">No movies found</h2>`;
            }
          })
          .catch((error) => {
            // Error handling
            console.error("Fetch error:", error);
          });
      } else {
        alert("Please select an option before submitting the form.");
      }
    });
  }
  //I2I Collaborative filtering with cosine similarity
  if (recommendCollabCSi2iButton) {
    recommendCollabCSi2iButton.addEventListener("click", function (event) {
      const movieInputValue = document.getElementById("movie-input");
      console.log(movieInputValue.value);
      var movieTitle = movieInputValue.value.trim();
      console.log(recCollabCSi2iURL);
      if (movieTitle !== "") {
        fetch(recCollabCSi2iURL, {
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
              var parentDiv = document.getElementById(
                "recommended-collab-cs-i2i-movies"
              );
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
                recommendCollabCSi2iSMovie.appendChild(movieDiv);
              }
            }
          });
      } else {
        alert("Please select an option before submitting the form.");
      }
    });
  }
  //U2U Collaborative filtering with cosine similarity
  if (recommendCollabCSu2uButton) {
    recommendCollabCSu2uButton.addEventListener("click", function (event) {
      const userInputValue = document.getElementById("user-input");
      console.log(userInputValue.value);
      var userId = userInputValue.value.trim();
      if (userId !== "") {
        fetch(recCollabCSu2uURL, {
          method: "POST",
          credentials: "same-origin",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFTOKEN": getCookie("csrftoken"),
            "Content-type": "application/json",
          },
          body: JSON.stringify({ user_id: parseInt(userId) }),
        })
          .then((response) => response.json())
          .then((data) => {
            console.log(data);
            watched_list = data.watched_list;
            rec_movie_list = data.recommeded_list;
            if (watched_list !== "") {
              var parentDiv = document.getElementById("watched-movies");
              try {
                var childDivs =
                  parentDiv.getElementsByClassName("watched-movie");
                while (childDivs.length > 0) {
                  childDivs[0].remove();
                }
              } catch (error) {
                // Code to handle the exception
                console.error("An error occurred:", error.message);
              }

              const watchLableDiv = document.getElementById(
                "movie-watched-title"
              );
              watchLableDiv.innerHTML = `
              <h1 class="h3 mb-0 text-gray-800">Movies watched by ${userId}.</h1>`;
              for (let i = 0; i < 5; i++) {
                const watchedMovieDiv = document.createElement("div");
                watchedMovieDiv.classList.add("watched-movie");
                imdb_url =
                  "https://www.imdb.com/title/" + watched_list[i]["imdb_id"];
                watchedMovieDiv.innerHTML = `
                <a href=${imdb_url} target="_blank" class="btn btn-light btn-icon-split">
                                          <span class="icon text-gray-600">
                                              <i class="fas fa-arrow-right"></i>
                                          </span>
                                          <span class="text">${watched_list[i]["title"]}</span>
                </a>
                                `;
                watchedMovies.appendChild(watchedMovieDiv);
              }
            }

            if (rec_movie_list !== "") {
              var parentDiv = document.getElementById(
                "recommended-collab-cs-u2u-movies"
              );
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
              <h1 class="h3 mb-0 text-gray-800">Movies recommended for this user based on other users..</h1>`;
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
                recommendCollabCSu2uSMovie.appendChild(movieDiv);
              }
            }
          });
      } else {
        alert("Please select an option before submitting the form.");
      }
    });
  }
});
