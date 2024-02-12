const action_name = "action_hello_world";
// Replace with Public IP address where Rasa server is hosted below
const rasa_server_url = "http://localhost:5005/webhooks/rest/webhook";
// const sender_id = uuidv4();

var userId = document.getElementById("user-id").dataset.userId;
console.log("User ID:", userId);

const sender_id = userId;
