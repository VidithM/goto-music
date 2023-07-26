import pyaudio
import math, random
import numpy as np 
import find_peaks as fp
from search_tree import SearchTree

from pydub import AudioSegment

import time

SAMPLE_DURATION = 10000 # Length of the audio/video samples

THRESH_LOWER = 0.6      # Lower bound on amount of improvement in similarity of audio/video sample to register a new start point
THRESH_UPPER = 8.0      # Upper bound on amount of improvement described above

JUMP_LOWER = 200        # Lower bound on amount to jump in milliseconds for each video sample
JUMP_UPPER = 800        # Upper bound on amount to jump in milliseconds for each video sample

# lower and upper bounds are used to compute a corresponding value for the current sample. As the sampling proceeds, the values
# shift quadratically towards the upper bound.

AUDIO_SAMPLE_OFFSET = 5000  # Offset from the start of the audio for the audio sample
MAX_SAMPLE_TIME = 120000    # Upper bound on timestamp in the video to be sampled

NPEAKS_THRESH = 150

'''
TODO:
It seems that incorrect results can be produced when the start of the music video is quiet
    - Possible reason: Poor fingerprint on the spectrogram?
    - Solutions: ignore samples with low peak counts

Also should consider altering the audio sample to start at a point that has a good number of peaks
(if start of song is quiet, for example)
'''

'''
Finds the time at which the closest match between a computed audio sample and a sliding video sample occurrs
'''
def match(audio_name, mv_name):
    audio_file = AudioSegment.from_file(audio_name)[AUDIO_SAMPLE_OFFSET : (SAMPLE_DURATION + AUDIO_SAMPLE_OFFSET)]
    mv_file = AudioSegment.from_file(mv_name)
    
    data = np.frombuffer(audio_file._data, np.int16)
    
    audio_channels = []
    audio_sparse_maps = [] # freq/time mappings of amp peaks in spectogram

    for i in range(audio_file.channels):
        audio_channels.append(data[i::audio_file.channels])

    for channel_data in audio_channels:
        smap = fp.get_sparse_map(channel_data, audio_file.frame_rate)
        audio_sparse_maps.append(list(smap))

    l = 0
    length = min(MAX_SAMPLE_TIME, mv_file.duration_seconds * 1000)
    best = None
    mn = -1

    while((l + SAMPLE_DURATION) <= length):
        sample = mv_file[l : (l + SAMPLE_DURATION)]
        progress = l / length
        curr_thresh = (THRESH_UPPER - THRESH_LOWER) * (progress ** 2) + THRESH_LOWER

        sample_channels = []
        sample_sparse_maps = []

        data = np.frombuffer(sample._data, np.int16)
        for i in range(sample.channels):
            sample_channels.append(data[i::sample.channels])

        for channel_data in sample_channels:
            smap = fp.get_sparse_map(channel_data, mv_file.frame_rate)
            sample_sparse_maps.append(list(smap))

        try:
            init = time.time() * 1000
            curr = difference(audio_sparse_maps, sample_sparse_maps)
        except(Exception) as e:
            print('Encountered exception', e, 'while sampling')
            exit()
    
        if((mn == -1) or ((curr > 0) and (mn - curr >= curr_thresh))):
            mn = curr 
            best = l 

        print(curr, l)    
        l += (JUMP_UPPER - JUMP_LOWER) * (progress ** 2) + JUMP_LOWER

    return (best - AUDIO_SAMPLE_OFFSET, mn)

def difference(audio_maps, sample_maps):
    mean_offset = 0
    mean_npeaks = 0
    map_cnt = min(len(audio_maps), len(sample_maps))
    for i in range(map_cnt):
        mean_offset += offset(audio_maps[i], sample_maps[i])
        mean_npeaks += len(sample_maps[i])

    mean_npeaks /= map_cnt
    if(mean_npeaks < NPEAKS_THRESH):
        # Do not consider this sample as valid; not enough peaks (too quiet)
        return float('inf')
    
    return (mean_offset / map_cnt)


def offset(mapA, mapB):
    init = time.time() * 1000
    mean_dist = 0
    st = SearchTree()
    #print('sizes:',len(mapA), len(mapB))
    random.shuffle(mapA) #Reduce tree height
    for i in mapA:
        #print(i[0], i[1])
        st.push(i[0], i[1])
    #print('building done. Time was', (time.time() * 1000 - init))
    init = time.time() * 1000
    for j in mapB:
        #print(j, st.query(j[0], j[1], False))
        res = st.query(j[0], j[1], False)
        mean_dist += res[0]
    
    #print('query end. Time was', (time.time() * 1000 - init), 'Visited count:', res[1])
    
    return (mean_dist / len(mapB))
