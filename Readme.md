# MASHUP-WEB APP TO MAKE MASHUP OF SONGS
## 1. Description

The web application allows users to create mashup songs by providing the singer's name and specifying the desired number of songs to include. It retrieves songs from YouTube, merges them together using audio processing libraries, and then sends the resulting mashup to the user via email in MP3 format.

## How to use this
Just enter the name of singer, length of each song and no of videos to extract audio.
Enter e-mail id on which you want result as zip file.

## Work Flow of Code
1. User inputs the singer's name, number of videos, desired duration, output file name, and email address in the web interface.
2. The user submits the form.
3. The code checks for various input validation and error handling:
   - It checks if the output file format is ".mp3".
   - It validates the email address.
   - It ensures that the number of videos and duration are integers and greater than zero.
4. The code then proceeds to scrape YouTube for videos related to the singer's name and specified keywords (e.g., "songs," "new songs").
5. It downloads the selected videos, filtering them by length (between 2 to 6 minutes) and storing them as both MP4 and MP3 files.
6. The MP3 files are then sliced to the desired duration (EndSec) and saved.
7. All the processed audio clips are concatenated into a final mashup.
8. The mashup is saved as an MP3 file and compressed into a ZIP file called "Mashup.zip."
9. The code sends the ZIP file as an email attachment to the user's specified email address.
10. The temporary MP3 and MP4 files, as well as the ZIP file, are deleted.
11. A success message is displayed to the user.






