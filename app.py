import streamlit as st
import openai
import os
from pytube import YouTube

# --- Configuration ---
# It's recommended to set the API key as an environment variable for security.
# You can also hardcode it here for simplicity, but be careful with sharing your code.
# Example: openai.api_key = "YOUR_OPENAI_API_KEY"
openai.api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

# --- Helper Functions ---

def transcribe_audio(file_path):
    """
    Transcribes the audio file using OpenAI's Whisper API.
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
              model="whisper-1",
              file=audio_file
            )
        return transcript.text
    except Exception as e:
        st.error(f"Error in transcription: {e}")
        return None

def extract_notes_and_actions(transcript_text):
    """
    Uses a GPT model to extract structured notes and action items from the transcript.
    """
    if not transcript_text:
        return "", ""

    # This prompt guides the model to produce the desired output format.
    prompt = f"""
    You are a professional meeting assistant. Your task is to analyze the following meeting transcript and produce two things:
    1. A concise, easy-to-read summary of the meeting's key discussion points, decisions, and outcomes. Use bullet points.
    2. A list of all action items mentioned, clearly assigning each item to a person if mentioned.

    Here is the transcript:
    ---
    {transcript_text}
    ---

    Please format your output clearly with "Meeting Summary" and "Action Items" as headings.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-16k",  # Or "gpt-4" for higher quality results
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in summarizing meeting transcripts."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error in extracting notes: {e}")
        return ""

def download_youtube_audio(url):
    """
    Downloads the audio from a YouTube URL and saves it as 'youtube_audio.mp4'.
    """
    try:
        yt = YouTube(url)
        # Select the best audio-only stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            st.error("No audio-only stream found for this video.")
            return None
            
        output_path = "temp_audio"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        file_path = audio_stream.download(output_path=output_path, filename="youtube_audio.mp4")
        return file_path
    except Exception as e:
        st.error(f"Failed to download YouTube audio: {e}")
        return None


# --- Streamlit UI ---

st.set_page_config(page_title="Meeting Notes Extractor", layout="wide", page_icon="🎙️")

st.title("🎙️ Meeting Notes and Action Item Extractor")
st.markdown("Convert meeting audio into structured notes and task lists. Upload an audio file or provide a YouTube link.")

# Check for API key
if not openai.api_key:
    st.error("OpenAI API key not found! Please set it as an environment variable or in st.secrets.")
else:
    # Use tabs for different input methods
    tab1, tab2 = st.tabs(["📤 Upload Audio File", "🔗 Use YouTube URL"])

    with tab1:
        uploaded_file = st.file_uploader(
            "Choose an audio file (MP3, WAV, M4A...)",
            type=['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']
        )

        if uploaded_file is not None:
            st.audio(uploaded_file, format='audio/wav')
            
            # Save uploaded file temporarily to process it
            file_path = os.path.join("temp_audio", uploaded_file.name)
            os.makedirs("temp_audio", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            if st.button("Generate Notes from Uploaded File"):
                with st.spinner("Transcribing audio... This may take a moment. ⏳"):
                    transcript = transcribe_audio(file_path)

                if transcript:
                    st.success("Transcription complete! ✅")
                    with st.spinner("Extracting notes and action items... 🧠"):
                        notes = extract_notes_and_actions(transcript)
                        st.markdown("---")
                        st.markdown(notes)
                    # Clean up the temporary file
                    os.remove(file_path)

    with tab2:
        youtube_url = st.text_input("Enter the YouTube URL of the meeting recording:")

        if st.button("Generate Notes from YouTube URL"):
            if youtube_url:
                with st.spinner("Downloading audio from YouTube... 📥"):
                    audio_file_path = download_youtube_audio(youtube_url)
                
                if audio_file_path:
                    st.success("Audio downloaded successfully! ✅")
                    with st.spinner("Transcribing audio... This may take a moment. ⏳"):
                        transcript = transcribe_audio(audio_file_path)
                    
                    if transcript:
                        st.success("Transcription complete! ✅")
                        with st.spinner("Extracting notes and action items... 🧠"):
                            notes = extract_notes_and_actions(transcript)
                            st.markdown("---")
                            st.markdown(notes)
                        # Clean up the downloaded audio file
                        os.remove(audio_file_path)
            else:
                st.warning("Please enter a valid YouTube URL.")
