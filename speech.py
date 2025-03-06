import pyttsx3
import speech_recognition as sr
import datetime
import operator
from word2number import w2n  # Convert words to numbers

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Set to Voice 1 (Female)
engine.setProperty('voice', voices[1].id)

# Set speech rate (optional)
engine.setProperty('rate', 150)

def speak(text):
    """Friday speaks"""
    print("Friday:", text)  # Display text
    engine.say(text)
    engine.runAndWait()

def listen():
    """Convert speech to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)  # Debugging message
        return text.lower()
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError:
        return "Could not connect to Google."

def get_time():
    """Get current time"""
    now = datetime.datetime.now()
    return f"The time is {now.strftime('%I:%M %p')}"

def get_date():
    """Get today's date"""
    now = datetime.datetime.now()
    return f"Today's date is {now.strftime('%A, %B %d, %Y')}"

def get_greeting():
    """Greet based on the time of day"""
    now = datetime.datetime.now()
    hour = now.hour

    if 5 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 17:
        return "Good afternoon!"
    elif 17 <= hour < 21:
        return "Good evening!"
    else:
        return "Good night!"

def calculate(expression):
    """Perform basic calculations"""
    operators = {
        "plus": operator.add,
        "+": operator.add,
        "minus": operator.sub,
        "-": operator.sub,
        "multiply": operator.mul,
        "times": operator.mul,
        "x": operator.mul,
        "divide": operator.truediv,
        "/": operator.truediv,
    }

    words = expression.split()
    numbers = []
    ops = []

    for word in words:
        if word in operators:
            ops.append(operators[word])
        else:
            try:
                numbers.append(w2n.word_to_num(word))
            except ValueError:
                pass  # Ignore non-numbers

    print(f"Detected numbers: {numbers}")  # Debugging message
    print(f"Detected operators: {ops}")  # Debugging message

    if len(numbers) == 2 and len(ops) == 1:
        result = ops[0](numbers[0], numbers[1])
        return f"The result is {result}"

    return "Sorry, I can't calculate that."

def main():
    greeting = get_greeting()
    speak(f"{greeting} My name is Friday. How can I assist you?")

    while True:
        command = listen()

        if "time" in command:
            speak(get_time())

        elif "date" in command:
            speak(get_date())

        elif "hello" in command or "hi" in command:
            speak(get_greeting())

        elif any(op in command for op in ["plus", "minus", "multiply", "times", "divide", "x", "/"]):
            speak(calculate(command))

        elif "exit" in command or "bye" in command:
            speak("Goodbye! Have a great day!")
            break

        else:
            speak("I didn't understand that. Try asking for the time, date, or a calculation.")

# Run the assistant
if __name__ == "__main__":
    main()
