def push(db, id, start):
    curr = db.child('songs').get().val()
    curr[id] = start
    db.child('songs').set(curr)