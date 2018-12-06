import numpy as np
from pathlib import Path
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, Flatten

class PredictionModel(Sequential):
    """ Prediction model manipulation """

    # Indicates the schema of the photos.
    INPUT_SHAPE = (96, 96, 3)

    # Where to store the model weights. Using this path
    # since this class is used outside of this folder.
    MODELPATH = 'models/'
 
    def __init__(self, model_id):
        """
        Get specific model.

        Attributes
        ----------
        model_id : int
            The model id to initialize.
        """
        super().__init__()
        self.model_id = model_id
        self.initialize_model()
        if (self.model_exists()):
            self.load_weights()

    def model_exists(self):
        """
        Get if this model exists. Hence it is trained.

        Returns
        -------
        boolean
            True if module exists.
        """
        model_weights = Path(self.MODELPATH + 'model_' + str(self.model_id) + '.h5')
        if (model_weights.is_file()):
            return True
        else:
            return False
    
    def load_weights(self):
        """
        Load weights to model.
        """
        super().load_weights(self.MODELPATH + 'model_' + str(self.model_id) + '.h5')
    
    def initialize_model(self):
        """
        Initialize model.
        """
        super().add(Conv2D(96, kernel_size=3, activation='relu', input_shape=self.INPUT_SHAPE))
        super().add(Dropout(0.1))
        super().add(Conv2D(64, kernel_size=3, activation='relu'))
        super().add(Dropout(0.1))
        super().add(Flatten())
        super().add(Dense(2, activation='softmax'))
        super().compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def train(self, values, labels, n_epochs=10):
        """
        Train the model.

        Attributes
        ----------
        values : numpy.array
            Values to train for.
        labels : numpy.array
            Labels to train against.
        epochs : int
            How many epochs.
        """
        super().fit(values, labels, epochs=n_epochs, batch_size=100)
    
    def save(self):
        """
        Save model weights.
        """
        super().save_weights(self.MODELPATH + 'model_' + str(self.model_id) + '.h5')
