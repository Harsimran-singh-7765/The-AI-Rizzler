from flask import Flask, render_template, request, jsonify
import os
import tempfile
from PIL import Image
from io import BytesIO
from google import genai
from dotenv import load_dotenv
from google.generativeai import configure
from crewai import Agent, Task, Crew, LLM
from flask_cors import CORS
import base64

# Load environment variables
load_dotenv(dotenv_path=r".env")
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
configure(api_key=os.environ["GEMINI_API_KEY"])

# Initialize the LLM client and configure the API key for Google Gemini
llm = LLM(model="gemini/gemini-1.5-flash")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Max file size 10 MB
app.config['UPLOAD_FOLDER'] = 'uploads'  # Set upload folder
CORS(app)  # Enable CORS for cross-origin requests

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to generate a description for the uploaded image
def get_frame_description(frame):
    try:
        # Save image directly to a file
        img_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image.png')
        frame.save(img_filename)

        print("We are trying to get description.")

        # Prepare the request to Gemini API
        contents = [
            {"text": "Can you describe the contents of the following image? make the disciption detailed and personlised"},
            {
                "inline_data": {
                    "mime_type": "image/png",
                    "data": open(img_filename, "rb").read()
                }
            }
        ]
        
        # Make a request to Gemini API to generate content (description)
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=contents,
            config=genai.types.GenerateContentConfig(
                response_modalities=["Text", "Image"]
            )
        )

        print(f"API response: {response}")

        description = "No description generated."
        
        # Parse the API response
        for part in response.candidates[0].content.parts:
            if part.text:
                description = part.text
            elif part.inline_data:
                image_data = part.inline_data.data
                if image_data:
                    try:
                        image = Image.open(BytesIO(image_data))
                        image.show()  # Display the image if generated
                        description = "An image has been generated and displayed."
                    except Exception as e:
                        print(f"Error processing generated image: {e}")
                        description = "Error displaying the generated image."
                else:
                    print("Received image data is None.")
                    description = "No image generated."

        return description
    except Exception as e:
        print(f"Error in image description generation: {e}")
        return "Unable to generate description."


# Function to generate AI comment based on the description
def get_ai_comment(description):
    try:
        # Create an AI agent to generate the comment
        agent = Agent(
            role="Webcam Rizzler",
            goal="Give flirty and fun comments based on the webcam scene."
            "the comment should be according to the {description} and should be personlized",
            backstory="You are a flirty 18+ AI who watches a webcam and gives witty feedback every few seconds.",
            verbose=True,
            llm=llm
        )

        task = Task(
            description=f"The webcam shows: {description}\nGive a short, fun, human-like comment.",
            expected_output="A casual sentence like a friend talking to the user.",
            agent=agent
        )

        # Execute the task using Crew (task orchestration)
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        return result.raw
    except Exception as e:
        print(f"Error generating comment: {e}")
        return "Unable to generate comment."


# Route to handle the homepage
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle the image capture and processing via POST request
@app.route('/capture', methods=['POST'])
def capture():
    try:
        print("Request received")
        
        # Get the image data from the request
        image_data = request.json['image_data']

        # Validate image data
        if not image_data:
            raise ValueError("No image data received")

        # Remove the base64 header part
        image_data = image_data.split(',')[1]

        # Decode the base64 string into image bytes
        image_bytes = base64.b64decode(image_data)
        print("Image bytes received successfully.")

        # Save the image to a file
        img_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image.png')
        with open(img_filename, 'wb') as img_file:
            img_file.write(image_bytes)

        # Process the image and generate description and comment
        image = Image.open(img_filename)
        description = get_frame_description(image)
        comment = get_ai_comment(description)
        
        return jsonify({"description": description, "comment": comment})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
