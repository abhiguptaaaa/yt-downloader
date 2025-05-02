from flask import Flask, request, render_template, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    selected_format = request.form['format']
    filename = f"{uuid.uuid4()}"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        'outtmpl': filepath + ".%(ext)s", #  Crucial: Keep extension to get the right file
        'noplaylist': True,
        'quiet': True,
    }

    if selected_format == "mp3" or selected_format == "m4a":
        ydl_opts['extract_audio'] = True
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['audioformat'] = selected_format
        ydl_opts['keepvideo'] = False  # important for audio-only

    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['merge_output_format'] = selected_format  # Now use merge_output_format

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)  # Get info *and* download

        #Determine the correct filepath *after* download.  ydl_opts['outtmpl'] only specifies the *pattern*
        actual_filepath = ydl.prepare_filename(info_dict) #Correct filepath.

        return send_file(actual_filepath, as_attachment=True)  # Send the *actual* file

    except Exception as e:
        return f"❌ Error while downloading: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)