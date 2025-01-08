import openai
import speech_recognition as sr

openai.api_key = 'YOUR_OPENAI_API_KEY'

def transcribe_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Transcribing...")
        transcription = recognizer.recognize_google(audio)
        print("Transcription: " + transcription)
        return transcription
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

def generate_story(transcription):
    prompt = f"Create a story based on the following conversation: {transcription}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    story = response['choices'][0]['message']['content']
    return story

def generate_code_for_story(story):
    prompt = f"Generate code that represents this story: {story}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    code = response['choices'][0]['message']['content']
    return code

def main():
    # Step 1: Transcription
    transcription = transcribe_audio()

    if transcription:
        # Step 2: Generate story
        story = generate_story(transcription)
        print("Generated Story: ")
        print(story)

        # Step 3: Generate code for the story
        code = generate_code_for_story(story)
        print("Generated Code: ")
        print(code)

if __name__ == "__main__":
    main()
