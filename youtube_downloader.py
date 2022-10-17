from operator import truediv
import os
import subprocess
import string
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

TEXT_BLUE = "\033[94m"
TEXT_GREEN = "\033[92m"
TEXT_YELLOW = "\033[93m"
TEXT_RED = "\033[91m"

TEXT_LIGHT_GRAY = "\033[0;37m"
TEXT_LIGHT_RED = "\033[1;31m"
TEXT_LIGHT_GREEN = "\033[1;32m"
TEXT_LIGHT_BLUE = "\033[1;34m"

TEXT_DARK_GRAY = "\033[1;30m"

TEXT_BOLD = "\033[1m"
TEXT_ITALIC = "\x1B[3m"
TEXT_UNDERLINE = "\033[4m"

TEXT_RESET = "\033[0m"  # ", TEXT_RESET, "


def TEXT_BREAK():
    print(TEXT_BOLD, TEXT_BLUE,
          ">>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>>", TEXT_RESET)


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
              TEXT_LIGHT_GRAY, TEXT_ITALIC, " ("+str(round(((i/len(links))*100), 2))+"%)", TEXT_RESET)
        yt = YouTube(l)  # Convert link to YouTube object

        # takes the best resolution stream for best possible audio result
        music = yt.streams.get_highest_resolution()

        # gets the filename of the first audio stream
        default_filename = music.default_filename
        print(TEXT_GREEN, TEXT_BOLD, "Downloading  ",
              TEXT_RESET, default_filename)

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
    print(TEXT_GREEN, TEXT_BOLD, "\nComplete!", TEXT_RESET)
    TEXT_BREAK()


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear command line

    if remove_source_file == False:
        print(TEXT_ITALIC, TEXT_YELLOW, "remove_source_file", TEXT_RESET, TEXT_YELLOW,
              " is set to ", TEXT_BOLD, "false!", TEXT_RESET, TEXT_YELLOW, "\nAs a result, you will be prompted to answer \"yes\" or \"no\" to anything ffmpeg may ask of you, primarily the annoying overwriting of duplicate files!\nSet it to \"True\"  at the top of the code to ignore this warning and automatically shadow-answer \"yes\" to any prompts!", TEXT_RESET)
        TEXT_BREAK()

    if debug_mode == True:
        print(TEXT_ITALIC, TEXT_YELLOW, "debug_mode", TEXT_RESET, TEXT_YELLOW,
              " is set to ", TEXT_BOLD, "true!", TEXT_RESET, TEXT_YELLOW, "\nAs a result, you will see all the output coming from ffmpeg!\nSet it to \"False\"  at the top of the code to ignore this warning and hide ffmpeg's output!", TEXT_RESET)
        TEXT_BREAK()

    TEXT_BREAK()
    print("                         Made by Rycia\n                  ", TEXT_ITALIC, TEXT_DARK_GRAY,
          "  github.com/Rycia\n          github.com/Rycia/python-youtube-downloader", TEXT_RESET)

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
            print(TEXT_RED, "ERROR | Enter a valid URL!\n Playlists should start with", TEXT_ITALIC, TEXT_UNDERLINE,
                  "https://youtube.com/playlist?list=", TEXT_RESET, TEXT_RED,
                  "\n You can obtain these under \"Share\" and \"Copy\" on the playlist page, not the link of any video within the playlist!", TEXT_RESET)
            print(thrown_error)
            TEXT_BREAK()
            exit(1)
    else:
        print(TEXT_RED, "ERROR | debug_mode is neither True nor False and is therefore invalid. Set it to one of the two!", TEXT_RESET)
        exit(2)
