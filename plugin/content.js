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

var currUrl = "";
var inDb = true;

async function jump(){
    let url = window.location.href;
    currUrl = url;
    let id = url.substr(url.indexOf('?v=') + 3);
    let quiet = false;
    if(id.includes("&t=")){
        return;
    }

    let start = -1;

    ref.once("value", (snapshot) => {
        snapshot.forEach((child) => {
            if(child.key == id){
                if(child.val() >= 5000){
                    start = child.val();
                } else {
                    quiet = true;
                }
            }
        });
    }).then(() => {
        if(start != -1){
            window.location.replace('https://youtube.com/watch?v=' + id + '&t=' + (Math.floor(start/1000)));
        } else {
            inDb = false;
            if(!quiet){
                alert('Video not in database')
            }
        }
    });
}

async function monitorURL(){
    let url = window.location.href;
    console.log(url);
    if(url.includes("?v=")){
        if(url != currUrl){
            inDb = true;
        }
        if(!inDb){
            return;
        }
        await jump();
    }
}

setInterval(monitorURL, 1000);



