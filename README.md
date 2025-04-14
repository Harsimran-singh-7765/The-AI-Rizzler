# 📸 The-AI-Rizzler - Real-time Webcam Flirty Comment Generator

Welcome to **AI Rizzler**, your cheeky AI companion that watches your webcam and throws flirty, witty, and human-like comments based on the live scene. Perfect for adding some spice and fun to your personal webcam interactions, demos, or just for having a laugh.

---

## 🚀 Features

- 🎥 **Live Webcam Access**: Captures real-time video frames from your device camera.
- 🧠 **AI-Powered Description**: Uses Google Gemini Vision API to analyze the image and describe the scene.
- 💬 **Witty Comment Generation**: Personalized, fun comments based on scene description using CrewAI and Google Gemini LLM.
- ⚡ **Interactive UI**: Beautiful frontend with gradient background and stylish buttons.
- 🔒 **Secure**: Handles image processing locally and sends data via base64 with CORS enabled.

---

## 🛠️ Tech Stack

| Technology      | Purpose                            |
|-----------------|------------------------------------|
| **Flask**       | Backend framework (Python)        |
| **Google Gemini** | Vision + LLM API for content generation |
| **CrewAI**      | Agent-based task handling          |
| **HTML/CSS**    | Frontend layout                    |
| **JavaScript**  | Webcam capture and API interaction|
| **Pillow**      | Image processing (Python Imaging Library) |
| **Base64**      | Image encoding for transmission    |
| **dotenv**      | Secure API key management          |

---




## 🗂️ Project Structure  
```
ai-rizzler/
│
├── app.py                 # Flask backend
├── .env                  # Your Gemini API key (ignored by git)
├── uploads/              # Stores temporary image files
├── templates/
│   └── index.html         # Frontend HTML
├── static/               # (Optional if you add custom styles/images)
└── requirements.txt                   # Project documentation
```


---

# ⚙️ How to Run

1. **Clone the repo**
    ```bash
   git clone https://github.com/yourusername/The-AI-Rizzler.git
   cd The-AI-Rizzler
    ```

2. **Install requirements**
    ```bash
    pip install -r requirements.txt
    ```

3. **Create a .env file and add:**
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here

    ```

4. **Run the app:**
    ```bash
    python app.py
    ```

## 🖼️ How it Works

1. **User opens the site**  
   → Grants webcam access when prompted.

2. **User clicks "Capture & Analyze"**  
   → A single frame is captured from the webcam.

3. **Frontend to Backend**  
   → The captured image is converted to Base64 format and sent to the Flask backend via a POST request.

4. **Backend Processing**
   - The image is saved temporarily.
   - It is sent to **Gemini Vision API** to get a natural language **description** of the image.
   - The description is passed to the **CrewAI Agent**, which generates a fun/flirty **comment** based on the image.

5. **Response to Frontend**  
   → The generated comment is returned and displayed to the user in real-time.


## 👤 Author  
**Made with ❤️ by Harsimran Singh**

Feel free to:

- 💫 **Star** this repo if it helped you  
- 🍴 **Fork** it and make it even better  
- 🤝 **Contribute** by raising PRs  
- 👋 Or just say hi and connect!

> “Code hard, dream bigger, and let AI handle the boring stuff!”






## 🚀 About Me
I'm a full stack developer...

