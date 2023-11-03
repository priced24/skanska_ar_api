
let building2DArray = []; // array to store building names and their id
let roomArray = []; // store room names and their building id
let sensorArray = []; // store sensor names and their room id

// do when the page loads
window.addEventListener("DOMContentLoaded", function(){

    // GET request for a building
    fetch("/buildings/")
        .then(response => response.json())
        .then(data => {
            data.forEach(function(item) {

                var id = item.id;
                var name = item.name;
                // store building ids
                let row = [];
                row.push(id);
                row.push(name);
                building2DArray.push(row);

                var select = document.getElementById("brDropdown");
                var option = document.createElement("option");
                option.text = name;
                select.appendChild(option);

                var select = document.getElementById("bsDropdown");
                var option = document.createElement("option");
                option.text = name;
                select.appendChild(option);

                var select = document.getElementById("bdDropdown");
                var option = document.createElement("option");
                option.text = name;
                select.appendChild(option);

                var select = document.getElementById("rdbDropdown");
                var option = document.createElement("option");
                option.text = name;
                select.appendChild(option);

            });
        })
        .catch(error => {
            console.error(error);
        });

    // GET request for a room
    fetch("/rooms/")
        .then(response => response.json())
        .then(data => {
            console.log(data)
            
            data.forEach(function(item) {
                var id = item.id;
                var name = item.name;
                var building_id = item.building_id;
                // store building ids
                let row = [];
                row.push(id);
                row.push(name);
                row.push(building_id);
                roomArray.push(row);

                var select = document.getElementById("rDropdown");
                var option = document.createElement("option");
                option.text = name;
                select.appendChild(option);

                var select = document.getElementById("rdrDropdown");
                var option = document.createElement("option");
                option.text = name;
                select.appendChild(option);

                var select = document.getElementById("sdrDropdown");
                var option = document.createElement("option");
                option.text = name;
                select.appendChild(option);
            });
        })
        .catch(error => {
            console.error(error);
        });

    // GET request for a sensor
    fetch("/sensors/")
    .then(response => response.json())
    .then(data => {
        console.log(data)
        
        data.forEach(function(item) {
            var id = item.id;
            var name = item.name;
            var room_id = item.room_id;
            let row = [];
            row.push(id);
            row.push(name);
            row.push(room_id);
            sensorArray.push(row);
        
            var select = document.getElementById("sdsDropdown");
            var option = document.createElement("option");
            option.text = name;
            select.appendChild(option);

        });
    })
    .catch(error => {
        console.error(error);
    });


    // POST for a building
    var bCreate = document.getElementById('bSubmit');
        bCreate.addEventListener('click', function(event){
            event.preventDefault();
            var bName = document.getElementById('bName');
            var bDescription =document.getElementById('bDescription')
            var name = bName.value;
            var description = bDescription.value;

            const formData = {
                name: name,
                description: description
            };
            fetch('/buildings/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (response.ok) {
                    console.log('Data was successfully submitted');
                    alert("Building successfully added.");
                    location.reload();
                } else {
                    console.error('There was a problem submitting the data');
                }
            })
            .catch(error => {
                console.error('There was a network error', error);
            });
        });
    
    // POST for a room
    var rCreate = document.getElementById('rSubmit');
    rCreate.addEventListener('click', function(event){
        event.preventDefault();
        
        var rNumber = document.getElementById('rNumber');
        var rDescription =document.getElementById('rDescription');
        var bName = document.getElementById('brDropdown');
        var number = rNumber.value;
        var description = rDescription.value;
        var name = bName.value;
    
        let buildingID = null;
        for (let i = 0; i < building2DArray.length; i++) {
            if (building2DArray[i][1] === name) {
                buildingID = building2DArray[i][0];
                break;
            }
        }
        const formData = {
            name: number,
            description: description,
            building_id: buildingID
        };
        fetch('/rooms/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                console.log('Data was successfully submitted');
                alert("Room successfully added.");
                location.reload();
            } else {
                console.error('There was a problem submitting the data');
            }
        })
        .catch(error => {
            console.error('There was a network error', error);
        });
    });

    // POST for a sensor
    var sCreate = document.getElementById('sSubmit');
        sCreate.addEventListener('click', function(event){
            event.preventDefault();
            var sName = document.getElementById('sName');
            var sDescription = document.getElementById('sDescription');
            var rDropdown = document.getElementById('rDropdown');
            var bsDropdown = document.getElementById('bsDropdown');
            var name = sName.value;
            var description = sDescription.value;
            var room = rDropdown.value;
            var building = bsDropdown;

            let roomID = null;
            for (let i = 0; i < roomArray.length; i++) {
                if (roomArray[i][1] === room ) {
                    roomID = roomArray[i][0]; 
                    break;
                }
            }
            const formData = {
                room_id: roomID,
                name: name,
                description: description
            };
            console.log(formData)
            
            fetch('/sensors/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (response.ok) {
                    console.log('Data was successfully submitted');
                    alert("Sensor successfully added.");
                    location.reload();
                } else {
                    console.error('There was a problem submitting the data');
                }
            })
            .catch(error => {
                console.error('There was a network error', error);
            });
        });
    
    // DELETE for a building
    var bDelete = document.getElementById('bDelete');
    bDelete.addEventListener('click', function(event){
        event.preventDefault();
        var bName = document.getElementById('bdDropdown');
        var name = bName.value;
        
        var id = -1;
        for (let i = 0; i < building2DArray.length; i++) {
            if (building2DArray[i][1] === name) {
                id = building2DArray[i][0]; 
            }
        }
        const formData = {
            id: id
        };
        console.log(formData);
        fetch('/buildings/' + id, {
            method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (response.ok) {
                    console.log('Data was successfully deleted');
                    alert("Building successfully deleted.");
                    location.reload();
                } else {
                    console.error('There was a problem deleting the data');
                }
            })
            .catch(error => {
                console.error('There was a network error', error);
            });
    });

     // DELETE for a room
     var rDelete = document.getElementById('rDelete');
     rDelete.addEventListener('click', function(event){
         event.preventDefault();
         var rName = document.getElementById('rdrDropdown');
         var name = rName.value;
         var id = -1;
         for (let i = 0; i < roomArray.length; i++) {
             if (roomArray[i][1] === name) {
                 id = roomArray[i][0]; 
             }
         }
         const formData = {
             id: id
         };
         console.log(formData);
         fetch('/rooms/' + id, {
             method: 'DELETE',
                 headers: {
                     'Content-Type': 'application/json'
                 },
                 body: JSON.stringify(formData)
             })
             .then(response => {
                 if (response.ok) {
                     console.log('Data was successfully deleted');
                     alert("Room successfully deleted.");
                     location.reload();
                 } else {
                     console.error('There was a problem deleting the data');
                 }
             })
             .catch(error => {
                 console.error('There was a network error', error);
             });
     });


    // DELETE for a sensor 
    var sDelete = document.getElementById('sDelete');
    sDelete.addEventListener('click', function(event){
        event.preventDefault();
        var rName = document.getElementById('sdrDropdown');
        var room = rName.value;

        var sName = document.getElementById('sdsDropdown');
        var sensor = sName.value;

        var id = -1;
        // match the sensor to its sensor id
         for (let i = 0; i < sensorArray.length; i++) {
             if (sensorArray[i][1] === sensor) {
                    id = sensorArray[i][0]; 
                    
             }
         }

        const formData = {
            id: id

        };
        console.log(formData);
        fetch('/sensors/', {
            method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (response.ok) {
                    console.log('Data was successfully deleted');
                    alert("Sensor successfully deleted.");
                    location.reload();
                } else {
                    console.error('There was a problem deleting the data');
                }
            })
            .catch(error => {
                console.error('There was a network error', error);
            });
    });


})    




