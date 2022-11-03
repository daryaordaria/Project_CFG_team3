const ip_endpoint = 'http://ip-api.com/json/?fields=status,message,country,city,lat,lon,query';
const xhr = new XMLHttpRequest();

xhr.open('GET', ip_endpoint, true);
xhr.send();

xhr.getLocation = function(checkboxElem) {
    if (checkboxElem.checked) {
        let response = JSON.parse(this.responseText);
        let insertCountry = confirm(`Do you want to enter the coordinates of ${response.city}, ${response.country} as your address?`);
        if (insertCountry === true) {
            document.getElementById('address').defaultValue = `${response.lat}, ${response.lon}`;
        }
        if (response.status !== 'success') {
            alert(`We arent't able to identify your location. Please, enter your address manually.`)
        }
    }
}