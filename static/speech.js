window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();
recognition.interimResults = true; // 실시간으로 결과를 받음
recognition.lang = 'ko-KR'; // 음성 인식 언어를 한국어로 설정

recognition.addEventListener('result', e => {
    const transcript = Array.from(e.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('');

    const p = document.getElementById('transcript');
    p.textContent = transcript;

    if (e.results[0].isFinal) {
        console.log('Final transcript:', transcript);
        // 서버로 전송하는 함수를 호출합니다.
        sendVoiceMessage(transcript);
    }
});

function sendVoiceMessage(transcript) {
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: transcript })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Server response:', data);
        if (data && data.GPT) {
            updateChatWindow(transcript, data.GPT);  // 채팅창 업데이트 함수 호출
            speak(data.GPT); // GPT의 응답을 음성으로 출력
        }
    })
    .catch(error => {
        console.error('Error sending transcript:', error);
    });
}

function updateChatWindow(userMessage, serverMessage) {
    addMessage(userMessage, 'user-message'); // 사용자 메시지 추가
    addMessage(serverMessage, 'assistant-message'); // 서버(GPT) 응답 추가
}

function addMessage(text, className) {
    const messageElement = document.createElement('div');
    messageElement.className = className;
    messageElement.textContent = text;
    const chatBox = document.getElementById('chat-box');
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // 스크롤을 최신 메시지 위치로 이동
}
