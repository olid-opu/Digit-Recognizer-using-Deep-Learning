from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import torch

from app.model import CNNModel
from app.utils import preprocess_base64_image


app = FastAPI()

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent
MODEL_PATH = ROOT_DIR / "saved_model" / "best_cnn_model.pth"

# Static and templates
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model
model = CNNModel().to(device)
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

model.load_state_dict(torch.load(str(MODEL_PATH), map_location=device))
model.eval()


class ImageData(BaseModel):
    image: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
def predict(data: ImageData):
    try:
        image_array = preprocess_base64_image(data.image)
        image_tensor = torch.from_numpy(image_array).to(device)

        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()

        return JSONResponse({
            "prediction": predicted_class,
            "confidence": round(float(confidence), 4)
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )