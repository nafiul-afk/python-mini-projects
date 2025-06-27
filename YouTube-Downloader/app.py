import yt_dlp
x = input("Enter the URL: ")
yt_dlp.YoutubeDL({'format' : '1080p', 'outtmpl': '%(title)s.%(ext)s'}).download([x])
