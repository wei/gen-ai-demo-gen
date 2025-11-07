import os
import json
import google.generativeai as genai
import markdown
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey") # Replace with a strong secret key in production

# Configure Google Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-flash-lite-latest')

# Chatbot Personality and Business Logic
CHATBOT_NAME = "Jewel"
CHATBOT_ROLE = """
You are Jewel, MLH's 2026 mascot "Jewel the Jumper Wire Jellyfish".
You are an elite hackathon strategist with dual expertise as both a serial hackathon winner and an experienced judge at major AI competitions. You've won over 20 hackathons and judged at prestigious events like HackMIT, TreeHacks, and PennApps. Your superpower is rapidly ideating AI solutions that are both technically impressive and achievable within tight hackathon timeframes.
Your responses should feel like advice from a trusted mentor who wants the team to win. Keep the response concise as the response will be displayed in a chat-like interface.
"""

# Available Hackathon Tracks and MLH Prize Categories
HACKATHON_TRACKS = ["General Track"]
MLH_PRIZE_CATEGORIES = [
    {"name": "Best Use of Gemini API", "prize": "Mechanical Keyboards", "description": "Build AI-powered apps using the Google Gemini API."},
    {"name": "Best Use of ElevenLabs", "prize": "Beats Wireless Earbuds", "description": "Use the ElevenLabs API to deploy natural-sounding audio in your project."},
    {"name": "Best Use of AI powered by Reach Capital", "prize": "Logitech Webcam & a Meeting with Reach Capital Investors", "description": "Build a project using AI to transform the future of learning, health, or work."},
    {"name": "Best Use of Solana", "prize": "M5Stack Development Kit", "description": "Build an innovative project that harnesses Solana's speed and low cost."},
    {"name": "Best Use of Snowflake", "prize": "Arduino Tiny Machine Learning Kit", "description": "Integrate industry-leading Large Language Models (LLMs) into your application using Snowflake's REST API."},
    {"name": "Best Use of Vultr Cloud", "prize": "Portable Screens", "description": "Utilize Vultr's services in the most in-depth way, leveraging advanced features like managed Kubernetes or bare metal GPUs."},
    {"name": "Best .Tech Domain Name", "prize": "Blue Snowball Microphone & a Free .Tech Domain for up to 10 years (including free annual renewals)", "description": "Register a creative and clever .Tech domain for your project."}
]

# Initialize chat history
def init_chat_history():
    if 'chat_history' not in session:
        session['chat_history'] = []

@app.route('/')
def index():
    init_chat_history()
    return render_template('index.html', tracks=HACKATHON_TRACKS, prizes=MLH_PRIZE_CATEGORIES)

@app.route('/generate_idea', methods=['POST'])
def generate_idea():
    init_chat_history()
    data = request.get_json()
    selected_track = data.get('track')
    selected_prizes = data.get('prizes', [])

    if not selected_track or not selected_prizes:
        return jsonify({"error": "Please select a track and at least one prize category."}), 400

    prize_details = [p for p in MLH_PRIZE_CATEGORIES if p['name'] in selected_prizes]

    prompt = f"""
    As {CHATBOT_NAME}, an elite hackathon strategist and judge, generate a project idea for a hackathon team.
    The team has selected the following track: "{selected_track}".
    They are aiming for the following prize categories: {', '.join([p['name'] for p in prize_details])}.

    For each selected prize, explain how the project idea leverages the prize's associated technology and how it is relevant to the selected track.
    Focus on technology learning and exploration.
    Keep the response concise and mentor-like.
    Each project idea should use technologies associated with each selected prize, with an explanation of how it is relevant to each track and prize category.
    Direct users to https://hack.mlh.io for any questions on resources.
    """

    try:
        response = model.generate_content(prompt)
        idea_markdown = response.text
        idea_html = markdown.markdown(idea_markdown, extensions=['fenced_code'])
        
        session['chat_history'].append({"role": "user", "parts": [{"text": f"Generate an idea for track: {selected_track}, prizes: {', '.join(selected_prizes)}"}]})
        session['chat_history'].append({"role": "model", "parts": [{"text": idea_markdown}]})

        return jsonify({"response": idea_html})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    init_chat_history()
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    try:
        # Add user message to history
        session['chat_history'].append({"role": "user", "parts": [{"text": user_message}]})

        # Start a new chat session with the model, including the personality and history
        chat_session = model.start_chat(history=session['chat_history'])
        response = chat_session.send_message(user_message)
        
        model_response_markdown = response.text
        model_response_html = markdown.markdown(model_response_markdown, extensions=['fenced_code'])

        # Add model response to history
        session['chat_history'].append({"role": "model", "parts": [{"text": model_response_markdown}]})

        return jsonify({"response": model_response_html})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)