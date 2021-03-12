# Federated Learning Demo server

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

Currently, the server is set up to run at port `7000`.

### Running with docker
Alternatively, you can just run the FL server using the command below:
```bash
docker-compose up --build
```

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

*   GET `/`
    Used to test whether server is alive. It will return `Hello, World!` if invoked. 

*   GET `/get_model`
    Used to get the base model in `.h5` format. 
    Example input: 
    ```
    localhost:7000/get_model 
    ``` 

*   GET `/get_model_weights`
    Used to get the model weights in json format. 
    Example input: 
    ```
    localhost:7000/model_weights 
    ``` 
    
    Example output: 
    ```json
    {
        "error_code": 0,
        "error_message": "",
        "result": {
            "weights": [weights_1,..., weights_n]
        },
        "success": true
    }
    ```

*   POST `update_model_weights`
    Used to update the model based on the aggregated weights. 
    Example input: 
    ```
    localhost:7000/update_model_weights 
    ``` 
    Request input format: 
    ```json
    {
        "weights": [weights_1,..., weights_n],
        "num_party": n
    }
    ```
    Where 
    *   `weights` denotes the weights of each layer as a list of weights. 
    *   `num_party` denotes the number of workers that are participating in the aggregated value.
    
*   GET `evaluate_model`
    Used to evaluate the current model performance (accuracy and loss).
    
    Example input:
    ```
    localhost:7000/evaluate_model 
    ``` 

    Example output:
    ```json
    {
        "error_code": 0,
        "error_message": "",
        "result": {
            "loss": 0.1,
            "accuracy": 0.95
        },
        "success": true
    }
    ```