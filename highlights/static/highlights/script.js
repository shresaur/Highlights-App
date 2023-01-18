//highlights current playing video from the playlist
document.addEventListener('DOMContentLoaded', function() {
    let el2 = document.querySelector('.iframe')
    document.querySelectorAll('img').forEach(function(img) {
        link = img.dataset.link
        if (link == el2.dataset.vidlink)
            img.style.border = 'solid orange 2px'
    });
});

//toggle notice thread
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.fa-solid').onclick = function() {
        const x = document.querySelector('.indexnotice')
        const y = document.getElementById("toggle")
        if (x.style.display ==="none") {
            x.style.display = "block";
            y.className = "fa-solid fa-angle-up";
            }
        else {
            x.style.display = "none";
            y.className = "fa-solid fa-angle-down";
            }
    }
});