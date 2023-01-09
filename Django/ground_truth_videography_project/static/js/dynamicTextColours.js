function getTextColour(rgba) {
    rgba = rgba.match(/\d+/g);
    if ((rgba[0]*0.299) + (rgba[1]*0.587) + (rgba[2]*0.114) > 186)
        return 'black';
    else
        return 'white';
}