function darkenColour(colour) {
    rgba = colour.match(/\d+/g);
    r = parseInt(rgba[0])
    g = parseInt(rgba[1])
    b = parseInt(rgba[2])

    return `rgb(${r + (255 - r)*0.25}, ${g + (255 - g)*0.25}, ${b + (255 - b)*0.25})`
}

$(".button-tracks").each((i, track) => {
    var track_bgcolour = $(track).css("background-color");
    $(track).css("color", getTextColour(track_bgcolour));
    $(track).hover(function() { $(this).css("background-color", darkenColour(track_bgcolour)); },
        function() { $(this).css("background-color", track_bgcolour); });
});