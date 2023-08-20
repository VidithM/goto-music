import time
from collect import collect

queries = open('songs.out', 'r')
for ln in queries:
    try:
        start = time.perf_counter()
        collect(ln)
        end = time.perf_counter()
        print('Time:', end - start)
    except(KeyboardInterrupt):
        print('Manually stopped processing')
        break
    except(Exception) as e:
        print('Exception', e, 'while processing song', ln)

queries.close()

'''
import asyncio
'''