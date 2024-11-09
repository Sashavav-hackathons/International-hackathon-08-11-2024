const userInput = document.getElementById('user-input');

// Обработка события ввода
// userInput?.addEventListener("keydown", function(event) {
//     console.error("хуй");
//     if (event.key === 'Enter' && !event.shiftKey) {
//         event.preventDefault();
//         sendMessage();
//     }
// });

// Увеличиваем высоту на Shift+Enter
userInput?.addEventListener("keypress", function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        adjustTextareaHeight();
    }
}, false);
// Обработка события ввода
// userInput.addEventListener('keypress', function(event) {
//     if (event.key === 'Enter' && !event.shiftKey) {
//         event.preventDefault();
//         sendMessage();
//     }
// });

// // Увеличиваем высоту на Shift+Enter
// userInput.addEventListener('keydown', function(event) {
//     if (event.key === 'Enter' && event.shiftKey) {
//         adjustTextareaHeight();
//     }
// });

function sendMessage() {
    const inputElement = document.getElementById("user-input");
    const messageText = inputElement.value.trim();
    if (messageText === "") return;

    appendMessage(messageText, 'user-message');
    inputElement.value = '';
    resetTextareaHeight(); // Сбрасываем высоту после отправки

    // Симулируем ответ от бота
    getAIResponse(messageText).then(response => {
        appendMessage(response, 'bot-message');
    });
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

function appendMessage(text, className) {
    const chatBox = document.getElementById('chat-box');
    const message = document.createElement('div');
    message.className = 'message ' + className;
    message.textContent = text;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Функция для динамического изменения высоты поля ввода
function adjustTextareaHeight() {
  const inputElement = document.getElementById("user-input");
  inputElement.style.height = "auto";
  inputElement.style.height = inputElement.scrollHeight + "px";
}

// Сброс высоты поля ввода после отправки сообщения
function resetTextareaHeight() {
  const inputElement = document.getElementById("user-input");
  inputElement.style.height = "auto";
}
