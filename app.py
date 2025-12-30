import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from tavily import TavilyClient

load_dotenv()

# Configure API Keys.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# print("OK")
# Select the model(s)
MODEL_INFO = "gemini-2.0-flash"
MODEL_SCRIPT = "gemini-2.0-flash"


st.set_page_config(
    page_title="Story Forge Agent",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.title("🤖 Story Forge Agent")


# --- Custom CSS ---
st.markdown("""
<style>
/* App background and fonts */
.stApp {
    background-color: #BAB86C;  /* soft olive green */
    color: #111827;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Main container width */
.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Headings */
h1, h2, h3, h4 {
    color: #ffffff;
    letter-spacing: 0.03em;
}

/* Card-style boxes */
.card {
    background: rgba(15, 23, 42, 0.95);
    border-radius: 18px;
    padding: 1.5rem 1.75rem;
    border: 1px solid rgba(148, 163, 184, 0.35);
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(16px);
    margin-bottom: 1.5rem;
}

/* Accent tag / pill */
.pill {
    display: inline-flex;
    align-items: center;
    padding: 0.18rem 0.7rem;
    border-radius: 999px;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    background: rgba(59, 130, 246, 0.12);
    color: #93c5fd;
    border: 1px solid rgba(59, 130, 246, 0.45);
}

/* Nice buttons */
button[kind="secondary"], button[kind="primary"] {
    border-radius: 999px !important;
    font-weight: 600 !important;
}

/* Links */
a {
    color: #60a5fa;
    text-decoration: none;
}
a:hover {
    color: #bfdbfe;
    text-decoration: underline;
}

/* Bullet lists inside cards */
.card ul {
    padding-left: 1.2rem;
}
.card li {
    margin-bottom: 0.15rem;
}
</style>
""", unsafe_allow_html=True)


def get_realtime_info(query):
    """Searches for current events using the Tavily API."""
    try:
        resp = tavily_client.search(
            query=query,
            max_results=3,
            topic="general"
        )
        if resp and resp.get("results"):
            summaries = []
            for r in resp["results"]:
                title = r.get("title", "")
                url = r.get("url", "")
                snippet = r.get("content","")
                summaries.append(f"Title: {title}\n\nURL: {url}\n\nSummary: {snippet}")
            
            source_info = "\n\n --- \n\n".join(summaries)
        else:
            source_info = f"No recent updates found on '{query}'."

    except Exception as e:
        print(f"Error in get_realtime_info: {e}")
        return None

    # refine and summarize the content via Gemini.

    prompt  = f"""
you are a professional researcher and content creator with experise in multiple fields.  using the following real-time information, 
write an accurate, engaging and human like summary for the topic:'{query}'.

requirements:
- keep it factual, insightful and concise (around 200 words).
- maintain a smooth, natural tone.
- highlight any key takeways and/or trends.
- avoid greetings or self-references.

source informatiion:  {source_info}

output only the refined, human-readable content'
"""
    try:
        model = genai.GenerativeModel(MODEL_INFO)
        response = model.generate_content(prompt)
        return response.text().strip() if response and response.text else source_info
    
    except Exception as e:
        print(f"Error in generating summary: {e}")
        return source_info
    
def generate_video_script(info_text):
    prompt = f"""
You are a creative scriptwriter. 
Turn this real-time information into a compelling video script (for Youtube shorts and/or Instagram reels).
The script should be engaging, informative, and well-structured.  Use a conversational tone with a strong hook and a clear call to action at the end.
The script should be no more than 100 - 120 words.
The script should be in the following format:
- Introduction
- Main content
- Conclusion

Real-time information: {info_text}
"""
    try:
        model = genai.GenerativeModel(MODEL_SCRIPT)
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "No script generated."
    except Exception as e:
        print(f"Error in generating script: {e}")
        return "No script generated."



def main():
    st.markdown("<h1>    StoryForge Agent.</h1>", unsafe_allow_html=True)   
    st.markdown("<p style='text-align: center;>Search any topic-- from world news to research trends -- and get AI-powered insights and video scripts instantly.</p>", unsafe_allow_html=True)


    query = st.text_input("Enter your search query:", "")

    if query:
        with st.spinner("Searching and generating / Gathering latest information ..."):
            info_result = get_realtime_info(query)
            if info_result:
                st.markdown("<h2>Real-time Information</h2>", unsafe_allow_html=True)
                st.subheader("AI generated summary")
                st.markdown(f"<p>{info_result}</p>", unsafe_allow_html=True)
                
                generate_script = st.radio("Generate Video Script", ("No", "Yes"), index=0, horizontal=True)
                if generate_script == "Yes":
                    with st.spinner("Generating video script..."):
                        script = generate_video_script(info_result)

                    if script:
                        st.markdown("<div class == 'card'>", unsafe_allow_html=True)
                        st.subheader("AI generated video script")
                        st.write(script)
                        st.download_button(label="Download Script",data=script, file_name="video_script.txt", mime ='text/plain')
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    else:
                        #st.error("No results found for the given query.")
                        st.warning('Could not generate transcription')
            else:
                st.warning('No valid information found, please try another query')

    st.markdown("<p style='text-align: center;>Powered by Google Gemini and Tavily.</p>", unsafe_allow_html=True)
    st.header("🎥 Author-PRK")


if __name__ == "__main__":
    main()
    


