import speech_recognition as sr
from collections import Counter

# Define word categories
first_person_pronouns = {"i", "me", "my", "mine", "myself"}
negative_emotion_words = {
    "sad", "unhappy", "miserable", "lonely", "angry", "tired", "hopeless", "depressed",
    "guilty", "worthless", "broken", "useless", "numb", "pointless", "stuck", "lost", "empty",
    "sick", "pain", "bad", "wrong", "cry", "tears", "hurt", "alone", "dark", "can't", "never"
}
absolutist_words = {
    "always", "never", "completely", "nothing", "totally", "entirely",
    "absolutely", "everyone", "no one", "forever", "all", "none", "everything"
}

def analyze_depressive_speech(text):
    """Analyze the speech for depression indicators."""
    words = text.lower().split()
    word_count = len(words)

    word_freq = Counter(words)
    
    first_person_count = sum(word_freq[word] for word in first_person_pronouns if word in word_freq)
    negative_emotion_count = sum(word_freq[word] for word in negative_emotion_words if word in word_freq)
    absolutist_count = sum(word_freq[word] for word in absolutist_words if word in word_freq)

    # Calculate percentages
    results = {
        "Total Words": word_count,
        "First-Person Pronouns (%)": (first_person_count / word_count) * 100 if word_count > 0 else 0,
        "Negative Emotion Words (%)": (negative_emotion_count / word_count) * 100 if word_count > 0 else 0,
        "Absolutist Words (%)": (absolutist_count / word_count) * 100 if word_count > 0 else 0
    }

    # Depression Severity Score
    depression_score = (negative_emotion_count * 2) + (absolutist_count * 1.5) + (first_person_count * 1)

    # Diagnosis
    if depression_score >= 10:
        diagnosis = "**High Concern:** Strong depressive indicators detected. Consider seeking help."
    elif depression_score >= 5:
        diagnosis = "**Mild Concern:** Some depressive patterns detected. Monitor speech over time."
    else:
        diagnosis = "**Normal:** No strong signs of depression detected."

    return results, diagnosis

def record_speech(duration=60):  # Forced 60-second recording
    """Record speech for a full 60 seconds without early termination."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Speak freely for **60 seconds** (Recording...)\n")
        
        # Set pause_threshold=2 to prevent early stopping on small pauses
        recognizer.pause_threshold = 2  
        
        try:
            audio = recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            print("\n⏳ Processing speech...\n")
            text = recognizer.recognize_google(audio)  # Convert speech to text
            return text
        except sr.UnknownValueError:
            return "**Error:** Could not understand the speech."
        except sr.RequestError:
            return "**Error:** Speech Recognition API not available."

# Main execution
if __name__ == "__main__":
    speech_text = record_speech()  # Capture voice input
    if "**Error:**" not in speech_text:
        print(f"\n📝 You said: {speech_text}\n")
        analysis, diagnosis = analyze_depressive_speech(speech_text)

        print("\n🔍 **Depression Analysis Results:**")
        for key, value in analysis.items():
            print(f"{key}: {value:.2f}%")
        print("\n📌 **Diagnosis:**", diagnosis)
    else:
        print(speech_text)



