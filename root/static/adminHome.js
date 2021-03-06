var pNum = 2;
var pDNum = 1;
var iNum = 1;
var vNum = 1;
var pos = 1;
var slideIndex = 0;
var posts = document.getElementsByClassName('postLink');
showSlide(slideIndex);

function openTab(tab){
    var tabs = document.getElementsByClassName('tabs')
    for (var i = 0;i<tabs.length;i+=1){
        tabs[i].style.display = 'none';
    }
    document.getElementById(tab).style.display = 'block';
    elements = document.getElementsByClassName('forms')
    if (tab == 'makePost') {
        for (var i = 0;i<elements.length;i+=1){
            elements[i].style.display = 'none';
        }
        document.getElementById('postStyles').style.display = 'block';
    }
    if (tab == 'viewPosts'){
        document.getElementById('viewPosts').style.display = 'flex';
    }
}

function show(formType){
    var elements = document.getElementsByClassName('forms')
    for (var i = 0;i<elements.length;i+=1){
        elements[i].style.display = 'none';
    }
    document.getElementById(formType).style.display = 'flex';
    document.getElementById('postStyles').style.display = 'none';
}

function add(inType){
    switch(inType){
        case 'p':
            var div = document.createElement("div");
            div.id = 'p' + pNum.toString() + 'div'; 
            var texta = document.createElement("textarea");
            texta.id = "par" + pNum.toString();
            texta.cols = "30";
            texta.rows = "1";
            texta.name = 'p' + pNum.toString(); 
            var title = document.createElement("label");
            title.htmlFor = 'p' + pNum.toString();
            var text = document.createTextNode('Paragraph ' + pNum + ":");
            title.appendChild(text);
            document.getElementById('content1').appendChild(div);
            document.getElementById('p' + pNum.toString() + 'div').appendChild(title);
            document.getElementById('p' + pNum.toString() + 'div').appendChild(texta);
            pNum += 1;
            break;
        case 'pDyn':
            var pdiv = document.createElement("div");
            pdiv.id = 'pD' + pDNum.toString() + 'div'; 
            var texta = document.createElement("textarea");
            texta.id = "parD" + pDNum.toString();
            texta.cols = "30";
            texta.rows = "1";
            texta.name = 'pD' + pDNum.toString() + '_' + pos.toString(); 
            var title = document.createElement("label");
            title.htmlFor = 'pD' + pDNum.toString() + '_' + pos.toString();
            var text = document.createTextNode('Paragraph ' + pDNum + ":");
            title.appendChild(text);
            document.getElementById('content2').appendChild(pdiv);
            document.getElementById('pD' + pDNum.toString() + 'div').appendChild(title);
            document.getElementById('pD' + pDNum.toString() + 'div').appendChild(texta);
            pDNum += 1; 
            pos += 1;     
            break;
        case 'i':
            var idiv = document.createElement("div");
            idiv.id = 'i' + iNum.toString() + 'div'; 
            var img = document.createElement("input");
            img.id = "i" + iNum.toString();
            img.type = 'file';
            img.name = 'i' + iNum.toString() + '_' + pos.toString(); 
            var title = document.createElement("label");
            title.htmlFor = 'i' + iNum.toString();
            var text = document.createTextNode('Image ' + iNum + ":");
            title.appendChild(text);
            document.getElementById('content2').appendChild(idiv);
            document.getElementById('i' + iNum.toString() + 'div').appendChild(title);
            document.getElementById('i' + iNum.toString() + 'div').appendChild(img);
            iNum += 1;   
            pos += 1;     
            break;
        case 'v':
            var vdiv = document.createElement("div");
            vdiv.id = 'v' + vNum.toString() + 'div'; 
            var vid = document.createElement("input");
            vid.id = "v" + vNum.toString();
            vid.type = 'file';
            vid.name = 'v' + vNum.toString() + '_' + pos.toString(); 
            var title = document.createElement("label");
            title.htmlFor = 'v' + vNum.toString();
            var text = document.createTextNode('Video ' + vNum + ":");
            title.appendChild(text);
            document.getElementById('content2').appendChild(vdiv);
            document.getElementById('v' + vNum.toString() + 'div').appendChild(title);
            document.getElementById('v' + vNum.toString() + 'div').appendChild(vid);
            vNum += 1;
            pos += 1;    
            break;
    }
    return inType;
}

function plusSlides(n) {
    if (slideIndex >= 0 && slideIndex < posts.length - 1){
        slideIndex += n;
        if (slideIndex < 0){
            slideIndex = 0
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