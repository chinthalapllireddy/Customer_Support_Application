document.getElementById("agent-chat-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const messageInput = document.getElementById("agent-message");
    const message = messageInput.value.trim();
    if (message) {
      appendMessage("Agent", message);
      sendMessageToServer("agent", message);
      messageInput.value = "";
    }
  });
  
  function appendMessage(sender, message) {
    const chatBox = document.getElementById("chat-box");
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("chat-message");
    msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
  
  function sendMessageToServer(role, message) {
    fetch("/send_message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role: role, message: message })
    });
  }
  
  setInterval(fetchMessages, 1000);
  
  function fetchMessages() {
    fetch("/get_messages?role=agent")
      .then(res => res.json())
      .then(data => {
        document.getElementById("chat-box").innerHTML = "";
        data.forEach(msg => appendMessage(msg.sender, msg.text));
      });
  }
      