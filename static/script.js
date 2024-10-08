function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (!userInput.trim()) return; // 사용자 입력이 비어 있으면 아무것도 하지 않음

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok'); // 네트워크 응답 실패 처리
        }
        return response.json();
    })
    .then(data => {
        if (data && data.GPT) { // 응답 데이터 검사
            const chatBox = document.getElementById('chat-box');
            addMessage(userInput, 'user-message'); // 사용자 메시지 추가
            addMessage(data.GPT, 'assistant-message'); // GPT 응답 추가
            document.getElementById('userInput').value = ''; // 입력 필드 초기화
            chatBox.scrollTop = chatBox.scrollHeight; // 스크롤 자동화
            speak(data.GPT); // GPT의 응답을 음성으로 출력
        } else {
            console.error('Invalid data:', data);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error); // 오류 로깅
        alert('An error occurred, please try again later.'); // 사용자에게 오류 알림
    });
}


function addMessage(text, className) {
    const messageElement = document.createElement('div');
    messageElement.className = className;
    messageElement.textContent = text;
    const chatBox = document.getElementById('chat-box');
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // 항상 새 메시지가 보이도록 스크롤
}

