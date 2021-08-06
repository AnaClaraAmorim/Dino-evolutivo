from tkinter import Canvas, Tk, mainloop, NW, Label, Frame, W
import numpy as np


def calcLayersAxis(width, nn_shape, padding):
    #the avaliable space on the x axis
    avaliable_x = (width - (padding[1] + padding[3]))
    
    x_offset = int(avaliable_x/len(nn_shape))
    layers_axis_x = []
    for index, layer in enumerate(nn_shape, start=0):
        layers_axis_x.append((index*x_offset)+padding[3])
    return layers_axis_x
def calcNeuronsAxisY(height, nn_shape, padding):
    #the avaliable space on the y axis
    avaliable_y = (height - (padding[0] + padding[2]))
    max_n_neurons = max(nn_shape)
    y_offset = int(avaliable_y/max_n_neurons)
    neurons_axis_y = []
    for i in range(0, max_n_neurons+1):
        neurons_axis_y.append((y_offset*i)+padding[0])
    return neurons_axis_y
def calcNeuronsAxis(width, height, nn_shape, padding = [10, 10, 10, 10]):
    layers_axis_x = calcLayersAxis(width, nn_shape, padding)
    neurons_axis_y = calcNeuronsAxisY(height, nn_shape, padding)
    return {
        'layers': layers_axis_x,
        'neurons': neurons_axis_y
    }
def combineAxis(neurons_axis, nn_shape, neuron_size):
    layers_axis = neurons_axis['layers']
    neurons_axis_y = neurons_axis['neurons']
    max_neurons = max(nn_shape)
    axis = []
    for i, layer_size in enumerate(nn_shape):
        top_empty_spaces = 0
        empty_spaces = max_neurons - layer_size
        if(empty_spaces%2==0):
            top_empty_spaces = int(empty_spaces/2)
        else:
            top_empty_spaces = int((empty_spaces-1)/2)
        for j in range(0, layer_size):
            axis.append([layers_axis[i], 
                        neurons_axis_y[top_empty_spaces+j], 
                        layers_axis[i]+neuron_size, 
                        neurons_axis_y[top_empty_spaces+j]+neuron_size])
    return axis

def drawNeurons(combined_axis, canvas, fill = "#000"):
    neuron_ids = []
    for axis in combined_axis:
        neuron_ids.append(canvas.create_oval(axis[0], axis[1], axis[2], axis[3], fill="#000"))
    return neuron_ids
def drawConnections(canvas, combined_axis, nn_shape, neuron_size, weights_flatten, fill = "#000"):
    n_layers = len(nn_shape)
    count = 0
    connection_count = 0
    weights_normalized = normalize(weights_flatten)
    connection_ids = []
    print(weights_normalized)
    for i, layer in enumerate(nn_shape):
        if(i!=n_layers-1):
            for j in range(0, layer):
                for k in range(0, nn_shape[i+1]):
                    color = "red"
                    if(weights_normalized[connection_count]>0):
                        color = "blue"
                    connection_ids.append(
                        canvas.create_line(combined_axis[count][2],
                                        combined_axis[count][3]-int(neuron_size/2), 
                                        combined_axis[count+layer-j+k][2]-neuron_size, 
                                        combined_axis[count+layer-j+k][3]-int(neuron_size/2),
                                        width=(abs(weights_normalized[connection_count])*2)+1,
                                        fill=color)
                    )
                    connection_count+=1
                count+=1
    return connection_ids
def removeSignal(values):
    unsigned = []
    for value in values:
        unsigned.append(abs(value))
    return unsigned
def normalize(values):
    max_val = max(removeSignal(values))

    normalized = []
    for value in values:
        normalized.append(round(value/max_val, 2))
    return normalized
def draw_nn(width, height, nn_shape, weights, weights_flatten, biases, canvas, padding = [10, 10, 10, 10], neuron_size = 30):
    # padding [top right bottom left]
    neurons_axis = calcNeuronsAxis(width, height, nn_shape, padding)
    combined_axis = combineAxis(neurons_axis=neurons_axis, nn_shape=nn_shape, neuron_size=neuron_size)
    neuron_ids  =drawNeurons(combined_axis, canvas)
    connection_ids = drawConnections(canvas, combined_axis, nn_shape, neuron_size, weights_flatten)
    return {
        'neurons': neuron_ids,
        'connections': connection_ids
    }
