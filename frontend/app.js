let start_button = document.querySelector("#start-button");
let stop_button = document.querySelector("#stop-button");
let camera = document.querySelector("#camera");

camera.style.display = "none";

let canvas = document.createElement("canvas")
let ctx = canvas.getContext("2d")

let mediaDevices = navigator.mediaDevices;
camera.muted = true;

let websocket = null;
let streamInterval = null;

events();

function events(){
    start_button.addEventListener("click" , openCamera);
    stop_button.addEventListener("click" , stopCamera);
}

function openCamera(){
    if(camera.srcObject){
        return;
    }
    
    websocket = new WebSocket("");
    
    camera.style.display = "flex";
    mediaDevices.getUserMedia({
        video: true,
        audio: false,
    }).then((stream)=>{
        camera.srcObject = stream;
        camera.addEventListener("loadedmetadata" , ()=>{
            camera.play();

            canvas.width = 480;
            canvas.height = 360;

            if(streamInterval){
                clearInterval(streamInterval);
            }

            streamInterval = setInterval(()=>{
                ctx.drawImage(camera , 0 , 0 , canvas.width , canvas.height);

                canvas.toBlob((blob) => {
                    if (websocket.readyState === WebSocket.OPEN && blob) {
                        websocket.send(blob);
                    }
                }, "image/jpeg", 0.4);
            } , 80);
        });
    }).catch(alert);
}

function stopCamera(){
    if(streamInterval){
        clearInterval(streamInterval);
        streamInterval = null;
    }

    if(websocket){
        websocket.close();
        websocket = null;
    }

    let stream = camera.srcObject;
    if(!stream){
        return;
    }
    
    let tracks = stream.getTracks();
    tracks.forEach((track) => {
        track.stop();
    });

    camera.srcObject = null;
    camera.style.display = "none";
}