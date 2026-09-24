# riemann-ai-flux
A collection of machine learning tools for machine learning approximation of riemann fluxes in CFD solvers

## Tools

All of the source codes are contained in the /src folder. Here, there are a number of different tools:

* Data Generator - a tool for generating the data used to train the ANN.

### Data Generator

In the /src/data-generator/ directory:

```bash
make
./generate.run
```

### Data Splitter

The data splitter takes the Riemann flux data contained in samples.csv and splits it by type, one for
each Riemann problem type. Then it saves the types back into the same directory as samples.csv.

To run, from the /src directory:

```bash
python split_data.py
```

**Note**: Your python executable alias may differ from mine.

### Riemann problem type classifier

Although this is a relatively simple problem to solve, the type of Riemann problem being solved (two shocks, left moving shock, right moving shock etc)
could impact on the ability of the NN to learn wave speeds. Hence, a classifier has been prepared which considers the state on each side
of the interface and predicts the type of Riemann problem being used.

To run, from the /src directory:

```bash
python train_type.py
```

Typical accuracy with the current model and codes is about 95%. Whether or not this is useful is up for debate.

### Riemann wave speed regression

For any 1D flux, we have mass, momentum and energy equations. Hence there are 3 wave speeds - classically these are the same speeds, but the training
data shows us clearly that these are not the same.

A new code has been added (train_riemann.py) which - for any Riemann problem type and for a particular conservation equation (mass, mom and eng) will train a NN
to predict the wave values in preparation for flux computation.

To run this, from the /src directory:

```bash
python train_riemann.py
```