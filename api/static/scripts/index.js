const apiKey= 'pk.eyJ1IjoibWFjaGlkYTIzIiwiYSI6ImNsZHdlZDh3ZzA2bmgzd255YWIyMGhjNzgifQ.Yzt9c34PQEXmJ033T0gKEw'

const map = L.map('map').setView([45.57205066141388, -122.72710950218752], 17);

// add Mapbox tile to Leaflet
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 18,
    id:'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: apiKey
}).addTo(map);


let buildingArray=[]; // stores the building name and id
let roomArray=[]; // store the building id, index is the room id
let sensorArray=[]; // store the room id


window.addEventListener("DOMContentLoaded", function(){

    const buildingRequest = fetch("/buildings/");
    const roomRequest = fetch("/rooms/");
    const sensorRequest = fetch("/sensors/");

    Promise.all([buildingRequest, roomRequest, sensorRequest])
    .then(responses => {
        return Promise.all(responses.map(response => response.json()));
    })
    .then(data => {
        data[0].forEach(function(item) {
            var id = item.id;
            var name = item.name;
            let row = [];
            row.push(id);
            row.push(name);
            buildingArray.push(row);
        });
        shileyID = getBuildingId("Shiley Hall");
        shileyRoom = countRooms(shileyID);
        shileySensor = countSensors(shileyID);

        data[1].forEach(function(item) {
            var building_id = item.building_id;
            let row = [];
            row.push(building_id);
            roomArray.push(row);
        });

        data[2].forEach(function(item) {
            var room_id = item.room_id;
            let row = [];
            row.push(room_id);
            sensorArray.push(row);
        });


        // helper function to find a building ID
        function getBuildingId(buildingName) {
            for (let i = 0; i < buildingArray.length; i++) {
            if (buildingArray[i][1] === buildingName) { 
                return buildingArray[i][0];
            }
            }
            return null;
        }

        // helper function to count the number of rooms in a building
        function countRooms(buildingID){
            var roomCount = 0;
            for (let i = 0; i < roomArray.length; i++) {
                if (roomArray[i][0] === buildingID) { 
                    roomCount++;
                }
            }
            return roomCount;
        }

        // helper function to count the number of sensors in a building
        function countSensors(buildingID){
            var sensorCount = 0;
            for (let i = 0; i < roomArray.length; i++) {
                if (roomArray[i][0] === buildingID) { 
                    for(let k = 0; k < sensorArray.length; k++){
                        if(sensorArray[k][0] === i){
                            sensorCount++;
                        }
                    }
                }
            }
            return sensorCount;
        }
        
        // Hardcoded Buildings

        // shiley
        var shileyID = getBuildingId("Shiley Hall");
        console.log("shileyID: " + shileyID);
        var shileyRoom = countRooms(shileyID);
        console.log("shileyRoom: "+shileyRoom);
        var shileySensor = countSensors(shileyID);
        console.log("shileySensor: "+shileySensor);
        const shileyMarker = L.marker([45.571848938613435, -122.7278813862825]).addTo(map);
        shileyMarker.bindPopup('Shiley Hall: ' + shileyRoom + ' Rooms, ' + shileySensor + ' Sensors');


        // franz 
        var franzID = getBuildingId("Franz Hall");
        var franzRoom = countRooms(franzID);
        var franzSensor = countSensors(franzID);
        const franzMarker = L.marker([45.57266302976268, -122.72771671767558]).addTo(map);
        franzMarker.bindPopup('Franz Hall: ' + franzRoom + ' Rooms, ' + franzSensor + ' Sensors');

        // buckley
        var buckleyID = getBuildingId("Buckley Center");
        var buckleyRoom = countRooms(buckleyID);
        var buckleySensor = countSensors(buckleyID);
        const buckleyMarker = L.marker([45.572013298699794, -122.72605677627351]).addTo(map);
        buckleyMarker.bindPopup('Buckley Center: ' + buckleyRoom + ' Rooms, ' + buckleySensor + ' Sensors');

        // dundon-berchtold
        var dbID = getBuildingId("Dundon-Berchtold Hall");
        var dbRoom = countRooms(dbID);
        var dbSensor = countSensors(dbID);
        const dbMarker = L.marker([45.57255894054325, -122.72495923471004]).addTo(map);
        dbMarker.bindPopup('Dundon-Berchtold Hall: ' + dbRoom + ' Rooms, ' + dbSensor + ' Sensors');

        // shiley-marcos
        var smID = getBuildingId("Shiley-Marcos Center");
        var smRoom = countRooms(smID);
        var smSensor = countSensors(smID);
        const smMarker = L.marker([45.57212561076955, -122.7291196117254]).addTo(map);
        smMarker.bindPopup('Shiley-Marcos Center:  ' + smRoom + ' Rooms, ' + smSensor + ' Sensors');

    });
})
