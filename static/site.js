$(function() {
    $('#myonoffswitch').change(function() {
        var $this = $(this);
        if($this.prop('checked')) {
            $('.result.with-russia').hide();
            $('.result.without-russia').show();
        } else {
            $('.result.without-russia').hide();
            $('.result.with-russia').show();
        }
    });
});