const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const predictBtn = document.getElementById("predictBtn");
const clearBtn = document.getElementById("clearBtn");

const predictionText = document.getElementById("predictionText");
const confidenceText = document.getElementById("confidenceText");

// Fill canvas black initially
ctx.fillStyle = "black";
ctx.fillRect(0, 0, canvas.width, canvas.height);

// Drawing settings
let drawing = false;
ctx.strokeStyle = "white";
ctx.lineWidth = 18;
ctx.lineCap = "round";

// Mouse events
canvas.addEventListener("mousedown", () => {
    drawing = true;
    ctx.beginPath();
});

canvas.addEventListener("mouseup", () => {
    drawing = false;
});

canvas.addEventListener("mouseleave", () => {
    drawing = false;
});

canvas.addEventListener("mousemove", draw);

// Touch events for mobile
canvas.addEventListener("touchstart", (e) => {
    e.preventDefault();
    drawing = true;
    ctx.beginPath();
});

canvas.addEventListener("touchend", (e) => {
    e.preventDefault();
    drawing = false;
});

canvas.addEventListener("touchmove", (e) => {
    e.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const touch = e.touches[0];
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;

    if (!drawing) return;

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
});

function draw(e) {
    if (!drawing) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

// Clear canvas
clearBtn.addEventListener("click", () => {
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    predictionText.textContent = "Prediction: -";
    confidenceText.textContent = "Confidence: -";
});

// Predict
predictBtn.addEventListener("click", async () => {
    const imageData = canvas.toDataURL("image/png");

    predictBtn.disabled = true;
    predictionText.textContent = "Prediction: ...";
    confidenceText.textContent = "Confidence: ...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ image: imageData })
        });

        let result = null;
        try {
            result = await response.json();
        } catch {
            result = { error: "Invalid server response" };
        }

        if (!response.ok || result.error) {
            predictionText.textContent = "Prediction: Error";
            confidenceText.textContent = result.error || `HTTP ${response.status}`;
            return;
        }

        predictionText.textContent = `Prediction: ${result.prediction}`;
        confidenceText.textContent = `Confidence: ${(result.confidence * 100).toFixed(2)}%`;
    } catch (error) {
        predictionText.textContent = "Prediction: Error";
        confidenceText.textContent = "Network/server error";
        console.error(error);
    } finally {
        predictBtn.disabled = false;
    }
});