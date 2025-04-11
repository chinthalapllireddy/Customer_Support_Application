function updateDashboard() {
    fetch("/admin/stats")
      .then(res => res.json())
      .then(data => {
        document.getElementById("agent-count").textContent = data.agents_online;
        document.getElementById("chat-count").textContent = data.active_chats;
        document.getElementById("user-count").textContent = data.total_users;
      });
  }
  
  // Refresh every 5 seconds
  setInterval(updateDashboard, 5000);
  updateDashboard();
  