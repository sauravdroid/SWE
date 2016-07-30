opened = false;
$(document).ready(function () {
    $(".menu-ul .menu-item").click(function () {
        if (!opened) {
            $(this).css("background-color", "#F1F4F8");
            $(this).css("height", "340px");
            //$(this).children().first().children().first().addClass('md-active');
            $(this).find( "i" ).addClass('md-active');
            $(this).find( ".header-link" ).css('color','#e91e63');
            //$(this).css("box-shadow","0 4px 8px rgba(0,0,0,0.2)");
            opened = true;
        }else{
            $(this).css("background-color", "#fff");
            $(this).css("height", "60px");
            opened = false;
            //$(this).children().first().children().first().removeClass('md-active')
            $(this).find( "i" ).removeClass('md-active');
            $(this).find( ".header-link" ).css('color','#9DA2A6');
             $(this).css("box-shadow","0 0 0 rgba(0,0,0,0.2)");
        }
        console.log(opened);
    });
    
    $(".sub-menu li").click(function () {
        opened = false;
        console.log($(this).index());
    });
});
