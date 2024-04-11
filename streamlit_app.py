import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration, AudioProcessorBase
import asyncio
import speech_recognition as sr

RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

class AudioProcessor(AudioProcessorBase):
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.transcript = ""

    async def recv_queued(self, frames):
        while frames:
            frame = frames.pop(0)
            if frame:
                data = frame.to_ndarray()
                try:
                    audio = sr.AudioData(data.tobytes(), frame.sample_rate, frame.sample_width)
                    text = self.recognizer.recognize_google(audio, language="pl-PL")
                    self.transcript += text + " "
                except Exception as e:
                    print(e)
                    continue

        return self.transcript

def main():
    webrtc_ctx = webrtc_streamer(key="example",
                                 mode=WebRtcMode.SENDONLY,
                                 rtc_configuration=RTC_CONFIGURATION,
                                 audio_processor_factory=AudioProcessor,
                                 media_stream_constraints={"video": False, "audio": True},
                                 async_processing=True)

    if webrtc_ctx.state.playing:
        audio_processor: AudioProcessor = webrtc_ctx.audio_processor
        if audio_processor:
            transcript = audio_processor.transcript
            editable_transcript = st.text_area("Edytuj transkrypcję", value=transcript, height=300)
            if st.button("Zakończ edycję"):
                st.write("Zakończono edycję. Ostateczny tekst:")
                st.write(editable_transcript)

if __name__ == "__main__":
    st.title("Streamlit Edytor Tekstu na Żywo")
    main()
