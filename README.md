# python-youtube-downloader

A python program built for use in Windows and Visual Studio Code to download and convert entire Youtube videos and playlists from video to audio format.

This script will have you input a URL (playlist or video), download it as a .mp4 at highest quality, and convert it to a mp3, removing the original .mp4 if remove_source_file (see configuration below) is set to True.

---

The script works essentially as is, excluding this little bit of setup that will not intrude on the preferences you have set for Visual Studio Code (assuming that's what you're using.)

1. You must pip install pytube from within Visual Studio Code.

2. You must have ffmpeg installed from https://ffmpeg.org/download.html#build-windows, may be different for other systems.
   On Windows, you must add the /bin folder within the compressed (zip) folder to the "path" System Enviroment Variable after renaming the containing folder to "ffmppeg" in a rememberable location, which on Windows 10, is changable through running "system enviroment variables" as admin and adding the path to ffmpeg to "path." Screenshots for this is located at https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ for older Windows systems, but it is the same for Windows 10, ect.
   For some people, simply adding the ffmpeg.exe file within /bin/ folder from within the same compressed (zip) folder into the directory the script is ran in will work.

---

Configuration options exist at the top of the python file.

    debug_mode = False             If you want to see FFMPEG output and other info for debugging.

    remove_source_file = True      If you want to remove the video (.mp4) file after converting to audio (.mp3).

---

The reason this exists is because many scripts I've found across the internet have either been so horridly outdated to the point of breaking beyond repair within the bounds of the methods they use are malicious, mostly lackluster to begin with.

> > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >

DO NOT use this to download copyrighted content!
I will not endorse it and heavily discourage it.
This script is purely for personal, educational use, archiving, and ultimately uncopyrighted content; such as grabbing uncopyrighted backing tracks and effects for video and audio production. Using this may be against the Terms of Service of YouTube and should used be at your own risk.
