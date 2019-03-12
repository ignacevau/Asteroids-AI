import random
from utility import sigmoid, sum_matrix_float, clamp, Vector2
import numpy as np
import data as d

class NeuralNetWork:
    def __init__(self, input, h_layers, output):
        self.input_len = input
        self.output_len = output
        self.h_layers = h_layers
        self.weights = []
        self.biases = []
        self.setup_weights()
        self.setup_biases()

    def setup_weights(self):
        """ Set every weight to random value between -1 and 1 """
        # Add for every layer their length
        layers_len = [self.input_len]
        for i in range(len(self.h_layers)):
            layers_len.append(self.h_layers[i])
        layers_len.append(self.output_len)

        for i in range(len(layers_len)-1):
            # Add layers
            self.weights.append([])
            for _ in range(layers_len[i]):
                # Add inputs with weights
                self.weights[i].append([random.uniform(-1, 1) for _ in range(layers_len[i+1])])

    def setup_biases(self):
        """ Set every bias to random value between -1 and 1 """
        # There is a bias for every hidden layer and for the input layer
        self.biases = []
        for _ in range(len(self.h_layers) + 1):
            rd = random.uniform(-1, 1)

            # Floats as inputs --> bias must be number as well
            if d.sensor_mode:
                self.biases.append(rd)
            # Vectors as inputs --> bias must be vector as well
            else:
                self.biases.append(Vector2(rd, rd))

    def forward_prop(self, inputs):
        """ Calculate output from given inputs through the neural network """
        layers = [inputs]
        for i in range(len(self.h_layers)+1):
            # Calculate the input * weights + bias
            z = np.dot(layers[i], self.weights[i]) + self.biases[i]

            # Apply activation function
            out = []
            if d.sensor_mode:
                # Outputs are numbers
                for j in range(len(z)):
                    o = sigmoid(clamp(-20, 20, z[j]))
                    out.append(o)
            else:
                # Output are vectors
                for j in range(len(z)):
                    sigm_x = sigmoid(clamp(-20, 20, z[j].x))
                    sigm_y = sigmoid(clamp(-20, 20, z[j].y))
                    out.append(Vector2(sigm_x, sigm_y))

            layers.append(out)

        # Return the output
        final_output = layers[len(layers)-1][0]     # Last layer only has 1 output neuron
        return final_output
        