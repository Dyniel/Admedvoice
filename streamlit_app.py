import streamlit as st
import time
import speech_recognition as sr

def recognize_speech_from_microphone(recognizer, microphone):
    with microphone as source:
        st.write("Proszę mówić...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        speech_to_text = recognizer.recognize_google(audio, language="pl-PL")
        st.write("Rozpoznano: " + speech_to_text)
        return speech_to_text
    except sr.UnknownValueError:
        st.write("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        st.write("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

def listen_and_edit_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    text = ""
    text_area = st.empty()

    while True:
        command = recognize_speech_from_microphone(recognizer, microphone)

        if command:
            if "zakończ" in command.lower():
                st.write("Zakończenie edycji.")
                break
            else:
                text += " " + command
                text_area.text_area("Edytuj tekst", value=text)



if __name__ == "__main__":
    st.title("Edytor dźwiękowy")
    st.write("Naciśnij przycisk poniżej, aby rozpocząć edycję tekstu.")
    if st.button("Rozpocznij edycję"):
        listen_and_edit_text()
