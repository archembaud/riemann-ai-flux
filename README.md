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