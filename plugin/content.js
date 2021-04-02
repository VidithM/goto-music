var firebaseConfig = {
    apiKey: "AIzaSyDjfdc64v44B1fecsZSc_TBj4sJPzaCi-g",
    authDomain: "goto-music-c98e1.firebaseapp.com",
    databaseURL: "https://goto-music-c98e1-default-rtdb.firebaseio.com/",
    projectId: "goto-music-c98e1",
    storageBucket: "goto-music-c98e1.appspot.com",
    messagingSenderId: "902734405248",
    appId: "1:902734405248:web:634ed7548a8e562f335065"
};
firebase.initializeApp(firebaseConfig);
var db = firebase.database();
var ref = db.ref('songs')

var url = window.location.href;
var id = url.substr(url.indexOf('?v=') + 3);
var quiet = false;
if(id.includes("&t=")){
    quiet = true;
}

var start = -1;

ref.once("value", (snapshot) => {
    snapshot.forEach((child) => {
        if(child.key == id){
            start = child.val();
        }
    });
}).then(() => {
    console.log(start);
    if(start != -1){
        window.location.replace('https://youtube.com/watch?v=' + id + '&t=' + (Math.floor(start/1000)));
    } else {
        if(!quiet){
            alert('Video not in database')
        }
    }
});
