

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

//load vids without loading entire webpage

function showSection(section) {
    fetch(`/worldcuptest/${section}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        let el2 = document.querySelector('.iframe');
        el2.src = `https://www.youtube.com/embed/${section}`;
        el2.dataset.vidlink = section
        const el1 = document.querySelectorAll('#videoimage');
        el1.forEach(function(el1) { //highlights current playing video from the playlist
            link = el1.dataset.link
            if (link == section)
                el1.style.outline = 'solid orange 2px'
            else
                el1.style.outline = 'none'
            });
        document.querySelector('#maintitle').innerHTML = data.title;
        document.querySelector('#maindesc').innerHTML = data.description;
       });
    }


document.addEventListener('DOMContentLoaded', function() {
    const el1 = document.querySelectorAll('#videoimage')
    el1.forEach(function(el1) {
        el1.onclick = function() {
            showSection(el1.dataset.link)
        }
    });
});
