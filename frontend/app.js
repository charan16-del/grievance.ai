function addMessage(text, type) {
  let div = document.createElement("div");
  div.className = type;
  div.style.margin = "5px 0";
  div.style.padding = "8px";
  div.style.borderRadius = "6px";
  div.style.background = type === "user" ? "#22c55e" : "#334155";

  div.innerText = text;

  document.getElementById("chat-box").appendChild(div);
}

async function sendMessage() {
  let input = document.getElementById("text");
  let text = input.value.trim();

  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  try {
    let res = await fetch("https://faithful-kindness-production.up.railway.app/complaint", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    let data = await res.json();

    addMessage(
      `Category: ${data.category} | Priority: ${data.priority}`,
      "bot"
    );

    loadComplaints();

  } catch (err) {
    addMessage("Error connecting to server", "bot");
  }
}

async function loadComplaints() {
  const list = document.getElementById("list");
  list.innerHTML = "Loading...";

  try {
    const res = await fetch("https://faithful-kindness-production.up.railway.app/complaints");
    const data = await res.json();

    let output = "";

    data.forEach(item => {
      let color =
        item.status === "Resolved" ? "#16a34a" :
        item.status === "In Progress" ? "#f59e0b" :
        "#ef4444";

      output += `
        <div class="card">
          <b>${item.text}</b><br>
          Category: ${item.category}<br>
          Priority: ${item.priority}<br>
          Status: <span style="color:${color}">${item.status}</span><br><br>

          <button onclick="updateStatus(${item.id}, 'In Progress')">In Progress</button>
          <button onclick="updateStatus(${item.id}, 'Resolved')">Resolved</button>
        </div>
      `;
    });

    list.innerHTML = output;

  } catch (err) {
    list.innerHTML = "Failed to load complaints";
  }
}

async function updateStatus(id, status) {
  try {
    await fetch(
      `https://faithful-kindness-production.up.railway.app/complaint/${id}?status=${encodeURIComponent(status)}`,
      { method: "PUT" }
    );

    loadComplaints();

  } catch (err) {
    alert("Update failed");
  }
}