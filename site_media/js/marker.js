//<![CDATA[
/**
Dynamically add a marker into map.
*/
$(document).ready(function() {
    
    $("#show_add_marker").click(function() {
        $('#add_business_container').dialog('open');
    });
    
    $("#add_business_container").dialog({
        autoOpen: false,
        height: 300,
        width: 350,
        modal: true,
    });
    
    $("#add_marker").click(function(){
        $('#add_business_container').dialog('close');
    });
    
});

//]]>