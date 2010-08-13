//<![CDATA[
$(document).ready(function() {
    var gYellowIcon = new google.maps.MarkerImage(
        "http://labs.google.com/ridefinder/images/mm_20_yellow.png",
        new google.maps.Size(12, 20),
        new google.maps.Point(0, 0),
        new google.maps.Point(6, 20));
    var gRedIcon = new google.maps.MarkerImage(
        "http://labs.google.com/ridefinder/images/mm_20_red.png",
        new google.maps.Size(12, 20),
        new google.maps.Point(0, 0),
        new google.maps.Point(6, 20));
    var gSmallShadow = new google.maps.MarkerImage(
        "http://labs.google.com/ridefinder/images/mm_20_shadow.png",
        new google.maps.Size(22, 20),
        new google.maps.Point(0, 0),
        new google.maps.Point(6, 20));
    
    var geocoder = new google.maps.Geocoder();
    var gLocalSearch = new GlocalSearch();
    var localSearchCenter = business_city+", "+business_province+", "+business_country+", "+business_zipcode;
    if (geocoder) {
        geocoder.geocode({ 'address': clean_address }, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                //alert(results[0].geometry.location.lat())
                //alert(results[0].geometry.location.lng())
                geocode_lat = results[0].geometry.location.lat();
                geocode_lng = results[0].geometry.location.lng();
                //Create the Map and center to geocode results latlong
                var latlng = new google.maps.LatLng(geocode_lat, geocode_lng);
                var myOptions = {
                    zoom: 13,
                    center: latlng,
                    mapTypeId: google.maps.MapTypeId.ROADMAP
                };

                map = new google.maps.Map(document.getElementById("map_canvas"),
                    myOptions);
                    
                gLocalSearch.setCenterPoint(localSearchCenter);
                gLocalSearch.setSearchCompleteCallback(this, OnLocalSearch);
                
                gLocalSearch.execute(business_name);
                console.log("string_location: {{string_location}}");
            } 
            else {
                $('#map_message').append('<div class="error">Google could not find the address you are looking for. So, we will display a Google Adsense here instead.</div>');
                //alert('No results found. Check console.log()');
                console.log("Geocoding address: " + address);
                console.log("Geocoding failed: " + status);
            }
        });
    }
    
    /*
    Other functions        
    */      
    function OnLocalSearch() {
        var results = gLocalSearch.results;
        
        console.log("results: "+gLocalSearch.results);
        console.log("results length: "+ results.length);
        
        //alert("business_name.soundex(): "+business_name.soundex()+" results[1].titleNoFormatting: "+results[0].titleNoFormatting.soundex());
        
        if (results[0]) {
            $.each(results, function(i, n){
                console.log("result ["+i+"]: "+n);
                if ((business_name.soundex() == results[i].titleNoFormatting.soundex())) {
                    //alert("business_name.soundex(): "+business_name.soundex()+" results.titleNoFormatting: "+results[i].titleNoFormatting.soundex());
                    var marker = new google.maps.Marker({
                        position: new google.maps.LatLng(results[i].lat,results[i].lng), 
                        map: map, 
                        title: results[i].streetAddress,
                        icon: gRedIcon,
                        shadow: gSmallShadow
                    });
                    centerNewLat = results[i].lat;
                    centerNewLng = results[i].lng;
                } else {
                    var marker = new google.maps.Marker({
                        position: new google.maps.LatLng(results[i].lat,results[i].lng), 
                        map: map, 
                        title: results[i].streetAddress,
                        icon: gYellowIcon,
                        shadow: gSmallShadow
                    });
                }
                
                var the_content = displayInfoWindow(results[i]);
                
                infowindow = new google.maps.InfoWindow({maxWidth: 200});
                
                google.maps.event.addListener(marker, 'click', function() {
                   infowindow.setContent(the_content);
                   infowindow.open(map, marker);
                   infowindow.setMaxWidth(100);
                });
                
                //Only used for debugging.
                $.each(n, function(j, k) {
                    console.log(" > result ["+j+"]: "+k);
                });
                
                
            });
            
            // Move map to center if Red Marker is found. If not, set to first result
            if(centerNewLat && centerNewLng) {
                map.setCenter(new google.maps.LatLng(parseFloat(centerNewLat),
                                                     parseFloat(centerNewLng)));
            } else {
                map.setCenter(new google.maps.LatLng(parseFloat(results[0].lat),
                                                     parseFloat(results[0].lng)));
            }
            
            //callbackFunction(point); 
        }else{ 
            $('#map_message').append('<div class="error">Sorry we could not find the business you are looking for. We will try to find a way so that you can add it in Google Local Search.</div>');
            //alert("business name not found!"); 
        } 
    }
    
    $("#add_marker").click(function() {
        //alert("Add a marker!");
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(geocode_lat, geocode_lng), 
            map: map, 
            title: "New Marker",
            draggable: true
        });
        
        //Display infoWindow when marker is clicked
        google.maps.event.addListener(marker, 'click', function() {
           infowindow.setContent("<div id='infowindow_title'>"+business_name+"</div><div id='infowindow_content'>Content. Data from pop-up will display here.</div><input type='button' value='Save Marker'/>");
           infowindow.open(map, marker);
        });
        
        //Event when you dropdown a map
        google.maps.event.addListener(marker, "dragend", function() {
            var marker_location = marker.getPosition();
            map.panTo(marker_location);
            
            //for now we log into the console
            console.log("marker lat: "+marker_location.lat());
            console.log("marker lng: "+marker_location.lng());
        });
    });
    
    function displayInfoWindow(current_result) {
        return ""+current_result.title +"<br/><span class='infowindow_small'>"+current_result.addressLines+"<br/><a href='"+current_result.url+"'>Place</a><span>";
    }
    
}); /*End jQuery onLoad here.*/
//]]>