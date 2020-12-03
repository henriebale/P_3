import os, sys, subprocess, shlex, re
from subprocess import call
def create_container(filename):
    # extract audio mono and lower bitrate
    command1=f"ffmpeg -i {filename} -ss 00:00:00 -t 00:01:00 -ac 1 -b:a 32k -map a BBB_audio_cut_mono.mp3"
    # replace audio and apply subtitles
    command2=f"ffmpeg -i {filename} -i BBB_audio_cut_mono.mp3 -i subtitles.srt -ss 00:00:00 -t 00:01:00  -c:v copy -c:a aac -c:s mov_text subtitles.mp4"
    os.system(command1)
    os.system(command2)


 # extract audio and video codec and find the broadcasting standard adequate
def get_standard(filename):
    # extract audio and video codec
    p1 = subprocess.Popen(f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {filename}", stdout=subprocess.PIPE, shell=True)
    (vout, err) = p1.communicate()
    p2 = subprocess.Popen(f"ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {filename}", stdout=subprocess.PIPE, shell=True)
    (aout, err) = p2.communicate()
    print("Broadcasting standards: ")
    std=0
    # find the broadcasting standard adequate
    if (vout == b'h264\n' or vout == b'mpeg2video\n' ) and (aout == b'aac\n' or aout == b'mp1\n' or aout == b'mp2\n' or  aout == b'mp3\n' or aout == b'ac3\n'):
        print("DVB")
        std+=1
    if (vout == b'h264\n' or vout == b'mpeg2video\n' ) and (aout == b'aac\n'):
        print("ISDB")
        std += 1
    if (vout == b'h264\n' or vout == b'mpeg2video\n' ) and (aout == b'ac3\n'):
        print("ATSC")
        std += 1
    if (vout == b'h264\n' or vout == b'mpeg2video\n' ) and (aout == b'aac\n' or aout == b'mp1\n' or aout == b'mp2\n' or  aout == b'mp3\n' or aout == b'ac3\n'):
        print("ATSC")
        std += 1
    if std==0:
        print("ERROR")


class video:
    #initialize with the video codec h264 and the audio codec aac
    video_codec="b'h264\n'"
    audio_codec="b'aac\n'"

    # name is the filename os the mp4
    def __init__(self, name):
        self.name = name

    def get_codecs(self):
        p1 = subprocess.Popen(f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {self.name}",
            stdout=subprocess.PIPE, shell=True)
        (self.video_codec, err) = p1.communicate()
        p2 = subprocess.Popen(f"ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {self.name}",
            stdout=subprocess.PIPE, shell=True)
        (self.audio_codec, err) = p2.communicate()

    def get_standard(self):
        print("Broadcasting standards: ")
        std = 0
        if (self.video_codec == b'h264\n' or self.video_codec == b'mpeg2video\n') and (self.video_codec == b'aac\n' or self.video_codec == b'mp1\n' or self.video_codec == b'mp2\n' or self.video_codec == b'mp3\n' or self.video_codec == b'ac3\n'):
            print("DVB")
            std += 1
        if (self.video_codec == b'h264\n' or self.video_codec == b'mpeg2video\n') and (self.video_codec == b'aac\n'):
            print("ISDB")
            std += 1
        if (self.video_codec == b'h264\n' or self.video_codec == b'mpeg2video\n') and (self.video_codec == b'ac3\n'):
            print("ATSC")
            std += 1
        if (self.video_codec == b'h264\n' or self.video_codec == b'mpeg2video\n') and (self.video_codec == b'aac\n' or self.video_codec == b'mp1\n' or self.video_codec == b'mp2\n' or self.video_codec == b'mp3\n' or self.video_codec == b'ac3\n'):
            print("ATSC")
            std += 1
        if std == 0:
            print("ERROR")

    def create_container(self):
        command1 = f"ffmpeg -i {self.name} -ss 00:00:00 -t 00:01:00 -ac 1 -b:a 32k -map a BBB_audio_cut_mono.mp3"
        command2 = f"ffmpeg -i {self.name} -i BBB_audio_cut_mono.mp3 -i subtitles.srt -ss 00:00:00 -t 00:01:00  -c:v copy -c:a aac -c:s mov_text subtitles.mp4"
        os.system(command1)
        os.system(command2)

    def test_sandard(self):

        os.system(f"ffmpeg -i {self.name} -acodec mp3 test_mp3.mp4")
        print("test_mp3.mp4")
        get_standard("test_mp3.mp4")

        os.system(f"ffmpeg -i {self.name} -acodec ac3 test_ac3.mp4")
        print("test_mp3.mp4")
        get_standard("test_mp3.mp4")

        os.system(f"ffmpeg -i {self.name} -vcodec mpeg2video test_mpeg2.mp4")
        print("test_mpeg2.mp4")
        get_standard("test_mp3.mp4")



ex="1"
while ex != "0":
    print("Exercice Nº (insert 0 to end)")
    ex=input()
    print(f"Exercise {ex} selected")
    if ex=="1":
       create_container("BBB_video.mp4")

    elif ex=="2":
        print("Select file:")
        filename = input()
        create_container(filename)

    elif ex=="3":
        print("Select file:")
        filename = input()
        get_standard(filename)

    elif ex=="4":
        os.system("ffmpeg -i BBB_video.mp4  -acodec mp3 BBB_video_mp3.mp4")
        print("BBB_video_mp3.mp4")
        get_standard("BBB_video_mp3.mp4")

        os.system("ffmpeg -i BBB_video.mp4  -acodec ac3 BBB_video_ac3.mp4")
        print("BBB_video_mp3.mp4")
        get_standard("BBB_video_ac3.mp4")

        os.system("ffmpeg -i BBB_video.mp4  -vcodec mpeg2video BBB_video_mpeg2.mp4")
        print("BBB_video_mpeg2.mp4")
        get_standard("BBB_video_mpeg2.mp4")

    elif ex == "5":
        v=video("BBB_video.mp4")
        v.create_container()
        v.get_codecs()
        v.get_standard()
        v.test_sandard()

    else:
        print(f"Exercise {ex} doesn't exiat")



