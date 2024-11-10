let typingInterval;
const typingIndicator = document.createElement('div');
typingIndicator.className = 'message bot-message typing-indicator';
typingIndicator.textContent = 'Печатает';

function showTypingIndicator(isTyping) {
    const chatBox = document.getElementById('chat-box');

    if (isTyping) {
        if (!chatBox.contains(typingIndicator)) {
            chatBox.appendChild(typingIndicator);
            scrollChatToBottom();
        }

        let dots = 0;
        typingInterval = setInterval(() => {
            dots = (dots + 1) % 4;
            typingIndicator.textContent = 'Печатает' + '.'.repeat(dots);
        }, 500);
    } else {
        // Останавливаем анимацию и удаляем индикатор из чата
        clearInterval(typingInterval);
        if (chatBox.contains(typingIndicator)) {
            chatBox.removeChild(typingIndicator);
        }
    }
}

// Функция для прокрутки к последнему сообщению
function scrollChatToBottom() {
    const chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Функция для обработки сообщения пользователя
function sendMessage() {
    const inputElement = document.getElementById("user-input");
    const messageText = inputElement.value.trim();
    const sessionId = getSessionId();

    if (messageText === "") return;

    appendMessage(messageText, 'user-message');
    inputElement.value = '';
    resetTextareaHeight(); // Сбрасываем высоту после отправки

    showTypingIndicator(true);

    getAIResponse(messageText, sessionId).then(response => {
        showTypingIndicator(false);
        appendMessage(response, 'bot-message');
    });
}

// Генерируем и сохраняем номер сессии
function generateSessionId() {
  const sessionId = crypto.randomUUID(); // Уникальный идентификатор
  localStorage.setItem('sessionId', sessionId);
  return sessionId;
}

// Получаем номер сессии, если он уже есть, или создаём новый
function getSessionId() {
  let sessionId = localStorage.getItem('sessionId');
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
}

// Перенаправляем юзера на страницу, где подгружаем его историю
async function redirectUser() {
  const sessionId = getSessionId();
  try {
    const responseHTML = await fetch("http://localhost:8000/", {
      method: "GET",
      body: sessionId
    });

  } catch (error) {
    console.error("Ошибка при получении ответа от ИИ:", error); // фигня дебаг
    return "Извините, произошла ошибка. Попробуйте еще раз.";
  }
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

  userInput?.addEventListener("input", adjustTextareaHeight); // автоформатирование строки пользователя

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

// Функция для получения ответа от ИИ
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

// функция для добавления сообщения в чат
function appendMessage(text, className) {
    const chatBox = document.getElementById('chat-box');
    const message = document.createElement('div');
    message.className = 'message ' + className;

    if (className == "bot-message")
      message.innerHTML = marked.parse(text);
    else
      message.textContent = text;

    // message.textContent = text;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

document.addEventListener("DOMContentLoaded", function() {
  const chatBox = document.getElementById('chat-box');
  const currentUrl = window.location.href;
  const baseUrl = "http://127.0.0.1:8000/c/";

  // Проверяем, содержит ли URL сессию
  if (currentUrl.startsWith(baseUrl)) {
      const sessionId = currentUrl.replace(baseUrl, ""); // Извлекаем uuid из URL

      if (sessionId) {
          // Загружаем историю чата
          showTypingIndicator(true);
          loadChatHistory(sessionId);
          showTypingIndicator(false);
      }
  }
});

async function loadChatHistory(sessionId) {
  try {
    const response = await fetch("http://localhost:8000/", { //пока что хз куда 
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ 
        id: sessionId
      })
    });
    const data = await response.json();
    parser(data.response);
  } catch (error) {
    console.error("Ошибка при получении ответа от ИИ:", error);
    return "Извините, произошла ошибка. Попробуйте еще раз.";
  }
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

function redirectToSession() {
  if (window.location.pathname === '/') {
    // Проверяем, есть ли уже сохранённый session_id в localStorage
    const sessionId = getSessionId();
    // Если session_id найден, перенаправляем на страницу с этим id
    window.location.replace(`${window.location.origin}/c/${sessionId}`);
  }
}

window.onload = redirectToSession;

// console.log(window.location.href)