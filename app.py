import streamlit as st
import yt_dlp
import os

# 1. Glassmorphism UI & Custom Styling
st.set_page_config(page_title="Media Downloader", page_icon="✨")

st.markdown("""
    <style>
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Frosted Glass Container */
    .main .block-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 3rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-top: 2rem;
    }
    
    /* Text Styling */
    h1, p, label {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ Ethereal Media Downloader")
st.write("Extract ultra-high-quality audio and video seamlessly.")

# 2. The User Interface
url = st.text_input("Drop your link here (YouTube, TikTok, Instagram):")
format_choice = st.radio("Select your format:", ["Audio Only (m4a)", "Video (mp4)"])

if st.button("Generate Download Link"):
    if url:
        with st.spinner("Weaving the magic... this might take a moment!"):
            # Setup temporary filenames so we know exactly what to hand to the browser
            temp_file = "temp_media.m4a" if "Audio" in format_choice else "temp_media.mp4"
            
            # Delete old temp file if it exists
            if os.path.exists(temp_file):
                os.remove(temp_file)

            if "Audio" in format_choice:
                ydl_opts = {
                    'format': 'ba[ext=m4a]',
                    'outtmpl': temp_file, 
                }
            else:
                ydl_opts = {
                    'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best',
                    'outtmpl': temp_file,
                }
            
            # Execute the yt-dlp download to the server first
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # 3. Hand the file to the Web Browser!
                with open(temp_file, "rb") as file:
                    btn = st.download_button(
                        label="⬇️ Click here to save to your laptop!",
                        data=file,
                        file_name=f"Ethereal_Download.{temp_file.split('.')[-1]}",
                        mime=f"video/mp4" if "Video" in format_choice else "audio/mp4"
                    )
                st.success("Ready! Click the button above to download.")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL first.")