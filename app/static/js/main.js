$(document).ready(function () {
    console.log("Hello........")
    $('.form-control-label').addClass("c-field__label");
    $('input[type=text], input[type=password], input[type=file], input[type=date]').addClass('c-input')
    $('input[type=submit]').addClass('c-btn c-btn--fullwidth c-btn--info');
    $('select').addClass('c-select__input');
    $('.form-group').addClass('c-field');
});