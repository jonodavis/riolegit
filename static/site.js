$(function () {
    $('.without-russia').hide();
    $('#myonoffswitch').change(function () {
        var $this = $(this);
        var $russia = $('.russia');
        var numbersBelow = $russia.nextAll().children('.number');
        if ($this.prop('checked')) {
            if (!$russia.hasClass('struck-through')) {
                $russia.addClass('struck-through');
                numbersBelow.each(function () {
                    var $this = $(this);
                    $this.html(parseInt($this.html()) - 1);
                });
            }
            $russia.addClass('struck-through');
            $('.result.with-russia').slideUp(function () {
                $('.result.without-russia').slideDown();
            });
        } else {
            if ($russia.hasClass('struck-through')) {
                numbersBelow.each(function () {
                    var $this = $(this);
                    $this.html(parseInt($this.html()) + 1);
                });
            }
            $('.result.without-russia').slideUp(function () {
                $('.result.with-russia').slideDown(function() {
                    $russia.removeClass('struck-through');
                });
            });
        }
    });
});