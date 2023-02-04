// progressbar


var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var player;
function onYouTubeIframeAPIReady() {
   player = new YT.Player("ytplayer", {
    events: {
      'onStateChange': onPlayerStateChange
    }
  });
}

document.addEventListener('DOMContentLoaded', function() {
    const el1 = document.querySelectorAll('#videoimage');
    let resumeTime = 0;
    el1.forEach(function(el1) {
        el1.onclick = function() {
            player.pauseVideo();
            if (el1.dataset.link in savedTimes) {
                resumeTime = savedTimes[el1.dataset.link];
                console.log(resumeTime)
            } else {
                resumeTime = 0;
            }
            player.cueVideoById({ 'videoId': el1.dataset.link, 'startSeconds': resumeTime });
            player.playVideo();
            showSection(el1.dataset.link, el1.dataset.page);
        };
    });
});


let savedWidths = JSON.parse(localStorage.getItem("savedWidths")) || {};
let savedTimes = JSON.parse(localStorage.getItem("savedTimes")) || {};

function onPlayerStateChange(event) {

  display = document.getElementById('displaytest');
  let el2 = document.querySelector('.iframe');
  const el1 = document.querySelectorAll('.episodeprogressbar');
  el1.forEach(function(el1) {
      link = el1.dataset.link
      if (link === el2.dataset.vidlink ) {
        pauseTime = player.getCurrentTime();
        watchedPercent = (player.getCurrentTime()/player.getDuration() * 100) + "%";
        savedWidths[link] = watchedPercent;
        savedTimes[link] = pauseTime;
        el1.style.width = watchedPercent;
      } else {
        el1.style.width = savedWidths[link] || '0%';
      }
  });
  localStorage.setItem("savedWidths", JSON.stringify(savedWidths));
  localStorage.setItem("savedTimes", JSON.stringify(savedTimes));
}

//toggle notice thread
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.fa-solid').onclick = function() {
        const x = document.querySelector('.toggle-notice')
        const y = document.getElementById("toggle")
        if (x.style.display === "none") {
            x.style.display = "block";
            y.className = "fa-solid fa-angle-up";
            }
        else {
            x.style.display = "none";
            y.className = "fa-solid fa-angle-down";
            }
    }
});

//load vids without loading entire webpage

function showSection(section, page) {
    fetch(`/watch/${page}-${section}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        let el2 = document.querySelector('.iframe');
        //el2.src = `https://www.youtube.com/embed/${section}?enablejsapi=1`;
        el2.dataset.vidlink = section
        const el1 = document.querySelectorAll('#videoimage');
        el1.forEach(function(el1) { //highlights current playing video from the playlist
            link = el1.dataset.link
            if (link == section)
                el1.style.outline = 'solid #CF9FFF 2px'
            else
                el1.style.outline = 'none'
            });
        document.querySelector('#maintitle').innerHTML = data.title;
        document.querySelector('#maindesc').innerHTML = data.description;
        document.querySelector('#date').innerHTML = `Published on ${data.date}`
       });
    }


