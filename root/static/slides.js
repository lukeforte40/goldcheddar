var slideIndex = 0;
var posts = document.getElementsByClassName('postLink');
showSlide(slideIndex);

function plusSlides(n) {
    if (slideIndex >= 0 && slideIndex <= posts.length - 1){
        slideIndex += n;
        if (slideIndex < 0){
            slideIndex = 0;
        }
        if (slideIndex >= posts.length){
            slideIndex = posts.length -1;
        }
    }
    showSlide(slideIndex)

}

function showSlide(n) {
    var i;
    if (n > 0){
        posts[n - 1].style.display = 'none';
    }
    posts[n].style.display = 'block';
    if(n + 1 < posts.length - 1){
        posts[n + 1].style.display = 'block';
        if(n + 2 < posts.length - 1){
            posts[n + 2].style.display = 'block';
            if(n + 3 < posts.length - 1){
                posts[n + 3].style.display = 'block';
                if(n + 4 < posts.length - 1){
                    posts[n + 4].style.display = 'none';
                }
            }
        }
    }
}