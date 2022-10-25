const ip_endpoint = 'http://ip-api.com/json/?fields=status,message,country,city,query';
const xhr = new XMLHttpRequest();

xhr.open('GET', ip_endpoint, true);
xhr.send();

xhr.getLocation = function(checkboxElem) {
    if (checkboxElem.checked) {
        let response = JSON.parse(this.responseText);
        let insertCountry = confirm(`Do you want to enter ${response.city}, ${response.country} as your country?`);
        if (insertCountry === true) {
            document.getElementById('address').defaultValue = `${response.city}, ${response.country}`;
        }
        if (response.status !== 'success') {
            alert(`We weren't able to identify your location.`)
        }
    }
}