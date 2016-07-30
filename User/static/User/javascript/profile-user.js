$(document).ready(function () {
    var opened = false;
    //$('.user-sub-header').css('height','0');
    $('#settings_link').click(function () {
        if(!opened) {
            $('.user-sub-header').css('transform', 'scale(1,1)');
            opened = true;
        }else{
            $('.user-sub-header').css('transform', 'scale(1,0)');
            opened = false;
        }
    });
});