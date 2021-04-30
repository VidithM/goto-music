from collect import collect

queries = open('songs.out', 'r')
for ln in queries:
    collect(ln)

queries.close()