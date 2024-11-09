document.getElementById("user-input").addEventListener("keydown", function(event) {
    // Проверка на Shift + Enter для новой строки
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();  // Предотвращаем перенос строки
      sendMessage();  // Отправляем сообщение
    }
});

async function sendMessage() {
    const inputElement = document.getElementById("user-input");
    const message = inputElement.value.trim();
    if (!message) return;

    // Отображаем сообщение пользователя
    addMessage("user", message);
    inputElement.value = "";
    adjustTextareaHeight();  // Сбрасываем высоту поля ввода

    // Получаем ответ от ИИ
    const response = await getAIResponse(message);

    // Отображаем ответ ИИ
    addMessage("bot", response);
  }

  function addMessage(sender, text) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("div");
    messageElement.className = `message ${sender}`;
    messageElement.textContent = text;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  async function getAIResponse(userMessage) {
  try {
    const response = await fetch("http://localhost:5000/api/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: userMessage })
    });
    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error("Ошибка при получении ответа от ИИ:", error);
    return "Извините, произошла ошибка. Попробуйте еще раз.";
  }
}

  // Функция для автоматической настройки высоты поля ввода
function adjustTextareaHeight() {
    const inputElement = document.getElementById("user-input");
    inputElement.style.height = "auto";  // Сначала сбрасываем высоту
    inputElement.style.height = inputElement.scrollHeight + "px";  // Устанавливаем новую высоту
}

// Автоматически регулируем высоту поля ввода при вводе текста
document.getElementById("user-input").addEventListener("input", adjustTextareaHeight);