import pandas as pd
import random
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


def generate_synthetic_emails():
    subjects = {
        "meeting": ["Department Meeting at 10 AM", "Urgent: Research Review Meeting", "Schedule Confirmation"],
        "urgent": ["Immediate Action Required", "Submission Deadline Today", "Please Respond: Emergency"],
        "personal": ["Lunch Plan This Friday?", "Congratulations!", "Birthday Celebration Invite"],
        "information": ["New Guidelines for Exams", "Updated Faculty Handbook", "NAAC Accreditation Document"],
        "schedule": ["Next Week's Timetable", "Class Adjustment Notice", "Room Booking Confirmed"],
        "security": ["Unusual Login Attempt", "Account Security Alert", "Reset Your Password"]
    }

    bodies = {
        "meeting": ["Meeting with the curriculum committee at 2 PM.", "Zoom link at 11 AM sharp.", "Postponed to 4 PM."],
        "urgent": ["Submit before 5 PM.", "Final review ASAP.", "Dean’s sign-off required."],
        "personal": ["Let's catch up after your session.", "Hope you’re well!", "Pictures from our event."],
        "information": ["Revised guideline document attached.", "Updated protocol info.", "Circulars on the portal."],
        "schedule": ["Proposed schedule for next week.", "Approve or suggest edits.", "Invigilation slots uploaded."],
        "security": ["Someone tried logging in from a new device.", "We noticed suspicious activity.", "Change your password immediately."]
    }

    data = []
    for category in subjects:
        for _ in range(10):
            subject = random.choice(subjects[category])
            body = random.choice(bodies[category])
            data.append({"subject": subject, "body": body, "category": category})

    return pd.DataFrame(data)


def load_real_emails():
    if os.path.exists("gmail_emails.csv"):
        df = pd.read_csv("gmail_emails.csv")
        if 'category' not in df.columns:
            df['category'] = df.apply(lambda row: auto_label(row['subject'], row['body']), axis=1)
        return df
    return pd.DataFrame(columns=["subject", "body", "category"])


def auto_label(subject, body):
    text = f"{subject} {body}".lower()

    if any(word in text for word in [
        "security", "login", "sign-in", "unauthorized", "unusual activity",
        "alert", "account", "password", "reset password", "new device", "breach",
        "suspicious", "verification", "recovery", "2fa", "authentication", "access denied",
        "phishing", "blocked access", "attempted login", "unrecognized device",
        "verify identity", "email security", "compromised", "secure link", "session expired"
    ]):
        return "security"

    elif any(word in text for word in [
        "urgent", "asap", "immediate", "important", "final reminder", "last date",
        "action needed", "due today", "deadline", "today itself", "respond now",
        "approval required", "pending approval", "critical", "high priority",
        "emergency", "respond by", "submit", "submission deadline", "non-compliance"
    ]):
        return "urgent"

    elif any(word in text for word in [
        "meeting", "zoom", "google meet", "webex", "discussion", "conference",
        "calendar", "faculty meeting", "board meeting", "virtual session",
        "meeting scheduled", "meeting request", "call with dean", "review meeting",
        "panel discussion", "committee meeting", "connect on call", "strategic meeting"
    ]):
        return "meeting"

    elif any(word in text for word in [
        "schedule", "timetable", "revised schedule", "slot", "slot change",
        "class timing", "rescheduling", "updated slot", "adjusted slot",
        "calendar update", "exam duty", "invigilation", "lecture timing",
        "exam schedule", "exam plan", "lecture rescheduled", "teaching slot",
        "revised calendar", "updated roster", "schedule note", "duty schedule"
    ]):
        return "schedule"

    elif any(word in text for word in [
        "circular", "notice", "announcement", "guideline", "update", "notification",
        "rules", "regulation", "policy", "protocol", "minutes of meeting",
        "documentation", "instructions", "procedures", "report", "summary",
        "handbook", "exam policy", "grading policy", "evaluation method",
        "admin note", "official announcement", "institutional update", "brief",
        "memo", "new process", "attachment", "circular released"
    ]):
        return "information"

    elif any(word in text for word in [
        "birthday", "invitation", "celebration", "reunion", "dinner", "lunch", "family",
        "outing", "get together", "thank you", "congratulations", "best wishes",
        "personal", "call me", "catch up", "coffee", "greetings", "fun", "festival",
        "holiday", "gift", "wedding", "marriage", "hope you're doing well",
        "miss you", "free this evening", "event pictures"
    ]):
        return "personal"

    return "information"


df_synthetic = generate_synthetic_emails()
df_real = load_real_emails()
df = pd.concat([df_synthetic, df_real], ignore_index=True)


df['text'] = df['subject'].fillna('') + ' ' + df['body'].fillna('')
df = df.dropna(subset=['category'])


vectorizer = TfidfVectorizer(max_features=3000)
X = vectorizer.fit_transform(df['text'])
y = df['category']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
print("\n Classification Report:\n")
print(classification_report(y_test, y_pred))


with open("email_classifier_model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)


if not df_real.empty:
    df_real['text'] = df_real['subject'].fillna('') + ' ' + df_real['body'].fillna('')
    X_real = vectorizer.transform(df_real['text'])
    df_real['Predicted_Category'] = model.predict(X_real)
    df_real.to_csv("gmail_emails_classified.csv", index=False)
    print("Gmail emails classified and saved to 'gmail_emails_classified.csv'")

