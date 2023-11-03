# Test Data

## Overview
To initialize the database with dummy data the file `test_data.json` can be modified to include JSON serialized model instances. 

## Database Initialization
The database can be initialized with dummy data by running the following command: (The `--dummy` flag can also be replaced with `-d`)

```flask --app api init_db --dummy```

This will output whether each model instances were added successfully, in addtition to any errors that may have occurred during the process. The process will attempt to bulk create all model instances. If an error occurs for one model it will continue to the next.

The `--verbose` or `-v` flags followed by `true` or `false` can be used to remove command line outputs.

## JSON Fromat
The following is the JSON format of the `test_data.json` file:
```
{
    "Building": [
        {
            "name": "building",
            "description": "description"
        }
    ],
    "Room": [
        {
            "name": "room",
            "description": "description",
            "building_id": 1
        }
    ],
    "Sensor": [
        {
            "name": "sensor",
            "description": "description",
            "room_id": 1
        }
    ],
    "SensorReadableData": [
        {
            "name": "sensor_data",
            "description": "description",
            "value": "1",
            "type": "type",
            "sensor_id": 1
        }
    ]
}
```
Root level keys utilize the name of the model for accessible indexing. Records can easily be added by appending JSON objects to the corresponding list.

Records are bulk inserted in the following model order: **Building**, **Room**, **Sensor**, **SensorReadable**