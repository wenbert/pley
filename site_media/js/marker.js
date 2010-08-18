//<![CDATA[
/**
Dynamically add a marker into map.
*/
$(document).ready(function() {
    
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
            $.post("/business/add/", { 
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']")val(),
                name: $("#id_name").val(),
                website: $("#id_website").val(),
                category: $("#id_category").val(),
                address1: $("#id_address1").val(),
                address2: $("#id_address2").val(),
                city: $("#id_city").val(),
                province: $("#id_province").val(),
                country: $("#id_country").val(),
                zipcode: $("#id_zipcode").val(),
                phone_number: $("#id_phone_number").val()
            },
            function(data) {
                    data = json_parse(data);
                    $('#add_business_container').dialog('close');
                    if(data.status=="success") {
                        add_marker();
                    } else {
                        alert('An error occured while adding the marker. Please contact the site administrator.');
                        console.log("error: "+data.error)
                        console.log("POST: "+data.data)
                    }
            });
            
        }
    });
    
    
    $("#show_add_marker").click(function() {
        $('#add_business_container').dialog('open');
    });
    
    $("#add_business_container").dialog({
        autoOpen: false,
        height: 300,
        width: 350,
        modal: true,
    });
    
    $("#add_marker").click(function(){});
    
    function add_marker() {
        var container = $('#add_business_container')
        
        //container.dialog('close');
        
        /*Store values from textboxes*/
        container.data("title", $("#id_name").val());
        container.data("website", $("#id_website").val());
        container.data("address1", $("#id_address1").val());
        container.data("address2", $("#id_address2").val());
        container.data("city", $("#id_city").val());
        container.data("province", $("#id_province").val());
        container.data("country", $("#id_country").val());
        container.data("zipcode", $("#id_zipcode").val());
        
        var content = "test"
        
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
                                 "</div><input type='button' value='Save Marker'/>");
            infowindow.open(map, marker);
            });
        }
        
        
        //Event when you dropdown a map
        google.maps.event.addListener(marker, "dragend", function() {
            var marker_location = marker.getPosition();
            map.panTo(marker_location);
            
            //for now we log into the console
            console.log("marker lat: "+marker_location.lat());
            console.log("marker lng: "+marker_location.lng());
        });
        
        //once the marker is added, display immediately the infowindow
        google.maps.event.trigger(marker, "click")    
    }
    
});

//]]>