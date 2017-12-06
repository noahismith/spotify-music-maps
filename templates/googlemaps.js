function initMap() {
var uluru = {lat: -25.363, lng: 131.044};
var map = new google.maps.Map(document.getElementById('map'), {
  zoom: 4,
  center: uluru
});

var contentString = 'hi';

var infowindow = new google.maps.InfoWindow({
  content: contentString
});

var marker = new google.maps.Marker({
  position: uluru,
  map: map,
  title: 'Uluru (Ayers Rock)'
});
marker.addListener('click', function() {
  infowindow.open(map, marker);
});
return map;
}
