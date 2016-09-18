// this programme creates the color scroller which is an overview of all the font colors used in the text
// which can then be used to scroll through the text
///  author:seenu.andi-rajendran
(function ( $ ) {



    $.fn.colorScroller = function( options ) {

        var settings = $.extend({
            replaceBlack: 'rgb(83, 84, 72)',
            colorScrollClass: "color-map",
            overlayClass: "overlay",
            scrollSectionClass: "mapSection",
            coloredTextClass: "passage"
        }, options );



      var container = this;
      // getting the height of container
      var containerHeight = container.outerHeight(true);
      // creating overlay scrolling element
      var $overlay = $('<div class="'+settings.overlayClass+'" ></div>')
      //creating container for colored parts
      var $colorScroll=$('<div class="'+settings.colorScrollClass+'" ></div>')
      // appending colormap element after container in DOM
      container.after($colorScroll);
      // approximate total height of browser vertical scroll buttons
      var browserScrollButtons = 26;
      // setting height of colorscroll element to the height of container
      $colorScroll.outerHeight(container.outerHeight()-browserScrollButtons );

      var scrollerHandleMin = 31



      // here calculating the total height of text elements of container
      var totalHeight = 0;
      container.children('.'+ settings.coloredTextClass).each(function(){
        totalHeight = totalHeight + $(this).outerHeight(true);
      });

      // calculate height of  text empty elements like br or <p></p>
      var emptyHeight = 0;
      container.children().not('.'+ settings.coloredTextClass).each(function(){
        emptyHeight = emptyHeight + $(this).outerHeight(true);
      });


      // calculating the ratio b/n total height of children of container and the height of color-scroll element
      var ratio = totalHeight/$colorScroll.outerHeight();
      // create a jquery object containing of small divs which will be colored, and associated with each passage div in container
      var $mini = $('.'+settings.coloredTextClass, container).map(function(){

        var heightPassage=$(this).outerHeight(true)/ratio+'px';
        // getting the color of passage
        var colorPassage=$(this).css('color');
        // color change if color is black
        if (colorPassage=='rgb(0, 0, 0)')
          colorPassage = settings.replaceBlack;

        var elem = $('<div class="'+settings.scrollSectionClass+'" style="height:'+heightPassage+'; background-color:'+colorPassage+'" ></div>').get(0)

        return  elem
      });

      // get approximate height of browser scroll bar  handle
      var browserScrollBarHeight = (containerHeight*(containerHeight-browserScrollButtons ))/(totalHeight + emptyHeight )
      browserScrollBarHeight = browserScrollBarHeight >  scrollerHandleMin ? browserScrollBarHeight : scrollerHandleMin

      // set overlay scroller height to browser scroll handle height
      $overlay.outerHeight(browserScrollBarHeight);
      var overlayHeight = $overlay.outerHeight();

      // appending the minified elements into colorscroll element
      $($mini).appendTo($colorScroll);

      // appending overlay element into color-scroll element
      $colorScroll.append($overlay);

      // getting top position of container related to document top
      var colorScrollTop = $colorScroll.offset().top+1+parseInt($colorScroll.css('margin-top').replace('px', ''))

      // getting multiple to create algorithm for converting top positions
      var k = (totalHeight + emptyHeight - containerHeight)/($colorScroll.innerHeight()-overlayHeight)


      // attaching draggable to overlay scrolling element, so that it can be moved along color scroll element
      $overlay.draggable({
        // constrain movement to color-scroll element only
        containment: "."+settings.colorScrollClass,
        // what to do when overlay is dragged
        drag: function() {
          // getting top position of overlay related to document top
          var top = $(this).offset().top;

          console.log('k  ' , k )
          container.animate({
            // scroll container vertically to the point of overlay top (related to color-scroll element ) associated with text in container
            scrollTop: (top-colorScrollTop)*k +'px'
          }, 5)

        },

        drop: function() {
          // getting top position of overlay related to document top
          var top = $(this).offset().top;
          container.animate({
            // scroll container vertically to the point of overlay top (related to color-scroll element ) associated with text in container
            scrollTop: (top-colorScrollTop)*k +'px'
          }, 2)
        }

      });

        $colorScroll
          .mouseenter(function() {
            $overlay.draggable('enable')
            container.off('scroll',  scrollText)
          })
          .mouseleave(function() {
            $overlay.draggable('disable')
            container.on('scroll',  scrollText)
          });
      // function triggered when container scrolled, basically scroll the overlay
      function  scrollText(){
              $overlay.animate({
                top: container.scrollTop()/k + 'px'
              }, 1)
       }
      container.on('scroll',  scrollText)

      // when the color-scroll element is clicked
      $colorScroll.on('click',function(e){
        // calculate the position of click related to color-scroll itself
        var topPosition = e.pageY-$(this).offset().top;

        $overlay.animate({
          top: topPosition+'px'
        }, 200)

        container.animate({
          scrollTop: (topPosition+overlayHeight)*ratio-containerHeight+'px'
        }, 10)
      })



      return container;

    };

}( jQuery ));

///  end plugin

$(document).ready(function() {
  var passes = [0, 1, 2, 3, 4, 5, 6]

  for (var i in passes) {
    col = document.getElementById('pass' + i).style.color;
    var element = document.createElement("section");
    element.style.background = col;

    document.getElementById("left").appendChild(element);
  }
  canvas = document.createElement("canvas");
  canvas.id = 'canvas';
  canvas.style = 'height:700px;width:50px;';

///   init plugin function
  $('#document_content').colorScroller({replaceBlack: 'rgb(0,0,0)'});

   /// the other option with defaults are :
//         colorScrollClass: "color-map", css class of colored scrollbar
//         overlayClass: "overlay",       css class of the custom scrollbar
//         scrollSectionClass: "mapSection",  css class of the small colored sections in colored scroll bar
//         coloredTextClass: "passage"     css class of the original text part
///

});
