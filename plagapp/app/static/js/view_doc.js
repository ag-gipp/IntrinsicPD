
$(document).ready(function() {

    var lastClicked;
    var flag;
    function updateFeatureBox(text) {
        $('#feature_box').html(text);
    };

    function affixWidth() {
        // Using an affix messes with the width/styling of 
        // the sidebar -- this makes sure that the panel maintains
        // its proper width
        // Thanks to:
        // https://github.com/twbs/bootstrap/issues/6350#issuecomment-16069663
        // for the fix
        var affix = $('#feature_panel');
        var width = affix.width();
        affix.width(width);
    }

    affixWidth();

    $('.passage').click(function() {
        // Highlight the clicked passage
        if(lastClicked !== undefined) {
            lastClicked.css("border-style", "none");
        }

        $(this).css("border-style", "inset");
        lastClicked = $(this);

        updateFeatureBox($(this).attr('features'));
    });

});
