## Fast the audio or slow down the video

ffmpeg -i '../Results/sample_audio.wav' -filter:a "atempo=1.23" -vn '../Results/speed_up_audio.wav'

# ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono:sample_rate=22050 -t 242 -q:a 9 -acodec libmp3lame out.mp3

## Append the audio and the video
ffmpeg -i ../'Speed of Sound _ Mechanical waves and sound _ Physics _ Khan Academy.mp4' -i '../Results/speed_up_audio.wav' -c:v copy -map 0:v:0 -map 1:a:0 '../Results/new_video2.mp4'