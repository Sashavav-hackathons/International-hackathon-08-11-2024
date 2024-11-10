
// function insertNewLine() {
//   // Добавляем перенос строки в текущее положение курсора
//   const cursorPosition = userInput.selectionStart;
//   const text = userInput.value;
//   userInput.value = text.slice(0, cursorPosition) + '\n' + text.slice(cursorPosition);
//   userInput.selectionStart = userInput.selectionEnd = cursorPosition + 1;
//   adjustTextareaHeight(); // Увеличиваем высоту текстового поля
// }

//
function sendMessage() {
    const inputElement = document.getElementById("user-input");
    const messageText = inputElement.value.trim();
    const sessionId = getSessionId();

    if (messageText === "") return;

    appendMessage(messageText, 'user-message');
    inputElement.value = '';
    resetTextareaHeight(); // Сбрасываем высоту после отправки

    // Симулируем ответ от бота
    getAIResponse(messageText, sessionId).then(response => {
        appendMessage(response, 'bot-message');
    });
}

// Генерируем и сохраняем номер сессии
function generateSessionId() {
  const sessionId = crypto.randomUUID(); // Уникальный идентификатор
  localStorage.setItem('sessionId', sessionId);
  console.log(sessionId)
  return sessionId;
}

// Получаем номер сессии, если он уже есть, или создаём новый
function getSessionId() {
  let sessionId = localStorage.getItem('sessionId');
  // console.log(sessionId);
  if (!sessionId) {
      sessionId = generateSessionId();
  }
  return sessionId;
}

// Отображаем номер сессии на странице
function displaySessionId() {
  const sessionId = getSessionId();
  const session = document.getElementById("session-id")
  if (session){
    session.textContent = `Сессия: ${sessionId}`;
  }
  // session.textContent = `Сессия: ${sessionId}`;
}

function parser(inputString) {
  let to_parse = inputString.split('\n\n\n\n\n');
  let flag = 'bot-message'
  to_parse.forEach(element => {
    appendMessage(element, flag);
    if (flag === 'bot-message') flag = 'user-message';
    else flag = 'bot-message';
  });

}

document.addEventListener('DOMContentLoaded', () => {
  displaySessionId(); // Отображаем номер сессии при загрузке страницы
  const userInput = document.getElementById('user-input');
  userInput?.addEventListener("input", adjustTextareaHeight);

  userInput.addEventListener('keydown', function(e) {
    // Проверка нажатия клавиш для Enter и Shift + Enter
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();

    } else if (e.key === "Enter") {
      e.preventDefault(); // предотвращаем стандартное поведение Enter
      insertNewLine();
    }
  
  function insertNewLine() {
    // Добавляем перенос строки в текущее положение курсора
    const cursorPosition = userInput.selectionStart;
    const text = userInput.value;
    userInput.value = text.slice(0, cursorPosition) + '\n' + text.slice(cursorPosition);
    userInput.selectionStart = userInput.selectionEnd = cursorPosition + 1;
    adjustTextareaHeight(); // Увеличиваем высоту текстового поля
  }

});
});

async function getAIResponse(userMessage, sessionID) {
  try {
    const response = await fetch("http://localhost:8000/api/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ 
        message: userMessage,
        id: sessionID
      })
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
