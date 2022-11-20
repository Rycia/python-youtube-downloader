import os
from operator import truediv
from tkinter.tix import Tree
from pytube import Playlist, YouTube
# https://www.youtube.com/watch?v=XGckAVECXKw
# https://www.youtube.com/playlist?list=PLP1MQHioOXtF0XXz3HRhkIqo8u-f7nNOh

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# CONFIG

# Whether to remove the source video (.mp4) files when converted to mp3.
# True or False
remove_source_file = True

# If enabled, will show more info about what's going on and error information for debugging. Not reccomended to enable this!
debug_mode = False

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

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

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


class format:  # text formatting bank, in a class to be collapsable
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

    def divider():
        print(format.bold, format.blue,
              ">>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>>", format.reset)


class error_text:
    def invalid_url():
        print(format.red, 'Enter a valid URL!\n\n Playlists should start with ', format.italic, format.underline,
              'https://youtube.com/playlist?list=', format.reset, format.red,
              '\n Videos shoulds start with   ', format.italic, format.underline,
              'https://www.youtube.com/watch?v=', format.reset, format.red,
              '\n\n You can obtain playlist links under \"Share\" and \"Copy\" on the playlist page, not the link of any video within the playlist!', format.reset)


class response:  # Various "responses" that can be used for prompts, all put here for ease
    is_yes = ['yes', 'ye', 'yea', 'yeah', 'yup', 'yay', 'y']
    is_no = ['no', 'na', 'naw', 'nah', 'nay', 'nu', 'nada', 'n']
    is_playlist = ['playlist', 'plist', 'playl',
                   'pl', 'play', 'multi', 'multiple,', 'm']
    is_video = ['video', 'vid', 'v', 'single', 's']

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


def playlist_downloader_execute(playlist_url):
    # remove special characters in playlist name/playlist title
    playlist_title_filtered = (playlist_url.title)
    playlist_title_filtered.replace(';', '-')
    playlist_title_filtered.replace(':', '-')

    # if title is invalid, makes a alt directory
    try:
        if not (os.path.isdir("./"+playlist_title_filtered)):
            os.mkdir(playlist_title_filtered)
        os.chdir(playlist_title_filtered)  # Change working directory
    except:
        if not (os.path.isdir("./"+'Backup')):
            os.mkdir('Backup')
        os.chdir('Backup')  # Change working directory
        print(format.yellow, format.italic, "Folder name would had been invalid due to special characters typically disallowed within a file's name.\nCreated a directory alternatively named Backup instead of the playlist's name.", format.reset)

    # get linked list of links in the playlist
    links = playlist_url.video_urls
    # download each item in the list
    for i, l in enumerate(links):
        print(format.reset, str(i)+" of "+str(len(links)) +
              format.light_gray, format.italic, " ("+str(round(((i/len(links))*100), 2))+"%)", format.reset)
        yt = YouTube(l)  # Convert link to YouTube object

        # takes the best resolution stream for best possible audio result
        stream = yt.streams.get_highest_resolution()

        # gets the filename of the first audio stream
        default_filename = stream.default_filename
        print(format.green, format.bold, "Downloading  ",
              format.reset, default_filename)

        # downloads first audio stream
        stream.download()

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
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# Ran at the end of the program

    format.divider()
    print(format.green, format.bold, "Complete!", format.reset)
    format.divider()


def video_downloader_execute(video_url):
    # download each item in the list
    #link = video_url.video_urls

    # yt = YouTube(url)  # Convert link to YouTube object
    yt = YouTube(video_url)

    # takes the best resolution stream for best possible audio result
    stream = yt.streams.get_highest_resolution()

    # gets the filename
    default_filename = stream.default_filename
    print(format.green, format.bold, "Downloading  ",
          format.reset, default_filename)

    stream.download()

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

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


if __name__ == "__main__":
    # name == main allows tou to execute code when the file runs as a script, but not when it’s imported as a module.
    # Nested code only runs in the top-level code environment, aka as a script or cmd.
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear command line

    def make_header():  # Make the "heaher" containing credits and warning messages
        if remove_source_file == False:
            print(format.yellow, "[INFO]", format.italic,  "remove_source_file", format.reset, format.yellow,
                  " is set to ", format.bold, "false!", format.reset, format.yellow, "\nAs a result, you will be prompted to answer \"yes\" or \"no\" to anything ffmpeg may ask of you, primarily the annoying overwriting of duplicate files!\nSet it to \"True\"  at the top of the code to ignore this warning and automatically shadow-answer \"yes\" to any prompts!", format.reset)
            format.divider()

        if debug_mode == True:
            print(format.yellow, "[INFO] ", format.italic,  "debug_mode", format.reset, format.yellow,
                  " is set to ", format.bold, "true!", format.reset, format.yellow, "\nAs a result, you will see all the output coming from ffmpeg!\nSet it to \"False\"  at the top of the code to ignore this warning and hide ffmpeg's output!", format.reset)
            format.divider()
        print("\n                         Made by Rycia\n", format.italic, format.dark_gray,
              "       github.com/Rycia/python-youtube-downloader", format.reset, "\n")
        format.divider()
    make_header()

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

    def prompt_url():  # Ask the user for the URL and execute other functions & code based on the input
        global url
        url = input(
            " Enter the URL of the YouTube playlist or video you wish to download: ")
        format.divider()

        ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

        if (str("youtube.com/playlist")) in url:  # If url input is a playlist url,
            # if using "contains," a error is thrown: AttributeError: 'str' object has no attribute 'contains', so use "in" instead
            if debug_mode == True:
                print(format.yellow, "[INFO] Playlist detected!")

            # With error checking, execute playlist_downloader_execute with playlist's url parameter
            yt = Playlist(url)
            if debug_mode == True:
                playlist_downloader_execute(yt)
            elif debug_mode == False:
                try:
                    playlist_downloader_execute(yt)
                except Exception as thrown_error:
                    error_text.invalid_url()
                    print(thrown_error)
                    format.divider()
                    exit(1)
            else:
                print(
                    format.red, "[ERROR] debug_mode is neither True nor False and is therefore invalid. Set it to one of the two!", format.reset)
                exit(2)

        ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

        elif (str("youtube.com/watch")) in url:  # If url input is a video url
            if debug_mode == True:
                print(format.yellow, "[INFO] Video detected!", format.reset)

            # With error checking, execute video_downloader_execute with video's url parameter
            yt = YouTube(url)
            if debug_mode == True:
                video_downloader_execute(yt)
            elif debug_mode == False:
                try:
                    video_downloader_execute(yt)
                except Exception as thrown_error:
                    error_text.invalid_url()
                    print(thrown_error)
                    format.divider()
                    exit(1)
            else:
                print(
                    format.red, "[ERROR] debug_mode is neither True nor False and is therefore invalid. Set it to one of the two!", format.reset)
                exit(4)

        else:  # Invalid link
            error_text.invalid_url()

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

    prompt_url()  # Start the code
