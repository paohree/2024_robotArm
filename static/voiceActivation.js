// voiceActivation.js
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();
recognition.continuous = true; // 음성 인식을 지속적으로 실행
recognition.interimResults = true; // 중간 결과를 반환하도록 설정
recognition.lang = 'ko-KR'; // 인식할 언어 설정

let isListeningForCommands = false; // 명령어 감지 상태 초기화

recognition.onresult = function(event) {
    let interimTranscript = ''; // 중간 결과를 저장할 변수
    for (let i = event.resultIndex; i < event.results.length; ++i) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
            const listeningStatus = document.getElementById('listeningStatus');
            listeningStatus.textContent += transcript; // 최종 결과를 표시
            if (transcript.trim().toLowerCase().includes("인디야")) {
                document.getElementById('listeningStatus').textContent = '활성화되었습니다!'; // 상태 메시지를 사용자에게 표시
                document.getElementById('userInput').value = transcript;
                sendMessage();
            }
        } else {
            interimTranscript += transcript;
        }
    }
    // 중간 결과 업데이트
    if (!event.results[0].isFinal) {
        document.getElementById('listeningStatus').textContent = interimTranscript;
    }
};


recognition.onend = function() {
    recognition.start(); // 음성 인식을 지속적으로 유지
};

recognition.onerror = function(event) {
    console.error('음성 인식 오류 발생:', event.error);
};

recognition.start(); // 음성 인식 시작
