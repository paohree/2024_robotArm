// speak.js
function speak(text) {
    if (!window.speechSynthesis) {
        console.error("Browser does not support text-to-speech.");
        return;
    }
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ko-KR';  // 음성 언어 설정 (한국어)
    window.speechSynthesis.speak(utterance);
}
