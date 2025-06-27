import yt_dlp
x = input()
yt_dlp.YoutubeDL({'format' : '1080p', 'outtmpl': '%(title)s.%(ext)s'}).download([x])
