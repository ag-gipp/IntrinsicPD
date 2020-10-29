$(document).ready(function() {
    var slider = document.getElementById("threshholdSlider");
    var sliderOutput = document.getElementById("sliderValue");

    var currentLocation = location.href;
    var split = currentLocation.split("&threshold=");
    var threshold = split[1].substring(0,3);
    var thresholdSpecial = split[1].substring(0,4);
    if(thresholdSpecial.localeCompare("pc90") == 0){
        slider.value = 0.9;
    }
    else{
        slider.value = parseFloat(threshold);
    }

    sliderOutput.innerHTML = slider.value;
    slider.oninput = function(){
        var displayValue = this.value;
        if(displayValue == 0){
            displayValue = "0." + displayValue;
        }
        if(displayValue == 1){
            displayValue = displayValue + ".0";
        }
        sliderOutput.innerHTML = displayValue;
    };
    slider.addEventListener("mouseup",function(){
        var currentLocation = location.href;
        var split = currentLocation.split("&threshold=");
        var urlEnd =""
        for(i=0;i<split[1].length;i++){
            if((split[1].charAt(i)).localeCompare("&") == 0){
                urlEnd = split[1].substring(i);
                break;
            }
        }
        var newURL = split[0] +"&threshold=" + slider.value + urlEnd;
        location.replace(newURL);
    });
});