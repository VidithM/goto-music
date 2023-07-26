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
var processed = false;

async function jump(){
    processed = true;
    let url = window.location.href;
    console.log('Checking ' + url);
    currUrl = url;
    let id = "";
    let extra = "";
    if(url.indexOf("&") != -1){
        id = url.substring(url.indexOf('?v=') + 3, url.indexOf("&"));
        extra = url.substring(url.indexOf("&"));
    } else {
        id = url.substring(url.indexOf("?v=") + 3);
    }
    console.log(id);
    let quiet = false;
    if(url.includes("&t=")){
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
            let player = document.getElementsByClassName('video-stream html5-main-video')[0];
            player.currentTime = (start / 1000);
        } else {
            if(!quiet){
                alert('Video not in database')
            }
        }
    });
}

async function monitorURL(){
    let url = window.location.href;
    if(url.includes("?v=")){
        if(url != currUrl){
            console.log('url change ' + url);
            processed = false;
        }
        if(processed){
            return;
        }
        await jump();
    }
}

setInterval(monitorURL, 1000);


//Handle requests for new song
chrome.runtime.onMessage.addListener((msg, from, response) => {
    alert('received msg from background');
    if(msg == "add-song"){
        response("ok");
    }
});



