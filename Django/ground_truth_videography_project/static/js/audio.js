var coverart_colour = $(".section-audio").css("background-color");
var textColour = getTextColour(coverart_colour);

$(".heading-audio").css("color", textColour);
$(".paragraph-lines").hover(function() { $(this).css("color", textColour); }, 
    function() { $(this).css("color", "black"); });