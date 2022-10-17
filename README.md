# python-youtube-downloader
A python program built for use in Windows and Visual Studio Code to download and convert entire Youtube playlists from video to audio format.

-------------------------

The script works essentially as is, excluding this little bit of setup that will not intrude on the preferences you have set for Visual Studio Code (assuming that's what you're using.)

1) You must pip install pytube from within Visual Studio Code.

2) You must have ffmpeg installed from https://ffmpeg.org/download.html#build-windows, may be different for other systems.
      On Windows, you must add the /bin folder within the compressed (zip) folder to the "path" System Enviroment Variable after renaming the containing folder to "ffmppeg" in a rememberable location, which on Windows 10, is changable through running "system enviroment variables" as admin and adding the path to ffmpeg to "path." Screenshots for this is located at https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ for older Windows systems, but it is the same for Windows 10, ect.
      For some people, simply adding the ffmpeg.exe file within /bin/ folder from within the same compressed (zip) folder into the directory the script is ran in will work.
      
-------------------------

There's plans to extend this script's functioanlity to other platforms and to work with standard youtube videos.

The reason this exists is because many scripts I've found across the internet have either been so horridly outdated to the point of breaking beyond repair within the bounds of the methods they use or are straight up malicious, and mostly lackluster to begin with.

>>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>>

DO NOT use this to download copyrighted content! I will not endorse it and heavily discourage it.
This script is purely for educational use in figuring out these tools since documentation is a bit lacklaster and broken.
