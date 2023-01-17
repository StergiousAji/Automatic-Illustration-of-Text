$(".button-tracks").each((i, track) => {
    var track_bgcolour = $(track).css("background-color");
    $(track).css("color", getTextColour(track_bgcolour));
    $(track).hover(function() { $(this).css("background-color", hoverColour(track_bgcolour)); },
        function() { $(this).css("background-color", track_bgcolour); });
});