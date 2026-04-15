# Handwritten Digit Recognizer (CNN + FastAPI)

A full-stack deep learning project that recognizes handwritten digits using a Convolutional Neural Network (CNN) built with PyTorch and deployed via FastAPI. Users can draw a digit (0-9) directly in the browser, and the model predicts the digit in real time.

## Features

- Draw digits on an interactive canvas
- Real-time prediction using a trained CNN model
- FastAPI backend for model inference
- Clean frontend using HTML, CSS, and JavaScript
- End-to-end ML pipeline (training -> deployment -> UI)

## Tech Stack

- Deep Learning: PyTorch
- Backend: FastAPI
- Frontend: HTML, CSS, JavaScript
- Image Processing: Pillow, NumPy

## Project Structure

```text
digit-draw-app/
|
|-- app/
|   |-- main.py
|   |-- model.py
|   |-- utils.py
|   |-- templates/
|   |   `-- index.html
|   `-- static/
|       |-- style.css
|       `-- script.js
|
|-- saved_model/
|   `-- best_cnn_model.pth
|
|-- requirements.txt
`-- README.md
```

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/digit-draw-app.git
cd digit-draw-app
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the environment:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

Open your browser at:

```text
http://127.0.0.1:8000
```

## How It Works

1. User draws a digit on the canvas.
2. Canvas image is sent to FastAPI as base64.
3. Backend preprocesses the image (resize, normalize).
4. CNN model predicts the digit.
5. Prediction is returned and displayed.

## Model

- CNN trained on an MNIST-style dataset
- Input: 28x28 grayscale image
- Output: digit class (0-9)
- Model file: `best_cnn_model.pth`
