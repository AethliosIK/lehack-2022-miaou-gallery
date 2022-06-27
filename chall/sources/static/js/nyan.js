window.onload = function() {
    var posX = 100, posY = 100, px = 0, py = 0, an = false;
    var nyan = $('.nyan');

    $(document).on('mousemove', function( event ) {
      posX = event.pageX;
      posY = event.pageY;
    })

    function moveNyan()
    {
        var tamX = nyan.width()/2,
          tamY = nyan.height()/2;
        px += (posX - px - tamX) / 20 + 1;
        py += (posY - py - tamY) / 20 + 1;

        nyan.css({
          left: px + 'px',
          top: py + 'px'
        });
    }

    window.setInterval(function(){
      moveNyan();
    }, 10);

    window.setInterval(function(){ an = !an; }, 500);
}
