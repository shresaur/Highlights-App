document.addEventListener('DOMContentLoaded', function() {
    let el2 = document.querySelector('.iframe')
    document.querySelectorAll('img').forEach(function(img) {
        link = img.dataset.link
        if (link == el2.dataset.vidlink)
            img.style.border = 'solid orange 2px'
    });
});