import speech_recognition as sr
from collections import Counter

# Define word categories
first_person_pronouns = {"i", "me", "my", "mine", "myself"}

negative_emotion_words = {
    "sad", "unhappy", "miserable", "lonely", "angry", "tired", "hopeless", "depressed", "guilty", "worthless", "broken",
    "useless", "numb", "pointless", "stuck", "lost", "empty", "sick", "pain", "bad", "wrong", "cry", "tears", "hurt", "alone",
    "dark", "can't", "never", "fear", "regret", "shame", "doubt", "failure", "sorrow", "grief", "frustrated", "weak", "despair"
}

anxiety_words = {
    "worried", "anxious", "nervous", "panic", "uneasy", "overthinking", "afraid", "pressure", "tension", "racing thoughts",
    "dizzy", "sweaty", "overwhelmed", "fearful", "jumpy", "restless", "dread", "shaky", "hyperventilate", "heartbeat",
    "avoiding", "paralyzed", "self-conscious", "insecure", "distress", "tense", "obsessive", "doom"
}

ptsd_words = {
    "flashback", "nightmare", "trauma", "abuse", "reliving", "trigger", "startle", "dissociate", "numb", "detached", "on edge",
    "hypervigilant", "fear", "avoidance", "disturbance", "shaking", "agitated", "intrusive", "paranoia", "alert", "hyperaware",
    "guilt", "isolation", "mistrust", "suffocating", "claustrophobic", "sweating", "hallucination", "screaming"
}

bipolar_words = {
    "manic", "hypomania", "euphoric", "impulsive", "reckless", "energetic", "grandiose", "insomnia", "uncontrollable", "racing thoughts",
    "irritable", "overconfident", "agitated", "delusions", "distracted", "hyperactive", "excessive", "talkative", "restless",
    "elevated mood", "reckless spending", "hypersexual", "invincible", "risky", "extreme highs", "extreme lows", "rapid speech"
}

absolutist_words = {
    "always", "never", "completely", "nothing", "totally", "entirely", "absolutely", "everyone", "no one", "forever", "all", "none", "everything"
}

def analyze_speech(text):
    """Analyze the speech for mental health indicators."""
    words = text.lower().split()
    word_count = len(words)
    word_freq = Counter(words)
    
    first_person_count = sum(word_freq[word] for word in first_person_pronouns if word in word_freq)
    negative_emotion_count = sum(word_freq[word] for word in negative_emotion_words if word in word_freq)
    anxiety_count = sum(word_freq[word] for word in anxiety_words if word in word_freq)
    ptsd_count = sum(word_freq[word] for word in ptsd_words if word in word_freq)
    bipolar_count = sum(word_freq[word] for word in bipolar_words if word in word_freq)
    absolutist_count = sum(word_freq[word] for word in absolutist_words if word in word_freq)
    
    # Calculate percentages
    results = {
        "Total Words": word_count,
        "First-Person Pronouns (%)": (first_person_count / word_count) * 100 if word_count > 0 else 0,
        "Negative Emotion Words (%)": (negative_emotion_count / word_count) * 100 if word_count > 0 else 0,
        "Anxiety Words (%)": (anxiety_count / word_count) * 100 if word_count > 0 else 0,
        "PTSD Words (%)": (ptsd_count / word_count) * 100 if word_count > 0 else 0,
        "Bipolar Words (%)": (bipolar_count / word_count) * 100 if word_count > 0 else 0,
        "Absolutist Words (%)": (absolutist_count / word_count) * 100 if word_count > 0 else 0
    }
    
    # Mental Health Scores
    depression_score = (negative_emotion_count * 2) + (absolutist_count * 1.5) + (first_person_count * 1)
    anxiety_score = anxiety_count * 2.5
    ptsd_score = ptsd_count * 3
    bipolar_score = bipolar_count * 2.5
    
    # Diagnosis
    diagnosis = []
    if depression_score >= 10:
        diagnosis.append("**Depression:** Strong indicators detected. Consider seeking help.")
    if anxiety_score >= 8:
        diagnosis.append("**Anxiety:** High levels of anxious speech detected.")
    if ptsd_score >= 8:
        diagnosis.append("**PTSD:** Speech suggests possible traumatic stress.")
    if bipolar_score >= 8:
        diagnosis.append("**Bipolar Disorder:** Manic or depressive speech patterns detected.")
    
    if not diagnosis:
        diagnosis.append("**Normal:** No strong signs of mental health issues detected.")
    
    return results, "\n".join(diagnosis)

def record_speech(duration=30):  # Forced 30-second recording
    """Record speech for a full 30 seconds without early termination."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Speak freely for **30 seconds** (Recording...)\n")
        
        recognizer.pause_threshold = 2  # Allows for brief pauses
        
        try:
            audio = recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            print("\n⏳ Processing speech...\n")
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "**Error:** Could not understand the speech."
        except sr.RequestError:
            return "**Error:** Speech Recognition API not available."

# Main execution
if __name__ == "__main__":
    speech_text = record_speech()
    if "**Error:**" not in speech_text:
        print(f"\n📝 You said: {speech_text}\n")
        analysis, diagnosis = analyze_speech(speech_text)
        print("\n🔍 **Mental Health Analysis Results:**")
        for key, value in analysis.items():
            print(f"{key}: {value:.2f}%")
        print("\n📌 **Diagnosis:**", diagnosis)
    else:
        print(speech_text)



