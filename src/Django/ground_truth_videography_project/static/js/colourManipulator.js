function getTextColour(rgba) {
    rgba = rgba.match(/\d+/g);
    if ((rgba[0]*0.299) + (rgba[1]*0.587) + (rgba[2]*0.114) > 186)
        return 'black';
    else
        return 'white';
}

function hoverColour(colour, factor=1) {
    rgba = colour.match(/\d+/g);
    r = parseInt(rgba[0])
    g = parseInt(rgba[1])
    b = parseInt(rgba[2])

    // Lighten/Darken colour depending on the darkness of the colour
    if ((rgba[0]*0.299) + (rgba[1]*0.587) + (rgba[2]*0.114) > 186)
        return `rgb(${r*0.75*factor}, ${g*0.75*factor}, ${b*0.75*factor})`;
    else
        return `rgb(${r + (255 - r)*0.25*factor}, ${g + (255 - g)*0.25*factor}, ${b + (255 - b)*0.25*factor})`;
}