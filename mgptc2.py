from flask import Flask, render_template, request
import pyttsx3
import os
import uuid

app = Flask(__name__, template_folder='somethingnew')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if an audio file is uploaded
        if 'audio_file' in request.files:
            # Get the uploaded audio file
            audio_file = request.files['audio_file']

            # Generate a unique filename
            unique_filename = str(uuid.uuid4()) + '.wav'

            # Save the uploaded file to a desired location with the unique filename
            audio_file.save(os.path.join('audiohtml', unique_filename))

            # Process the uploaded audio file (e.g., perform analysis or other operations)

            return 'Audio uploaded successfully!'

        else:
            # Get user inputs from the form
            speaker = request.form['speaker']
            text_input = request.form['text_input']

            # Generate audio file
            audio_file = generate_audio(speaker, text_input)

            # Generate a unique filename
            unique_filename = str(uuid.uuid4()) + '.mp3'

            # Save the generated audio file with the unique filename
            os.rename(audio_file, os.path.join('static', unique_filename))

            # Render the template with the unique filename
            return render_template('audio_input.html', audio_file=unique_filename)

    return render_template('audio_input.html')


def generate_audio(speaker, text_input):
    # Initialize text-to-speech engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust speech rate if needed

    # Set the speaker voice
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice.name == speaker:
            engine.setProperty('voice', voice.id)
            break

    # Generate audio file
    output_file = 'generated_audio.mp3'
    engine.save_to_file(text_input, output_file)
    engine.runAndWait()

    return output_file


if __name__ == '__main__':
    app.run(debug=True)
