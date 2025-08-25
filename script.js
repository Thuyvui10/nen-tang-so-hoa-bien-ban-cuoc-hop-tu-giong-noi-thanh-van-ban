let mediaRecorder;
let audioChunks = [];

document.addEventListener("DOMContentLoaded", () => {
    const startBtn = document.getElementById("startBtn");
    const stopBtn = document.getElementById("stopBtn");
    const resultDiv = document.getElementById("result");

    startBtn.addEventListener("click", async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const formData = new FormData();
            formData.append("audio", audioBlob, "recording.wav");

            resultDiv.innerText = "⏳ Đang xử lý...";

            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });
            const data = await response.json();
            resultDiv.innerText = data.text || "Không nhận diện được.";
        };

        mediaRecorder.start();
        startBtn.disabled = true;
        stopBtn.disabled = false;
        resultDiv.innerText = "🔴 Đang ghi âm...";
    });

    stopBtn.addEventListener("click", () => {
        mediaRecorder.stop();
        startBtn.disabled = false;
        stopBtn.disabled = true;
    });
});
