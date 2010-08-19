//<![CDATA[
/**
Dynamically add a marker into map.
*/
$(document).ready(function() {
    
    /**
     * validation rules and messages for the form
     * This should more or less match the validation in forms.py
     */
    $("#add_business_form").validate({
        rules: {
            name: {
                required: true,
                minlength: 2
            },
            website: {
                url: true,
                minlength: 2
            }
        },
        messages: {
            name: {
                required: "Please enter a Business Name",
                minlength: "Your Business Name must consist of at least 2 characters"
            },
            website: {
                url: "You need to input a valid URL.",
                minlength: "URL length not valid."
            }
        },
        
        submitHandler: function(form) {
            add_marker();
            $('#add_business_container').dialog('close');
        }
    });
    
    /**
     * Start Dialog box methods
     */
    $("#show_add_marker").click(function() {
        $('#add_business_container').dialog('open');
    });
    
    $("#add_business_container").dialog({
        autoOpen: false,
        height: 300,
        width: 350,
        modal: true,
    });
    /**
     * End Dialog box methods
     */
    
    $("#save_marker").click(function(){
        //this won't work because the DOM elements are created dynamically
    });
    
    
    
    /**
     * add_marker()
     * Adds the marker in the middle of the map
     * "Reads" the values found in the add_business_container form elements 
     */
    function add_marker() {
        var container = $('#add_business_container')
        
        /*Store values from textboxes using jQuery data storage*/
        container.data("title", $("#id_name").val());
        container.data("website", $("#id_website").val());
        container.data("address1", $("#id_address1").val());
        container.data("address2", $("#id_address2").val());
        container.data("city", $("#id_city").val());
        container.data("province", $("#id_province").val());
        container.data("country", $("#id_country").val());
        container.data("zipcode", $("#id_zipcode").val());
        
        marker = new google.maps.Marker({
            position: map.getCenter(), 
            map: map, 
            title: container.data("title"),
            draggable: true
        });
        
        //Display infoWindow when marker is clicked
        if(infowindow) {
            google.maps.event.addListener(marker, 'click', function() {
            infowindow.setContent("<div id='infowindow_title'>"+container.data("title")+"</div>"+
                                 "<div id='infowindow_content'>"+
                                 container.data("address1")+" "+
                                 container.data("address2")+" "+
                                 container.data("city")+" "+
                                 container.data("province")+" "+
                                 container.data("country")+" "+
                                 container.data("zipcode")+" "+
                                 "</div><input type='button'  id='save_marker' value='Save Marker'/>");
                                 /* "</div><input type='button'  id='save_marker' onclick='save_data(this)' value='Save Marker'/>");*/
            infowindow.open(map, marker);
            });
        }
        
        //Event when you dragend a marker
        google.maps.event.addListener(marker, "dragend", function() {
            var marker_location = marker.getPosition();
            map.panTo(marker_location);
            
            //for now we log into the console everytime we dragend a marker
            console.log("marker lat: "+marker_location.lat());
            console.log("marker lng: "+marker_location.lng());
        });
        
        //once the marker is added, trigger a click on the marker to display the infowindow
        google.maps.event.trigger(marker, "click")
    }
    
    $('#save_marker').live('click', function() {
        //haven't figured out to make this work with dynamically created DOM elements yet
        $(this).attr('disabled','disabled');
        $(this).val('Saving...');
        //alert("Saved!");
        save_data();
        //alert('Good!');
        $(this).val('Saved');
    });
    
    
    
    /**
     * save_data(obj)
     * obj: The DOM of #save_marker button
     * Saves data inside the add_business_container 
     */
    function save_data() {
        $.post("/business/add/", { 
            csrfmiddlewaretoken: $("input[name='id_csrfmiddlewaretoken").val(),
            name: $("#id_name").val(),
            website: $("#id_website").val(),
            category: $("#id_category").val(),
            address1: $("#id_address1").val(),
            address2: $("#id_address2").val(),
            city: $("#id_city").val(),
            province: $("#id_province").val(),
            zipcode: $("#id_zipcode").val(),
            country: $("#id_country").val(),
            phone: $("#id_phone").val(),
            credit_card: $("#id_credit_card").val(),
            alcohol: $("#id_alcohol").val(),
            kids: $("#id_kids").val(),
            groups: $("#id_groups").val(),
            reservations: $("#id_reservations").val(),
            waiters: $("#id_waiters").val(),
            outdoor_seating: $("#id_outdoor_seating").val(),
            wheelchair: $("#id_wheelchair").val(),
            attire: $("#id_attire").val(),
            takeout: $("#id_takeout").val(),
            parking_open: $("#id_parking_open").val(),
            parking_basement: $("#id_parking_basement").val(),
            parking_private_lot: $("#id_parking_private_lot").val(),
            parking_valet: $("#id_parking_valet").val(),
            parking_validated: $("#id_parking_validated").val(),
            parking_street: $("#id_parking_street").val(),
            open_time: $("#id_open_time").val(),
            close_time: $("#id_close_time").val(),
        },
        function(data) {
                data = json_parse(data);
                //$('#add_business_container').dialog('close');
                if(data.status=="success") {
                    //add_marker();
                    //$(obj).attr('disabled','disabled');
                    //$(obj).val('Saving...');
                    //alert("Saved!");
                    //$(obj).val('Saved!');
                    //$(obj).hide();
                    return true;
                } else {
                    //alert('An error occured while adding the marker. Please contact the site administrator.');
                    console.log("status: "+data.status)
                    console.log("error: "+data.error)
                    console.log("POST DATA: "+data.data)
                    $.each(data.data, function(i, n){
                        console.log(">"+i+": "+n);
                    });
                    return false;
                }
        });
    }
}); 
/*End jQuery load*/
//]]>