from collect import collect

queries = open('songs.out', 'r')
for ln in queries:
    try:
        collect(ln)
    except:
        print('Error while processing', ln)
        continue

queries.close()