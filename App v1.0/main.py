import eel
import os
import logging
from pathlib import Path
from PIL import Image, ImageDraw
from ultralytics import YOLO
import base64
from io import BytesIO

# Logging setup
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    try:

        logging.info("Application starting")

        # Get script directory
        script_dir = Path(__file__).resolve().parent

        # Web folder
        web_dir = script_dir / "web"

        if not web_dir.is_dir():
            raise FileNotFoundError(f"Web folder not found at {web_dir}")

        eel.init(str(web_dir))

        # Load YOLO model
        model_path = script_dir / "weights" / "best.pt"

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")

        model = YOLO(str(model_path))

        logging.info("Model loaded successfully")

        class_names = [
            'elbow positive',
            'fingers positive',
            'forearm fracture',
            'humerus fracture',
            'humerus',
            'shoulder fracture',
            'wrist positive'
        ]

        @eel.expose
        def process_image(image_data_base64):

            logging.info("Processing image")

            try:

                image_data = base64.b64decode(image_data_base64)

                with Image.open(BytesIO(image_data)) as image:

                    results = model(image)

                    processed_image = image.copy()

                    draw = ImageDraw.Draw(processed_image)

                    detections = []

                    recovery_advice = "No fracture detected."

                    recovery_time = "No recovery required."

                    food_recommendation = "Maintain a healthy balanced diet."

                    for result in results:

                        boxes = result.boxes

                        for box in boxes:

                            x1, y1, x2, y2 = box.xyxy[0]

                            conf = float(box.conf[0])

                            cls = int(box.cls[0])

                            fracture_type = class_names[cls]

                            draw.rectangle(
                                [x1, y1, x2, y2],
                                outline="red",
                                width=3
                            )

                            draw.text(
                                (x1, y1 - 10),
                                f"{fracture_type}: {conf:.2f}",
                                fill="red"
                            )

                            detections.append({
                                "class": fracture_type,
                                "confidence": conf
                            })

                            # Recovery advice
                            if "elbow" in fracture_type:
                                recovery_advice = "Use arm sling and avoid lifting heavy objects."
                                recovery_time = "4 - 6 weeks"

                            elif "wrist" in fracture_type:
                                recovery_advice = "Wear wrist splint and avoid pressure on the hand."
                                recovery_time = "4 - 8 weeks"

                            elif "shoulder" in fracture_type:
                                recovery_advice = "Use shoulder immobilizer and limit arm movement."
                                recovery_time = "6 - 12 weeks"

                            elif "forearm" in fracture_type:
                                recovery_advice = "Keep arm in cast and avoid twisting movements."
                                recovery_time = "6 - 8 weeks"

                            elif "fingers" in fracture_type:
                                recovery_advice = "Use finger splint and avoid gripping heavy objects."
                                recovery_time = "3 - 6 weeks"

                            elif "humerus" in fracture_type:
                                recovery_advice = "Use arm brace and limit shoulder movement."
                                recovery_time = "8 - 12 weeks"

                            # Food recommendation
                            food_recommendation = """
Milk and yogurt (Calcium)
Eggs and fish (Protein)
Spinach and broccoli (Vitamin K)
Almonds and nuts
Oranges and citrus fruits (Vitamin C)
Sunlight exposure for Vitamin D
"""

                    buffered = BytesIO()

                    processed_image.save(buffered, format="PNG")

                    processed_image_base64 = base64.b64encode(
                        buffered.getvalue()
                    ).decode()

                    return {
                        "processedImage": processed_image_base64,
                        "detections": detections,
                        "recoveryAdvice": recovery_advice,
                        "recoveryTime": recovery_time,
                        "foodRecommendation": food_recommendation
                    }

            except Exception as e:

                logging.exception("Error processing image")

                return None

        @eel.expose
        def get_class_names():

            return class_names

        eel.start(
            "index.html",
            mode="chrome",
            size=(900, 700)
        )

    except Exception as e:

        logging.exception("Startup error")

        print(f"Error: {e}")


if __name__ == "__main__":

    main()