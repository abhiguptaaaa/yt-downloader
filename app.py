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
        'outtmpl': filepath + ".%(ext)s",
        'noplaylist': True,
        'quiet': True,
    }

    if selected_format == "mp3" or selected_format == "m4a":
        ydl_opts.update({
            'extract_audio': True,
            'format': 'bestaudio/best',
            'audioformat': selected_format,
            'keepvideo': False,
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': selected_format,
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            actual_filepath = ydl.prepare_filename(info_dict)

        return send_file(actual_filepath, as_attachment=True)

    except Exception as e:
        return f"❌ Error while downloading: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
