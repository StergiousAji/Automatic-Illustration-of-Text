var coverart_colour = $(".section-audio_subheading").css("background-color");
var textColour = getTextColour(coverart_colour);

$(".subheading-audio").css("color", textColour);
$("#parText").css("color", textColour);


$(".section-audio_subheading").hover(function() { $(this).css("background-color", hoverColour(coverart_colour, 1.1)); }, 
    function() { $(this).css("background-color", coverart_colour); });

$(".section-timestamp").css("background-color", hoverColour(coverart_colour, 1.1));
$("#parTimestamp").css("color", textColour);