# Federated Learning Demo 

## Subproject division

This project is further divided to 3 different subproject to handle different party roles in the network. Namely: 
*   Server  
    Located under `server`. By default, the server will be hosted on port `7000`.
*   Workers  
    Located under `workers`. By default, it will spawn two workers with port `7101` and `7102`. 
*   Aggregator  
    Located under `Aggregator`. By default, the server will be hosted on port `7200`.

Please refer to the respective subprojects' readme for more information. 

## Usage guide 
1.  Start the `server`, followed by `workers` and `aggregator` respectively. 
2.  To start training, go to any worker endpoints and invoke the `/train` API.
    ```
    localhost:7101/train 
    ```
    The training is currently set to perform 1 training epoch. 
    Afterwards, it will automatically send the resulting encrypted weight to the Aggregator service. 
3.  After the workers have finished their training, you can invoke the `/agg_val` API on the Aggregator service 
    to aggregate the weights and transfer it to the server. 
    ```
    localhost:7200/agg_val 
    ```
4.  To check the current accuracy of the model stored in the server, we can use the `/evaluate_model` API. 
    ```
    localhost:7000/evaluate_model
    ```
    You will get a json response containing current test accuracy and loss value, which looks something like this: 
    ```json
    {
        "error_code": 0,
        "error_message": "",
        "result": {
            "accuracy": 0.9749000072479248,
            "loss": 0.08522004634141922
        },
        "success": true
    }
    ```
    

### Model Used
The model description is located under `server/model/` package. 
The current model is built based on the [Keras Simple MNIST Convnet](https://keras.io/examples/vision/mnist_convnet/) example, which is:
```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d (Conv2D)              (None, 26, 26, 32)        320       
_________________________________________________________________
max_pooling2d (MaxPooling2D) (None, 13, 13, 32)        0         
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 11, 11, 64)        18496     
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 5, 5, 64)          0         
_________________________________________________________________
flatten (Flatten)            (None, 1600)              0         
_________________________________________________________________
dropout (Dropout)            (None, 1600)              0         
_________________________________________________________________
dense (Dense)                (None, 10)                16010     
=================================================================
Total params: 34,826
Trainable params: 34,826
Non-trainable params: 0
_________________________________________________________________

```