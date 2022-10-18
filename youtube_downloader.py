from operator import truediv
import os
from tkinter.tix import Tree
from pytube import Playlist, YouTube

# Whether to remove the source video (.mp4) files when converted to mp3.
# True or False
remove_source_file = True

# If enabled, will show more info about what's going on and error information for debugging. Not reccomended to enable this!
debug_mode = False

# Links to playlists should start with;
# https://youtube.com/playlist?list=
# You can obtain these under "Share" and "Copy" on the playlist page,
# not the link of the first video in the playlist, or any video at all.

# If video files files don't convert to audio files or a error is thrown about ffmpeg,
# download ffmpeg from https://ffmpeg.org/download.html#build-windows
# https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ for a tutorial!
# You must add the /bin folder of the zip to the system enviroment "path" variable on Windows.
# If you are using Visual Studio Code, (which is what this script is built for,)
# make sure you restart it before the command recognition will come into effect.
# Run VS Code as Admin to allow the terminal to run as admin-- required for using ffmpeg
# If ffmpeg still doesn't work, try to put the \bin\ffmpeg.exe executable next to the script.


class format:
    blue = "\033[94m"
    green = "\033[92m"
    yellow = "\033[93m"
    red = "\033[91m"

    light_gray = "\033[0;37m"
    light_red = "\033[1;31m"
    light_green = "\033[1;32m"
    light_blue = "\033[1;34m"

    dark_gray = "\033[1;30m"

    bold = "\033[1m"
    italic = "\x1B[3m"
    underline = "\033[4m"

    reset = "\033[0m"


def TEXT_BREAK():
    print(format.bold, format.blue,
          ">>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>>", format.reset)


def run(pl):
    # Create a folder where all the songs will be put
    if not (os.path.isdir("./"+pl.title)):
        os.mkdir(pl.title)
    os.chdir(pl.title)  # Change working directory

    # get linked list of links in the playlist
    links = pl.video_urls
    # download each item in the list
    for i, l in enumerate(links):
        print(" ", str(i)+" of "+str(len(links)) +
              format.light_gray, format.italic, " ("+str(round(((i/len(links))*100), 2))+"%)", format.reset)
        yt = YouTube(l)  # Convert link to YouTube object

        # takes the best resolution stream for best possible audio result
        music = yt.streams.get_highest_resolution()

        # gets the filename of the first audio stream
        default_filename = music.default_filename
        print(format.green, format.bold, "Downloading  ",
              format.reset, default_filename)

        # downloads first audio stream
        music.download()

        # creates mp3 filename for downloaded file
        new_filename = default_filename[0:-3] + "mp3"

        for filename in os.listdir((os.curdir)):  # Convert
            if (filename.endswith(".mp4")):  # or .avi, .mpeg, ect
                print('     . . .')
                prompt_a = ("ffmpeg -i \""+default_filename +
                            "\" \""+new_filename+"\""+" -y")
                prompt_b = (" -loglevel warning")  # debug mode

                if debug_mode == True:
                    os.system(prompt_a)
                elif debug_mode == False:
                    os.system(prompt_a + prompt_b)

        if remove_source_file == True:
            # Remove original mp4, just leaving the converted file
            os.remove(default_filename)

    TEXT_BREAK()
    print(format.green, format.bold, "\nComplete!", format.reset)
    TEXT_BREAK()


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear command line

    if remove_source_file == False:
        print(format.italic, format.yellow, "remove_source_file", format.reset, format.yellow,
              " is set to ", format.bold, "false!", format.reset, format.yellow, "\nAs a result, you will be prompted to answer \"yes\" or \"no\" to anything ffmpeg may ask of you, primarily the annoying overwriting of duplicate files!\nSet it to \"True\"  at the top of the code to ignore this warning and automatically shadow-answer \"yes\" to any prompts!", format.reset)
        TEXT_BREAK()

    if debug_mode == True:
        print(format.italic, format.yellow, "debug_mode", format.reset, format.yellow,
              " is set to ", format.bold, "true!", format.reset, format.yellow, "\nAs a result, you will see all the output coming from ffmpeg!\nSet it to \"False\"  at the top of the code to ignore this warning and hide ffmpeg's output!", format.reset)
        TEXT_BREAK()

    TEXT_BREAK()
    print("                         Made by Rycia\n                  ", format.italic, format.dark_gray,
          "  github.com/Rycia\n          github.com/Rycia/python-youtube-downloader", format.reset)

    TEXT_BREAK()
    url = input("Enter the URL of the YouTube playlist you wish to download: ")
    TEXT_BREAK()
    pl = Playlist(url)

    if debug_mode == True:
        run(pl)
    elif debug_mode == False:
        try:
            run(pl)
        except Exception as thrown_error:
            print(format.red, "ERROR | Enter a valid URL!\n Playlists should start with", format.italic, format.underline,
                  "https://youtube.com/playlist?list=", format.reset, format.red,
                  "\n You can obtain these under \"Share\" and \"Copy\" on the playlist page, not the link of any video within the playlist!", format.reset)
            print(thrown_error)
            TEXT_BREAK()
            exit(1)
    else:
        print(format.red, "ERROR | debug_mode is neither True nor False and is therefore invalid. Set it to one of the two!", format.reset)
        exit(2)
