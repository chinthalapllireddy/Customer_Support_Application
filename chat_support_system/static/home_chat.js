document.addEventListener("DOMContentLoaded", function () {
    const openBtn = document.getElementById("open-chat-btn");
    const closeBtn = document.getElementById("close-chat-btn");
    const slideChat = document.getElementById("slide-chat");
  
    openBtn.addEventListener("click", () => {
      slideChat.classList.add("active");
    });
  
    closeBtn.addEventListener("click", () => {
      slideChat.classList.remove("active");
    });
  
    // Optionally, handle form submission
    document.getElementById("slide-chat-form").addEventListener("submit", function (e) {
      e.preventDefault();
      const input = document.getElementById("slide-chat-input");
      const msg = input.value.trim();
      if (msg) {
        // Append message to the chat box (basic demo)
        const chatBox = document.getElementById("slide-chat-box");
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("chat-message");
        msgDiv.innerHTML = `<strong>You:</strong> ${msg}`;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        input.value = "";
        // Here you can send the message to the server with fetch or WebSocket
      }
    });
  });
  