# 📝 Meeting Notes and Action Item Extractor

A Streamlit web application that automatically transcribes meeting audio and generates concise summaries along with actionable tasks. Users can upload an audio file or provide a YouTube link to process meeting recordings efficiently.

---

## ✨ Features

### 🎙️ Accurate Audio Transcription

* Uses **OpenAI Whisper-1** model
* High-quality speech-to-text conversion
* Supports multiple audio formats

### 🧠 Intelligent Summarization

* Uses GPT model (e.g., GPT-3.5 Turbo)
* Extracts:

  * Key discussion points
  * Decisions
  * Outcomes
* Generates structured meeting summary

### ✅ Action Item Detection

* Automatically identifies tasks discussed in meeting
* Assigns action items to individuals (if mentioned)
* Presents clear and structured task list

### 🔀 Dual Input Methods

#### 📤 File Upload

* Upload audio files directly
* Supported formats: mp3, wav, m4a, etc.

#### 🔗 YouTube URL

* Paste meeting recording link
* Extracts and processes audio automatically

### 💻 User-Friendly Interface

* Clean and simple Streamlit UI
* Easy upload and result viewing
* Structured output for quick review

---

## 🚀 How It Works

The application follows a simple AI pipeline:

### 1️⃣ Audio Input

User provides audio source:

* Upload file
* OR paste YouTube link

### 2️⃣ Audio Processing

* For YouTube links → `pytube` downloads audio stream
* Uploaded files saved temporarily for processing

### 3️⃣ Transcription

* Audio sent to OpenAI Whisper API
* Returns complete text transcript

### 4️⃣ Summarization & Analysis

* Transcript sent to GPT model
* Custom prompt generates:

  * Meeting Summary
  * Action Items

### 5️⃣ Display

* Structured notes displayed in Streamlit UI
* Easy to copy, review, and use

---

## 🛠️ Tech Stack

**Frontend:**

* Streamlit

**AI Services:**

* OpenAI API (Whisper + GPT models)

**YouTube Downloader:**

* Pytube

---

## 📋 Setup and Installation

Follow these steps to run locally.

### 1️⃣ Prerequisites

* Python 3.8+
* OpenAI API key

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/meeting-notes-extractor.git
cd meeting-notes-extractor
```

---

### 3️⃣ Install Dependencies

Create a `requirements.txt` file:

```txt
streamlit
openai
pytube
```

Install packages:

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set Up OpenAI API Key

The app securely reads your API key.

You have two options:

---

## 🔐 Option A: Local Development (Environment Variable)

### macOS/Linux

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Windows (Command Prompt)

```bash
set OPENAI_API_KEY="your-api-key-here"
```

### Windows (PowerShell)

```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

---

## ☁️ Option B: Streamlit Cloud Deployment

Use Streamlit secrets management.

Create file:

```
.streamlit/secrets.toml
```

Add:

```toml
OPENAI_API_KEY = "your-api-key-here"
```

⚠️ Add `.streamlit/secrets.toml` to `.gitignore` to protect API key.

---

## ▶️ Running the Application

Run the Streamlit app:

```bash
streamlit run your_script_name.py
```

Replace `your_script_name.py` with your actual Python filename.

The application will open automatically in your browser.

---

## 📌 Use Cases

* Meeting transcription automation
* Team productivity tools
* Project management support
* Interview and lecture summarization
* AI productivity portfolio project


