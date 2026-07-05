(function () {
  const apiUrl = window.RestaurantChatbotApi || "/chat";

  const style = document.createElement("style");
  style.textContent = `
    .restaurant-chatbot-button {
      position: fixed;
      right: 20px;
      bottom: 20px;
      z-index: 9999;
      width: 58px;
      height: 58px;
      border: 0;
      border-radius: 50%;
      background: #1f4d3a;
      color: white;
      font: 700 24px Arial, sans-serif;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.22);
      cursor: pointer;
    }

    .restaurant-chatbot-panel {
      position: fixed;
      right: 20px;
      bottom: 92px;
      z-index: 9999;
      width: min(360px, calc(100vw - 40px));
      height: 480px;
      max-height: calc(100vh - 124px);
      display: none;
      flex-direction: column;
      overflow: hidden;
      border: 1px solid #d8ddd7;
      border-radius: 8px;
      background: #fffdf8;
      box-shadow: 0 18px 45px rgba(0, 0, 0, 0.2);
      font: 15px Arial, sans-serif;
    }

    .restaurant-chatbot-panel.is-open {
      display: flex;
    }

    .restaurant-chatbot-header {
      padding: 14px 16px;
      background: #1f4d3a;
      color: white;
      font-weight: 700;
    }

    .restaurant-chatbot-messages {
      flex: 1;
      padding: 14px;
      overflow-y: auto;
    }

    .restaurant-chatbot-message {
      max-width: 82%;
      margin: 0 0 10px;
      padding: 10px 12px;
      border-radius: 8px;
      line-height: 1.35;
    }

    .restaurant-chatbot-message.bot {
      background: #eef3ee;
      color: #1e2a24;
    }

    .restaurant-chatbot-message.user {
      margin-left: auto;
      background: #b9472f;
      color: white;
    }

    .restaurant-chatbot-form {
      display: flex;
      gap: 8px;
      padding: 12px;
      border-top: 1px solid #e5e2dc;
      background: white;
    }

    .restaurant-chatbot-input {
      min-width: 0;
      flex: 1;
      padding: 10px;
      border: 1px solid #c9cec8;
      border-radius: 6px;
      font: inherit;
    }

    .restaurant-chatbot-send {
      border: 0;
      border-radius: 6px;
      padding: 0 14px;
      background: #1f4d3a;
      color: white;
      font-weight: 700;
      cursor: pointer;
    }
  `;
  document.head.appendChild(style);

  const button = document.createElement("button");
  button.className = "restaurant-chatbot-button";
  button.type = "button";
  button.textContent = "?";
  button.setAttribute("aria-label", "Open restaurant chat");

  const panel = document.createElement("section");
  panel.className = "restaurant-chatbot-panel";
  panel.innerHTML = `
    <div class="restaurant-chatbot-header">Ask 123Burger</div>
    <div class="restaurant-chatbot-messages"></div>
    <form class="restaurant-chatbot-form">
      <input class="restaurant-chatbot-input" name="message" placeholder="Ask about hours, burgers..." autocomplete="off">
      <button class="restaurant-chatbot-send" type="submit">Send</button>
    </form>
  `;

  document.body.appendChild(panel);
  document.body.appendChild(button);

  const messages = panel.querySelector(".restaurant-chatbot-messages");
  const form = panel.querySelector(".restaurant-chatbot-form");
  const input = panel.querySelector(".restaurant-chatbot-input");

  function addMessage(text, who) {
    const message = document.createElement("div");
    message.className = `restaurant-chatbot-message ${who}`;
    message.textContent = text;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
  }

  button.addEventListener("click", () => {
    panel.classList.toggle("is-open");
    if (messages.children.length === 0) {
      addMessage("Hi! I can help with hours, burgers, chicken, fries, shakes, pickup, and more.", "bot");
    }
    input.focus();
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });
      const data = await response.json();
      addMessage(data.answer || "Sorry, I could not answer that.", "bot");
    } catch (error) {
      addMessage("I cannot reach the chatbot right now. Please try again later.", "bot");
    }
  });
})();
