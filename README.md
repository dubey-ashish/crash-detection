````markdown
#  Vehicle Image Analysis App

This app analyzes four images of a vehicle (front, rear, left, right) using Google's Gemini multimodal model. It evaluates:

- **Image quality** (clarity, lighting, resolution)
- **Structural damage** (dents, scratches, broken parts)
- **License plate** recognition

The results are shown in a clean table using a simple Streamlit interface.

---

##  How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
````

### 2. Add your Gemini API key

Create a `.env` file in the project root with:

```env
API_KEY=your_google_gemini_api_key
```

### 3. Launch the app

```bash
streamlit run ui.py
```

Upload exactly **4 images** when prompted.

---
