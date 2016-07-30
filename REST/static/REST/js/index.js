/*$(document).ready(function () {
 $('form.ajax').on('submit', function () {
 var that = $(this),
 url = that.attr('action'),
 method = that.attr('method'),
 data = {};
 that.find('[name]').each(function (index, value) { //Find anything with the value of name
 var that = $(this),
 name = that.attr('name'),
 value = that.val();
 data[name] = value;

 });
 console.log(data);
 $.ajax({
 url: url,
 type: method,
 data: data,
 success: function (response) {
 console.log(response)
 }
 });
 return false;,
 })
 });*/

$(document).ready(function () {
    $(document).on('submit', '#submit_form', function (e) {
        e.preventDefault();
        var url = $(this).attr('action'),
            method = $(this).attr('method');
        var data = {};
        $(this).find('[name]').each(function (index, value) {
            var name = $(this).attr('name'),
                value = $(this).val();
            data[name] = value;
        });
        $.ajax({
            type: method,
            url: url,
            data: data,
            success: function (response) {
                console.log(response)
            }
        });
    });
});

var Bike = function () {
    var gear;
    this.getGear = function () {
        return gear;
    };
    this.setGear = function (gearValue) {
        gear = gearValue;
    };
};