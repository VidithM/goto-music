async function requestAddSong(){
    let tab = (await chrome.tabs.query({active: true, currentWindow: true}))[0];
    chrome.tabs.sendMessage(tab.id, 'add-song', (msg) => {
        let status = msg.status;
        let content = msg.content;
        if(status == 'FAILED'){
            //if(content == )
        }
    });
}

console.log(document.);