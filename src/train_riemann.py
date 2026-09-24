import tensorflow as tf
import numpy as np
import pandas as pd

# Choose which problem type to solve
SHOCK_TYPE = 2

# Equation type 1 = mass, 2 = momentum, 3 = energy
EQUATION_TYPE = 3

# Load the data from csv; Pandas is ok for this.
# However, the file we are reading is a tab delimited file
# and is not actually a CSV.
# Since I'm on the train, its easier for me to rewrite my
# C code to generate a CSV file instead. OK, done.
data = pd.read_csv(
    f'./data-generator/samples_type_{SHOCK_TYPE}.csv'
)

# Focus on predicting just S1 at the moment.
# So we can drop the others.
features = data.drop(['s1', 's2', 's3', 'type'], axis=1).values

labels = data[f's{EQUATION_TYPE}'].values

# Check the shape of the features
print(f"Shape of features = {features.shape}")

# Train without scaling
# We can do this because everything is already dimensionless
print(features)
print(labels)

# Split anyway
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

# If we are using batching
batch_size = 32
train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(len(x_train)).batch(batch_size)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(batch_size)

# 6 inputs -> 64 tanh units -> one linear speed.
# The previous 12-unit net stalled near the mean predictor (MAE ~1.6).
# A smaller Adam step than the 0.001 default, plus a longer run that
# can still shrink the step when validation MAE plateaus, gives the
# wider hidden layer time to fit s1/s2/s3 without overshooting.
hidden_units = 64
learning_rate = 2e-4
epochs = 3000

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(6,)),
    tf.keras.layers.Dense(hidden_units, activation='tanh'),
    tf.keras.layers.Dense(1, activation='linear'),
])
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
    loss='mae',
    metrics=['mae'],
)

model.summary()

csv_logger = tf.keras.callbacks.CSVLogger(f'training_metrics_type_{SHOCK_TYPE}_equation_{EQUATION_TYPE} .csv', append=False)
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=100,
    min_lr=1e-6,
    verbose=1,
)
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=250,
    restore_best_weights=True,
    verbose=1,
)

history = model.fit(
    train_ds,
    epochs=epochs,
    callbacks=[csv_logger, reduce_lr, early_stop],
    validation_data=test_ds,
    verbose=2,
)

# Problem type 2
expected_S = -1.479609e+00  # s3
input = tf.constant([1.680376e+00,-3.127891e-01,1.251479e+00,1.596880e+00,6.123149e-01,6.285726e-01], dtype=tf.float32)   # shape (6,)
input = tf.reshape(input, (1,6))  
S_pred = model.predict(input)
print(f"Computed S value = {S_pred}, Expected {expected_S}")

# Save the model?
model.save(f'riemann_model_type_{SHOCK_TYPE}_equation_{EQUATION_TYPE}.h5')