import os
import time
from pytube import Playlist, YouTube


class Config():  # CONFIG

    # Whether to remove the source video (.mp4) files when converted to mp3.
    # True or False
    remove_source_file = True

    # If enabled, will show more info about what's going on and error information for debugging. Not reccomended to enable this!
    debug_mode = False


'''
Links to playlists should start with;
https://youtube.com/playlist?list=
You can obtain these under "Share" and "Copy" on the playlist page,
not the link of the first video in the playlist, or any video at all.

If video files files don't convert to audio files or a error is thrown about ffmpeg,
download ffmpeg from https://ffmpeg.org/download.html#build-windows
https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ for a tutorial!
You must add the /bin folder of the zip to the system enviroment "path" variable on Windows.
If you are using Visual Studio Code, (which is what this script is built for,)
make sure you restart it before the command recognition will come into effect.
Run VS Code as Admin to allow the terminal to run as admin-- required for using ffmpeg
If ffmpeg still doesn't work, try to put the \bin\ffmpeg.exe executable next to the script.

https://www.youtube.com/watch?v=XGckAVECXKw
https://www.youtube.com/playlist?list=PLP1MQHioOXtF0XXz3HRhkIqo8u-f7nNOh

pip list --outdated
'''


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
        print(format.red, ' Make sure to enter a valid URL!\n  Playlists should start with ', format.italic, format.underline,
              'https://youtube.com/playlist?list=', format.reset, format.red,
              '\n  Videos should start with   ', format.italic, format.underline,
              'https://www.youtube.com/watch?v=', format.reset, format.red,
              '\n  You can obtain playlist links under \"Share\" and \"Copy\" on the playlist page, not the link of any video within the playlist!'
              '\n  The connection may had failed if you received streamingData, and you should retry or use a different video.', format.reset)


class response:  # Various "responses" that can be used for prompts, all put here for ease
    is_yes = ['yes', 'ye', 'yea', 'yeah', 'yup', 'yay', 'y']
    is_no = ['no', 'na', 'naw', 'nah', 'nay', 'nu', 'nada', 'n']


# download a playlist from a url
def playlist_downloader_execute(playlist_url):
    # remove special characters in playlist name/playlist title
    playlist_title_filtered = (playlist_url.title)
    playlist_title_filtered.replace(';', '-')
    playlist_title_filtered.replace(':', '-')

    # if title is (still) invalid, makes a directory named Backup instead of the playlist's name, then go into that directory
    try:
        if not (os.path.isdir("./"+playlist_title_filtered)):  # if directory doesnt exist
            os.mkdir(playlist_title_filtered)
        os.chdir(playlist_title_filtered)  # Change working directory
    except:
        if not (os.path.isdir("./"+'Backup')):  # if directory doesnt exist
            os.mkdir('Backup')
        os.chdir('Backup')  # Change working directory
        print(format.yellow, format.italic, "Folder name would had been invalid due to special characters typically disallowed within a file's name.\nCreated a directory alternatively named Backup instead of the playlist's name.", format.reset)

    # get linked list of links in the playlist
    links = playlist_url.video_urls
    # download each item in the list
    for i, l in enumerate(links):
        print(format.reset, "", str(i+1)+" of "+(str(len(links))) +
              format.light_gray, format.italic, " ("+str(round(((i/len(links))*100), 2))+"%)", format.reset)
        yt = YouTube(l)  # Convert link to YouTube object

        # takes the best resolution stream for best possible audio result
        stream = yt.streams.get_highest_resolution()

        # gets the filename of the first audio stream
        default_filename = stream.default_filename
        print(format.green, format.bold, "Downloading  ",
              format.reset, (default_filename[:-4]))

        # downloads first audio stream
        stream.download()

        # creates mp3 filename for downloaded file
        new_filename = default_filename[0:-3] + "mp3"

        def ffmpeg_to_mp3():  # Convert the mp4 to mp3 using ffmpeg
            for filename in os.listdir((os.curdir)):  # Convert
                if (filename.endswith(".mp4")):
                    print(format.green, format.italic,
                          'Converting', format.reset)
                    prompt_a = ("ffmpeg -i \""+default_filename +
                                "\" \""+new_filename+"\""+" -y")
                    prompt_b = (" -loglevel warning")  # debug mode

                    if Config.debug_mode == True:
                        os.system(prompt_a)
                    elif Config.debug_mode == False:
                        os.system(prompt_a + prompt_b)
        ffmpeg_to_mp3()

        if Config.remove_source_file == True:
            # Remove original mp4, just leaving the converted file
            os.remove(default_filename)

    format.divider()  # Ran at the end of the program
    print(format.green, format.bold, "Complete!", format.reset)
    format.divider()

########################################################################################################################################


def video_downloader_execute(video_url):  # download a video from a url
    video_title_filtered = video_url.title()
    video_title_filtered.replace(';', '-')
    video_title_filtered.replace(':', '-')

    # Convert link to YouTube object (makimg the yt variable)
    yt = YouTube(video_url)

    # gets the best resolution stream for best possible audio result
    stream = yt.streams.get_highest_resolution()

    # gets the filename of the first audio stream, tells the user it's downloading
    # assign the default file name to a variable
    default_filename = stream.default_filename
    print(format.green, format.bold, "Downloading  ",
          format.reset, (default_filename[:-4]))

    stream.download()

    def ffmpeg_to_mp3():
        for filename in os.listdir((os.curdir)):
            if filename.endswith(".mp4"):
                print(format.green, format.italic, 'Converting', format.reset)
                # Split into base name and extension
                base_name, _ = os.path.splitext(filename)
                new_filename = base_name + ".mp3"  # Create new filename with .mp3 extension
                prompt_a = f'ffmpeg -i "{filename}" "{new_filename}" -y'
                prompt_b = " -loglevel warning"  # debug mode

                if Config.debug_mode:
                    os.system(prompt_a)
                else:
                    os.system(prompt_a + prompt_b)

    ffmpeg_to_mp3()

    if Config.remove_source_file == True:
        # Remove original mp4, just leaving the converted file
        os.remove(default_filename)

    format.divider()  # Ran at the end of the program
    print(format.green, format.bold, "Complete!", format.reset)
    format.divider()


if __name__ == "__main__":
    '''
    name == main allows you to execute code when the file runs as a script, but not when it’s imported as a module.
    Nested code only runs in the top-level code environment, aka as a script or cmd.
    '''
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear command line

    def make_header():  # Make the header containing the program's name, credits, and show warnings if certain settings are set to true
        if Config.remove_source_file == False:  # If remove_source_file is false, tell the user that source video files will be removed when converted
            print(format.yellow, "[INFO]", format.italic,  "remove_source_file", format.reset, format.yellow,
                  " is set to ", format.bold, "false!", format.reset, format.yellow, "\nAs a result, you will be prompted to answer \"yes\" or \"no\" to anything ffmpeg may ask of you, primarily the annoying overwriting of duplicate files!\nSet it to \"True\"  at the top of the code to ignore this warning and automatically shadow-answer \"yes\" to any prompts!", format.reset)
            format.divider()

        if Config.debug_mode == True:  # If debug on, tell the user they will see all the output coming from ffmpeg
            print(format.yellow, "[INFO] ", format.italic,  "debug_mode", format.reset, format.yellow,
                  " is set to ", format.bold, "true!", format.reset, format.yellow, "\nAs a result, you will see all the output coming from ffmpeg!\nSet it to \"False\"  at the top of the code to ignore this warning and hide ffmpeg's output!", format.reset)
            format.divider()
        print("\n                         Made by Rycia\n", format.italic, format.dark_gray,
              "       github.com/Rycia/python-youtube-downloader", format.reset, "\n")
        format.divider()
    make_header()

    def prompt_url():  # Ask the user for the URL and execute other functions & code based on the input
        global url
        url = input(
            "  Enter the URL of the YouTube playlist or video you wish to download: ")
        format.divider()

        # If url input is a playlist url, execute playlist_downloader_execute with playlist's url parameter
        if "youtube.com/playlist" in url:
            if Config.debug_mode == True:
                print(format.yellow, "[INFO] Playlist detected!")

            # With error checking, execute playlist_downloader_execute with playlist's url parameter
            yt = Playlist(url)
            if Config.debug_mode == True:
                playlist_downloader_execute(yt)
            elif Config.debug_mode == False:
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

        # If url input is a video url, execute video_downloader_execute with video's url parameter
        elif "youtube.com/watch" in url:
            if Config.debug_mode == True:
                print(format.yellow, "[INFO] Video detected!", format.reset)

            # With error checking, execute video_downloader_execute with video's url parameter
            if Config.debug_mode == True:
                video_downloader_execute(url)
            elif Config.debug_mode == False:
                try:
                    video_downloader_execute(url)
                except Exception as thrown_error:
                    error_text.invalid_url()
                    print(thrown_error)
                    # If StreamingData is the error
                    if 'streamingData' in str(thrown_error):
                        print(
                            format.red, "Check your internet connection or try again.", format.reset)
                    format.divider()
                    exit(1)
            else:
                print(
                    format.red, "[ERROR] debug_mode is neither True nor False and is therefore invalid. Set it to one of the two!", format.reset)
                exit(4)

        else:  # Invalid link
            error_text.invalid_url()

    prompt_url()  # Start the code
