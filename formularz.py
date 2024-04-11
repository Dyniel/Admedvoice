import time
import speech_recognition as sr
from docx import Document
import spacy

#nlp = spacy.load("pl_core_news_sm")


def recognize_speech_from_microphone(recognizer, microphone):
    with microphone as source:
        print("Proszę mówić...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        speech_to_text = recognizer.recognize_google(audio, language="pl-PL")
        print("Rozpoznano: " + speech_to_text)
        return speech_to_text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


def extract_information(command):
    doc = nlp(command)
    section_name = " ".join([token.text for token in doc if token.pos_ == "NOUN"])
    return section_name



def insert_text_in_section(doc_path, section_name, text_to_insert):
    document = Document(doc_path)
    section_found = False
    for paragraph in document.paragraphs:
        if section_name.lower() in paragraph.text.lower():
            section_found = True
        elif section_found and not paragraph.text.strip():
            paragraph.insert_paragraph_before(text_to_insert)
            section_found = False
            break

    modified_doc_path = doc_path.replace(".docx", "_modified.docx")
    document.save(modified_doc_path)
    if section_found:
        print(f"Tekst '{text_to_insert}' został dodany do sekcji: {section_name}.")
    else:
        print(f"Sekcja '{section_name}' nie została znaleziona. Sprawdź, czy nazwa sekcji jest poprawna.")


def listen_and_edit_document():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        command = recognize_speech_from_microphone(recognizer, microphone)

        if command:
            if "zakończ" in command.lower():
                print("Zakończenie programu.")
                break
            elif "zacznij pisać" in command.lower():
                section_name = extract_information(command)
                print(f"Sekcja do edycji: {section_name}")
                print("Mów tekst do wstawienia...")
                text_to_insert = recognize_speech_from_microphone(recognizer, microphone)
                if text_to_insert:
                    doc_path = "/Users/daniel/PycharmProjects/Admedvoice/Formularz.docx"
                    insert_text_in_section(doc_path, section_name, text_to_insert)

        time.sleep(1)


if __name__ == "__main__":
    listen_and_edit_document()
