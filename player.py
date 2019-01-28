import vlc
import curses
from flask import Flask, request
import os

INSTANCE = vlc.Instance()
PLAYER = INSTANCE.media_player_new()
UPLOAD_FOLDER = '{}/.config/player/'.format(os.path.expanduser("~"))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CURRENT_SONG = None
SONG_QUEUE = []
SONG_PLAYING = False

@app.route("/<song_name>")
def play_file(song_name):
    CURRENT_SONG = song_name
    SONG_PLAYING = True
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], song_name)
    media = INSTANCE.media_new(file_path)
    PLAYER.set_media(media)
    PLAYER.play()
    return "Playing {}".format(song_name)

@app.route("/pause")
def pause():
    PLAYER.pause()
    return "Paused {}".format(CURRENT_SONG)

@app.route("/play")
def play():
    PLAYER.play()
    return "Playing {}".format(CURRENT_SONG)

@app.route("/queue/<song_name>")
def queue_song(song_name):
    if SONG_PLAYING:
        SONG_QUEUE.append(song_name)
        return "Queued {}".format(song_name)
    else:
        return play_file(song_name)

@app.route("/upload", methods=["POST"])
def upload():
    # Get rid of extension
    file = request.files['file']
    file_name = file.filename.split(".")[0]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    return "Uploaded {}".format(file.filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

