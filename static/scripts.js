const video = document.getElementById('video');
const labelElement = document.getElementById('label');

// Replace with your remote server's URL (e.g., https://your-server.com)
const serverUrl = 'http://feelingai.devopsfor.cloud';

// Access the user's camera
navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((error) => console.error('Error accessing the camera:', error));

// Capture and send frames to the backend
setInterval(() => {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const frameData = canvas.toDataURL('image/jpeg'); // Base64-encoded frame

    // Send the frame to the backend for prediction
    fetch(`${serverUrl}/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ frame: frameData }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.label !== undefined) {
                labelElement.textContent = `Prediction: ${data.label}`;
            } else if (data.error) {
                console.error('Error:', data.error);
            }
        })
        .catch((error) => console.error('Error:', error));
}, 1000); // Send a frame every second
