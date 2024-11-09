const userInput = document.getElementById('user-input');

redirectUser();

// Увеличиваем высоту на Shift+Enter
userInput?.addEventListener("keydown", function(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
}
}, false);

// Увеличиваем высоту на Shift+Enter
userInput?.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && event.shiftKey) {
        adjustTextareaHeight();
    }
}, false);

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

//все очень плохо
async function redirectUser() {
  const sessionId = getSessionId();
  try {
    const responseHTML = await fetch("http://localhost:8000/", {
      method: "GET",
      body: sessionId
    });
    // window.location.replace(responseHTML);
    // const responseSTR = await fetch("http://localhost:8000/с/sessionId", {
    //   method: "GET"
    // });
    // parser(responseSTR)

  } catch (error) {
    console.error("Ошибка при получении ответа от ИИ:", error); // фигня дебаг
    return "Извините, произошла ошибка. Попробуйте еще раз.";
  }
}

// async function parse_history(){
//   const sessionId = getSessionId();

//   try {
//     const responseHTML = await fetch("http://localhost:8000/с/sessionId", {
//       method: "GET"
//     });
//     window.location.replace(responseHTML);
//     const responseSTR = await fetch("http://localhost:8000/с/sessionId", {
//       method: "GET"
//     });
//     parser(responseSTR)

//   } catch (error) {
//     console.error("Ошибка при получении ответа от ИИ:", error); // фигня дебаг
//     return "Извините, произошла ошибка. Попробуйте еще раз.";
//   }
// }

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
  userInput?.addEventListener("input", adjustTextareaHeight());
  // Обработка нажатия клавиш в поле ввода
  userInput?.addEventListener('keydown', function(e) {
    console.log("hui");
    if (e.key === 'Enter') {
        if (e.shiftKey) {
            // Если нажаты Shift + Enter, добавляем перенос строки и увеличиваем высоту поля
            e.preventDefault();
            userInput.value += '\n';
            adjustTextareaHeight();
        } else {
            // Если только Enter, отправляем сообщение
            e.preventDefault();
            sendMessage();
        }
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
