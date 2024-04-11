import streamlit as st
from streamlit_webrtc import webrtc_streamer, get_audio_devices
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

    audio_devices = get_audio_devices()
    selected_audio_device = st.selectbox("Wybierz urządzenie audio", audio_devices)

    microphone = sr.Microphone(device_index=selected_audio_device)

    text = ""
    text_area = st.empty()

    webrtc_ctx = webrtc_streamer(
        key="audio-record",
        audio=True,
        # Ustawiamy parametr `processing_timeout` na 10 sekund
        # żeby zakończyć nagrywanie po 10 sekundach nieaktywności
        processing_timeout=10,
        audio_receiver_bitrate=16000,  # Dodajemy tę linijkę żeby ustawić bitrate na 16 kHz
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

    if webrtc_ctx.audio_receiver:
        command = recognize_speech_from_microphone(recognizer, microphone)

        if command:
            if "zakończ" in command.lower():
                st.write("Zakończenie edycji.")
            else:
                text += " " + command
                text_area.text_area("Edytuj tekst", value=text)


if __name__ == "__main__":
    st.title("Edytor dźwiękowy")
    st.write("Naciśnij przycisk poniżej, aby rozpocząć edycję tekstu.")
    if st.button("Rozpocznij edycję"):
        listen_and_edit_text()
