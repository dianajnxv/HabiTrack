document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("ai-open-btn");
  const win = document.getElementById("ai-chat-window");
  const closeBtn = document.getElementById("ai-close-chat");
  const send = document.getElementById("chat-send");
  const input = document.getElementById("chat-input");
  const content = document.getElementById("chat-content");
  const csrfToken = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");

  const scrollToBottom = () => {
    content.scrollTop = content.scrollHeight;
  };

  btn.onclick = () => {
    const isHidden = win.style.display === "none" || win.style.display === "";
    win.style.display = isHidden ? "flex" : "none";
    if (isHidden) input.focus();
  };

  closeBtn.onclick = () => {
    win.style.display = "none";
  };

  const sendMessage = async () => {
    const msg = input.value.trim();
    if (!msg) return;

    content.innerHTML += `<div class="msg-user">${msg}</div>`;
    input.value = "";
    scrollToBottom();

    try {
      const response = await fetch("/ai-assistant/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ message: msg }),
      });
      const data = await response.json();

      content.innerHTML += `<div class="msg-ai"><b>AI:</b> ${data.reply}</div>`;
      scrollToBottom();
    } catch (e) {
      content.innerHTML += `<div style="color: red; font-size: 12px;">Connection error...</div>`;
    }
  };

  send.onclick = sendMessage;
  input.onkeypress = (e) => {
    if (e.key === "Enter") sendMessage();
  };
});
