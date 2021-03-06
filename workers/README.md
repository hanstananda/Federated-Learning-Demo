# Federated Learning Workers service

## Prerequisites
1. Python 3 (Tested on Python 3.7)

## Running the project

1.  Install the library requirements from pip
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the python script
    ```
    python run_server.py
    ```
    
Currently, there will be two workers set up at port `7101` and `7102` respectively.

### Running a single worker 
Alternatively, if you want to run just a single worker, you can use another script `run_single_server.py`. 
```bash
python run_single_server.py --port=7101 
```
Note: Change 7101 to your desired port for the worker. 

### Running with docker
Alternatively, you can just run the worker service using the command below:
```bash
docker-compose up -f docker-compose-worker1.yml --build
docker-compose up -f docker-compose-worker2.yml --build
```

Currently, those each worker has its own docker-compose file so that it can be started/stopped independently.

## APIs 

The current APIs available in this server:
*   GET `/get_params`
    Used to get the parameters for this server
    Example input:
    ```
    localhost:7200/get_params 
    ``` 

    Example output:
    ```json
    {
        "error_code": 0,
        "error_message": "",
        "result": {
            "scheme": "FL plain"
        },
        "success": true
    }
    ```

*   GET `/train`
    Used to train the model and send the weights after training to the aggregator service. 
    Currently set to only train for 1 epoch using MNIST dataset. 
    
    Example input: 
    ```
    localhost:7101/train 
    ``` 
    
    Example output: 
    ```json
    {
        "error_code": 0,
        "error_message": "",
        "success": true
    }
    ```

*   GET `/reload_weight`
    Used to reload the weight of the model in the worker based on the current weights in the server. 
    Used for synchronization / debugging purposes. 
    The underlying function will be called during each time `/train` API is called as well.
    
    Example input: 
    ```
    localhost:7101/reload_weight 
    ``` 
    
     Example output: 
    ```json
    {
        "error_code": 0,
        "error_message": "",
        "success": true
    }
    ```
    