if (document.images) {
    var imagePlus = new Image(9,9);
    var imageMinus = new Image(9,9);
    imagePlus.src = "/++static++/Products.SilvaPhotoGallery/plus.gif";
    imageMinus.src = "/++static++/Products.SilvaPhotoGallery/minus.gif";
}

function toggleElement(id) {
    var element = document.getElementById('txt'+id);
    var image = document.getElementById('img'+id)

    if ( element.style.display == "none" ) {
        element.style.display = "block";
        image.src = imageMinus.src;
    } else {
        element.style.display = "none";
        image.src = imagePlus.src;
    }
}
