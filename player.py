import vlc
import curses
from flask import Flask, request
import os
INSTANCE = vlc.Instance()
PLAYER = INSTANCE.media_player_new()
# Media = Instance.media_new('song.mp3')
# player.set_media(Media)
# player.play()
# while True:
#     c = stdscr.getch()
#     if c == ord('q'):
#         player.pause() 
#     if c == ord('p'):
#         player.play()
UPLOAD_FOLDER = '/Users/silver/.config/player/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/<song_name>")
def play_file(song_name):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], song_name)
    media = INSTANCE.media_new(file_path)
    PLAYER.set_media(media)
    PLAYER.play()
    return f"Playing {song_name}"

@app.route("/pause")
def pause():
    PLAYER.pause()
    return("Paused!")

@app.route("/play")
def play():
    PLAYER.play()
    return("Playing!")

@app.route("/upload/<file_name>", methods=["POST"])
def upload(file_name):
    # print(request.files)
    # for f in request.files:
    #     print(f)
    #     file = request.files[f]
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return f"Uploaded ?"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
