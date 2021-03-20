import pyaudio
import fingerprint as fp
from pydub import AudioSegment
import numpy as np 


END = 10000 #Sample for 10 seconds

def match(audio_name, mv_name):
    audio_file = AudioSegment.from_file(audio_name)[0:END]
    mv_file = AudioSegment.from_file(mv_name)
    
    data = np.frombuffer(audio_file._data, np.int16)
    
    audio_channels = []
    audio_hashes = set()

    for i in range(audio_file.channels):
        audio_channels.append(data[i::audio_file.channels])
    
    for channel_data in audio_channels:
        hashes = fp.fingerprint(channel_data, audio_file.frame_rate, plots=False)
        audio_hashes.add(hashes)

    l = 0
    len = mv_file.duration_seconds
    best = None
    max = 0

    while((l + END) <= len):
        sample = mv_file[l:(l + END)]
        sample_channels = []
        sample_hashes = set()
        
        data = np.frombuffer(sample._data)
        for i in range(sample.channels):
            mv_channels.append([i::sample.channels])

        for channel_data in sample_channels:
            hashes = fp.fingerprint(channel_data, mv_file.frame_rate,plots=False)
            sample_hashes.add(hashes)
        
        curr = similarity(audio_hashes, sample_hashes)
        if(curr > max):
            max = curr 
            best = l 
    
    return l 

def similarity(audio_hashes, sample_hashes):
    pass


match('audio_only.webm', 'music_video.m4a')