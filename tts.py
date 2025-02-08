from flask import Flask, render_template, request, url_for
from PIL import Image
import io
import base64
from gtts import gTTS
import pytesseract as pt
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    extracted_text = None
    audio_file_url = None

    if request.method == "POST":
        if "file" in request.files:  # File upload
            uploaded_file = request.files["file"]
            if uploaded_file:
                try:
                    img = Image.open(uploaded_file)
                    extracted_text = extract_text(img)
                    print(f"Extracted text: {extracted_text}")
                    if extracted_text.strip():
                        audio_file_url = text_to_speech(extracted_text)
                except Exception as e:
                    print(f"Error processing uploaded file: {e}")
        if "capturedImage" in request.form: 
            captured_image_data = request.form["capturedImage"]
            if captured_image_data:
                try:
                    # Decode the base64 image data
                    image_data = base64.b64decode(captured_image_data.split(",")[1])
                    img = Image.open(io.BytesIO(image_data))

                    # Save the decoded image for debugging (temporary)
                    debug_image_path = "static/debug_captured_image.png"
                    img.save(debug_image_path)
                    print(f"Decoded image saved at {debug_image_path}")

                    # Extract text from the image
                    extracted_text = extract_text(img)
                    print(f"Extracted text: {extracted_text}")

                    # Convert extracted text to speech
                    if extracted_text.strip():  # Ensure text is not empty
                        audio_file_url = text_to_speech(extracted_text)
                    else:
                        print("No text detected in the image.")
                except Exception as e:
                    print(f"Error processing captured image: {e}")

    return render_template("app.html", ext_text=extracted_text, audio_file_url=audio_file_url)


@app.route("/scanner")
def scanner():
    return render_template("scanner.html")

def extract_text(image):
    try:
        text = pt.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting text with pytesseract: {e}")
        return "Error extracting text."

def text_to_speech(text):
    try:
        audio_file = os.path.join('static', 'audio.mp3')
        tts = gTTS(text)
        tts.save(audio_file)
        return url_for('static', filename='audio.mp3')
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

if __name__ == "__main__":
    app.run(debug=True)
