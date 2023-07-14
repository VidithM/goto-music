from collect import collect

queries = open('songs.out', 'r')
for ln in queries:
    try:
        collect(ln)
    except(KeyboardInterrupt):
        print('Manually stopped processing')
        break
    except(Exception) as e:
        print('Exception', e, 'while processing song', ln)

queries.close()

'''
import asyncio

'''