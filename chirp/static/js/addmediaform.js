$('#addmedia').click(function(){
    var formnum = parseInt($("#justfornum").val());
    $("[name=form-TOTAL_FORMS]").val(formnum+1);
    $("[name=form-INITIAL_FORMS]").val(0);
    html = $("#form_template").clone().html().replace(/__prefix__/g,formnum);
    $('#forms').append(html);

    // create a preview box
    $.uploadPreview({
        input_field: "#id_form-" + formnum + "-media",   // Default: .image-upload
        preview_box: "#image-preview-" + formnum,  // Default: .image-preview
    });
    // update value
    $("#justfornum").val(formnum+1);
});