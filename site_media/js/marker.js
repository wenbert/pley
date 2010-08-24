//<![CDATA[
/**
Dynamically add a marker into map.
*/
$(document).ready(function() {    
    $("#add_mark_button").click(function() {
        put_marker();
    });
    
    /**
     * put_marker()
     * Just adds a marker.
     */
     function put_marker() {
         marker = new google.maps.Marker({
            position: map.getCenter(), 
            map: map, 
            title: $("#business_name").val(),
            draggable: true
        });
        
        //Display infoWindow when marker is clicked
        if(infowindow) {
            google.maps.event.addListener(marker, 'click', function() {
            infowindow.setContent("<div id='infowindow_title'>"+$("#business_name").val()+"</div>"+
                                 "<div id='infowindow_content'>"+
                                 $("#business_address").val()+
                                 "</div><input type='button'  id='save_marker' value='Save Marker'/>");
            infowindow.open(map, marker);
            });
        }
        
        //Event when you dragend a marker
        google.maps.event.addListener(marker, "dragend", function() {
            var marker_location = marker.getPosition();
            map.panTo(marker_location);
            
            $('#business_lat').val(marker_location.lat());
            $('#business_lng').val(marker_location.lng());
        });
        
        //once the marker is added, trigger a click on the marker to display the infowindow
        google.maps.event.trigger(marker, "click")
     }
    
    $('#save_marker').live('click', function() {
        $(this).attr('disabled','disabled');
        $(this).val('Saving...');
        if(store_data()) {
            $(this).val('Saved');
        } else {
            alert('Error. Please contact site administrator.');
        }
        
    });
    
    /**
     * store_data()
     * Save the LatLng of the marker
     */
    function store_data() {
        $.post("/business/save_latlng/"+$("#business_id").val()+"/", {
            csrfmiddlewaretoken: $("input[name='id_csrfmiddlewaretoken").val(),
            lat: $('#business_lat').val(),
            lng: $('#business_lng').val()
         }, function(data) {
            data = json_parse(data);
            if(data.status=="success") {
                return true;
            } else {
                console.log("status: "+data.status)
                console.log("error: "+data.error)
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