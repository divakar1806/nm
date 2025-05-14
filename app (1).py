from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Enhanced healthcare responses with more conditions and detailed information
healthcare_responses = {
    "headache": {
        "symptoms": [
            "Dull, aching head pain",
            "Sensation of tightness or pressure across forehead",
            "Tenderness on scalp, neck, and shoulder muscles"
        ],
        "remedies": [
            "Rest in a quiet, dark room",
            "Stay hydrated",
            "Take over-the-counter pain relievers",
            "Apply a cold or warm compress",
            "Practice relaxation techniques",
            "If persistent, consult a doctor"
        ],
        "prevention": [
            "Maintain regular sleep schedule",
            "Stay hydrated",
            "Manage stress",
            "Avoid known triggers"
        ]
    },
    "fever": {
        "symptoms": [
            "Body temperature above 98.6°F (37°C)",
            "Sweating or chills",
            "Headache",
            "Muscle aches"
        ],
        "remedies": [
            "Rest",
            "Stay hydrated",
            "Take fever reducers",
            "Use light clothing and bedding",
            "Take lukewarm baths"
        ],
        "warning": "Seek immediate medical attention if temperature exceeds 103°F (39.4°C)"
    },
    "cold": {
        "symptoms": [
            "Runny or stuffy nose",
            "Sore throat",
            "Cough",
            "Congestion",
            "Mild body aches"
        ],
        "remedies": [
            "Rest",
            "Drink warm fluids",
            "Use over-the-counter cold medications",
            "Use a humidifier",
            "Gargle with salt water",
            "Try honey for sore throat"
        ],
        "prevention": [
            "Wash hands frequently",
            "Avoid close contact with sick people",
            "Maintain good sleep habits",
            "Eat vitamin-rich foods"
        ]
    },
    "cough": {
        "types": [
            "Dry cough",
            "Wet cough",
            "Persistent cough"
        ],
        "remedies": [
            "Stay hydrated",
            "Use honey for soothing",
            "Try over-the-counter cough medicine",
            "Use a humidifier",
            "Avoid irritants"
        ],
        "warning": "Consult a doctor if cough persists over 2 weeks or is accompanied by difficulty breathing"
    },
    "stress": {
        "symptoms": [
            "Anxiety",
            "Restlessness",
            "Lack of motivation or focus",
            "Irritability",
            "Sleep problems"
        ],
        "management": [
            "Practice deep breathing exercises",
            "Regular exercise",
            "Maintain a healthy sleep schedule",
            "Try meditation or yoga",
            "Talk to friends or a therapist"
        ]
    },
    "allergies": {
        "symptoms": [
            "Sneezing",
            "Runny or stuffy nose",
            "Watery eyes",
            "Itching of nose, eyes, or roof of mouth"
        ],
        "remedies": [
            "Take antihistamines",
            "Use nasal sprays",
            "Keep windows closed during high pollen times",
            "Use air purifiers",
            "Shower after being outdoors"
        ]
    }
}

# Greeting messages for variety
greetings = [
    "Hello! I'm your healthcare assistant. How can I help you today?",
    "Hi there! I'm here to help with your health concerns. What can I do for you?",
    "Welcome! I'm your virtual health assistant. How may I assist you?",
    "Greetings! I'm here to provide health information. What would you like to know?"
]

def format_condition_response(condition_data):
    """Format the detailed condition data into a readable response"""
    response = ""
    
    if "symptoms" in condition_data:
        response += "Symptoms:\n" + "\n".join(f"• {s}" for s in condition_data["symptoms"]) + "\n\n"
    
    if "types" in condition_data:
        response += "Types:\n" + "\n".join(f"• {t}" for t in condition_data["types"]) + "\n\n"
    
    if "remedies" in condition_data:
        response += "Remedies:\n" + "\n".join(f"• {r}" for r in condition_data["remedies"]) + "\n\n"
    
    if "prevention" in condition_data:
        response += "Prevention:\n" + "\n".join(f"• {p}" for p in condition_data["prevention"]) + "\n\n"
    
    if "management" in condition_data:
        response += "Management:\n" + "\n".join(f"• {m}" for m in condition_data["management"]) + "\n\n"
    
    if "warning" in condition_data:
        response += "⚠️ Warning: " + condition_data["warning"]
    
    return response.strip()

def get_bot_response(user_message):
    """Generate appropriate response based on user input"""
    user_message = user_message.lower()
    
    # Handle greetings
    if user_message in ['hello', 'hi', 'hey']:
        return random.choice(greetings)
    
    # Handle goodbye
    if user_message in ['bye', 'goodbye', 'see you']:
        return "Take care! Remember to prioritize your health. Feel free to return if you have more questions."
    
    # Handle help request
    if user_message == 'help':
        conditions = list(healthcare_responses.keys())
        return f"I can provide information about these health conditions:\n" + \
               "\n".join(f"• {condition.title()}" for condition in conditions) + \
               "\n\nJust type the condition you'd like to learn about!"
    
    # Check for health conditions
    for condition, data in healthcare_responses.items():
        if condition in user_message:
            return format_condition_response(data)
    
    # Default response
    return "I'm not sure about that. Please ask about specific conditions like headache, fever, cold, cough, stress, or allergies. Type 'help' to see all available topics."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']
    response = get_bot_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True) 