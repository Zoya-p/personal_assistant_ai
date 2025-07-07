# personal_assistant_ai
AI Email Assistant with Spam Classifier This project integrates a machine learning-based spam detection system with a voice-controlled virtual assistant. It classifies email messages as spam or ham using NLP techniques and allows voice interaction for tasks like browsing, sending emails, and fetching information
# AI Email Assistant with Spam Classifier

This project combines two powerful components:
1. **Email Spam Classifier** using Machine Learning and Natural Language Processing.
2. **Voice-Controlled Virtual Assistant** capable of executing common desktop tasks through voice commands.

## Features

### 1. Email Spam Classifier
- Built using `scikit-learn`, `LogisticRegression`, and `TfidfVectorizer`.
- Trained on labeled email data (spam or ham).
- Users can input email messages through the terminal and get instant classification results.
- Accuracy metrics displayed for training and testing datasets.

### 2. Voice Assistant
- Built using `pyttsx3`, `speech_recognition`, and system-level modules.
- Responds with appropriate greetings based on the time of day.
- Supports voice commands for:
  - Searching Wikipedia
  - Opening websites like YouTube, Google, Stack Overflow
  - Playing music from a specified path
  - Telling the current time
  - Opening Visual Studio Code
  - Sending emails via SMTP (Gmail)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-email-assistant.git
   cd ai-email-assistant
