import tensorflow as tf
import numpy as np
import pandas as pd

# We need to load all the data to train the type
fileName = './data-generator/samples.csv'
my_columns = ['rhoL', 'uL', 'TL', 'rhoR', 'uR', 'TR', 's1', 's2', 's3', 'type']
data = pd.read_csv(fileName, names=my_columns)

# Drop things we don't want - we have 6 real feature inputs (rho, ux, temp)
features = data.drop(['s1', 's2', 's3', 'type'], axis=1).values
# We are classifying based on the type
# These contain values of 2, 3, 4 or 5 (4 different types of shock wave solutions)
# Remap to 0, 1, 2, 3 so the 4-neuron softmax output can use sparse labels
labels = data['type'].values - 2

# Collect some analytics and split the data into training and verification
num_samples = features.shape[0]
indices = np.arange(num_samples)
# Use time to set the seed
np.random.seed(int(tf.timestamp()) % 2**32)
# np.random.seed(42)
np.random.shuffle(indices)
train_split = int(0.9 * num_samples)
train_idx, test_idx = indices[:train_split], indices[train_split:]

x_train, y_train = features[train_idx], labels[train_idx]
x_test, y_test = features[test_idx], labels[test_idx]

# Classifier: 6 inputs -> 32 hidden neurons -> 4 class scores
# A lower Adam step size than the 0.001 default gives the wider hidden
# layer more time to settle on the type boundaries.
learning_rate = 5e-4

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(6,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax'),
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)

model.summary()

history = model.fit(
    x_train,
    y_train,
    epochs=80,
    batch_size=32,
    validation_data=(x_test, y_test),
)

loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f'Test loss: {loss:.4f}')
print(f'Test accuracy: {accuracy:.4f}')

