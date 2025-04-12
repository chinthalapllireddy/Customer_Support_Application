function updateDashboard() {
    fetch("/admin/stats")
      .then(res => res.json())
      .then(data => {
        document.getElementById("agent-count").textContent = data.agents_online;
        document.getElementById("chat-count").textContent = data.active_chats;
        document.getElementById("user-count").textContent = data.total_users;
      });
  }
  
  function loadChartData() {
    fetch("/admin/chart_data")
      .then(res => res.json())
      .then(data => {
        const labels = data.map(item => item.agent);
        const counts = data.map(item => item.chat_count);
        const ctx = document.getElementById('agentChart').getContext('2d');
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [{
              label: 'Chats Handled by Agent',
              data: counts,
              backgroundColor: 'rgba(26, 115, 232, 0.5)',
              borderColor: 'rgba(26, 115, 232, 1)',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      });
  }
  
  setInterval(() => {
    updateDashboard();
    loadChartData();
  }, 5000);
  updateDashboard();
  loadChartData();
  