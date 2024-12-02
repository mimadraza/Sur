let currentMusic = 0;
const music = document.querySelector('#audio');
const seekBar = document.querySelector('.seek-bar');
const currentTime = document.querySelector('.current-time');
const musicDuration = document.querySelector('.song-time');
const playBtn = document.querySelector('.play-btn');
const forwardBtn = document.querySelector('.forward-btn');
const backwardBtn = document.querySelector('.backward-btn');

playBtn.addEventListener('click' , () => {
    if (playBtn.className.includes('pause')){
        music.play();
    }else{
        music.pause();
    }
    playBtn.classList.toggle('pause');
    disk.classList.toggle('play');
})

const setMusic = (audioURL) => {
    seekBar.value = 0;
    playSong('Song 1');
    music.src = audioURL; 
    currentTime.innerHTML = '00:00';
    setTimeout(() => {
        seekBar.max = music.duration;
        musicDuration.innerHTML = formatTime(music.duration);
    }, 300)
}


const formatTime = (time) => {
    let min = Math.floor(time / 60);
    if (min < 10) {
        min = `0${min}`; // Use backticks for template literals
    }
    let sec = Math.floor(time % 60);
    if (sec < 10) {
        sec = `0${sec}`; // Use backticks for template literals
    }
    return `${min}:${sec}`; // Use backticks here as well
}


setInterval(() => {
    seekBar.value =music.currentTime;
    currentTime.innerHTML = formatTime(music.currentTime);
},500)

function playSong(songName) {
    fetch(`/get_music_from_backend/${songName}`)
        .then(response => response.blob())  // Response as a blob (binary data)
        .then(data => {
            const audioURL = URL.createObjectURL(data);  // Create a URL for the audio blob
            setMusic(audioURL);

        })
        .catch(error => console.error('Error fetching song:', error));

    
}