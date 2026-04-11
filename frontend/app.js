function addMessage(text, type) {
  let div = document.createElement("div");
  div.className = "message " + type;
  div.innerText = text;
  document.getElementById("chat-box").appendChild(div);
}

async function sendMessage() {
  let input = document.getElementById("text");
  let text = input.value;

  addMessage(text, "user");
  input.value = "";

  let res = await fetch("http://127.0.0.1:8000/complaint", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: text })
  });

  let data = await res.json();

  addMessage(
    "Category: " + data.ai.category + 
    " | Priority: " + data.ai.priority,
    "bot"
  );
}