from flask import Flask, request, jsonify
from flask_cors import CORS
import pyjokes
import datetime
import math
import random
import os
import webbrowser
import subprocess

app = Flask(__name__)
CORS(app)

# --- Memory system ---
memory = []

# --- Extra data banks ---
quotes = [
    "Believe you can and you’re halfway there.",
    "The harder you work for something, the greater you’ll feel when you achieve it.",
    "Success doesn’t come to you — you go to it.",
    "It always seems impossible until it’s done.",
    "Stay positive, work hard, make it happen."
]

facts = [
    "The first computer mouse was made of wood!",
    "The name Google was accidentally misspelled from 'Googol'.",
    "A group of flamingos is called a flamboyance.",
    "The first hard drive could hold only 5MB of data.",
    "NASA’s internet speed is around 91 Gbps!"
]

# --- Safe math evaluator ---
def safe_eval(expr):
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    try:
        return eval(expr, {"__builtins__": {}}, allowed_names)
    except:
        return None

# --- Helper: open local apps ---
def open_app(command_name):
    apps = {
        "chrome": "/Applications/Google Chrome.app",
        "vscode": "/Applications/Visual Studio Code.app",
        "safari": "/Applications/Safari.app",
        "notes": "/Applications/Notes.app",
        "spotify": "/Applications/Spotify.app",
        "calculator": "/Applications/Calculator.app",
        "finder": "/System/Library/CoreServices/Finder.app"
    }

    if command_name in apps:
        try:
            subprocess.Popen(["open", apps[command_name]])
            return f"Opening {command_name.capitalize()}..."
        except:
            return f"Sorry, I couldn’t open {command_name}."
    else:
        return "App not recognized."


# --- Core AI Logic ---
def generate_response(user_input):
    text = user_input.lower().strip()

    # Greetings
    if any(word in text for word in ["hi", "hello", "hey", "yo", "good morning", "good evening"]):
        return random.choice([
            "Hey there, I’m KRYTEN. What’s up?",
            "Hello human, KRYTEN at your service.",
            "Hi! How can I assist you today?",
            "Hey! Good to see you again."
        ])

    # Time and Date
    elif "time" in text:
        return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
    elif "date" in text:
        return f"Today is {datetime.datetime.now().strftime('%A, %d %B %Y')}."

    # Jokes
    elif "joke" in text:
        return pyjokes.get_joke()

    # Quotes
    elif "motivate" in text or "inspire" in text:
        return random.choice(quotes)

    # Facts
    elif "fact" in text:
        return random.choice(facts)

    # Math
    elif any(op in text for op in ["+", "-", "*", "/", "^"]):
        expression = text.replace("what is", "").replace("calculate", "").strip()
        result = safe_eval(expression)
        return f"The result of {expression} is {result}." if result is not None else "Sorry, that seems invalid."

    # Local Apps
    elif "open" in text:
        if "youtube" in text:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube..."
        elif "google" in text:
            webbrowser.open("https://google.com")
            return "Opening Google..."
        elif "github" in text:
            webbrowser.open("https://github.com")
            return "Opening GitHub..."
        elif "whatsapp" in text:
            webbrowser.open("https://web.whatsapp.com")
            return "Opening WhatsApp Web..."
        elif "chrome" in text:
            return open_app("chrome")
        elif "vscode" in text or "visual studio" in text:
            return open_app("vscode")
        elif "finder" in text or "file" in text:
            return open_app("finder")
        elif "notes" in text:
            return open_app("notes")
        elif "safari" in text:
            return open_app("safari")
        elif "spotify" in text:
            return open_app("spotify")
        elif "paint" in text:
            return open_app("paint")
        elif "calculator" in text:
            return open_app("calculator")
        elif "cmd" in text:
            return open_app("cmd")
        elif "edge" in text:
            return open_app("edge")
        else:
            return "I can’t find that app on this system."
    elif "vs code" in text:
        return open_app ("vscode")

    # System Commands (⚠️ Optional — comment out if not needed)
    elif "shutdown" in text:
        os.systen("sudo shutdown -h now")
        return "shutting down the system..."
    elif "restart" in text:
        os.system ("sudo shutdown -r now")
        return "restarting..."
    elif "sleep" in text:
        os.system("pmset sleepnow")
        return "putting the system to sleep..."

    # Memory
    elif "remember" in text:
        info = text.replace("remember", "").strip()
        if info:
            memory.append(info)
            return f"Got it! I’ll remember that you said: '{info}'."
        else:
            return "What do you want me to remember?"

    elif "what did i tell you" in text or "what do you remember" in text:
        if memory:
            return "You told me: " + "; ".join(memory[-3:])
        else:
            return "I don’t remember anything yet."

    # Search
    elif "search" in text:
        query = text.replace("search", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching for '{query}'..."
        else:
            return "Please tell me what to search."

    # Wikipedia (browser only)
    elif "wikipedia" in text:
        topic = text.replace("wikipedia", "").strip()
        if topic:
            webbrowser.open(f"https://en.wikipedia.org/wiki/{topic}")
            return f"Looking up {topic} on Wikipedia..."
        else:
            return "What topic should I look up?"

    # Fallback
    else:
        return random.choice([
            "I’m still learning that part.",
            "Could you rephrase that?",
            "Hmm, that’s interesting.",
            "I'm not sure about that yet, but I'll try to learn!"
        ])

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"response": "Please say or type something."})

    response = generate_response(user_message)
    memory.append({"user": user_message, "bot": response})
    return jsonify({"response": response})

if __name__ == "__main__":
    print("🤖 KRYTEN Backend is running on http://127.0.0.1:5000/")
    app.run(host="127.0.0.1", port=5000, debug=True) 