# ML

## Synopsis

Part of the [TuxML](https://github.com/TuxML) Project to predict kernel properties from a wide range of already tested kernels.

`ML` is the last leg of the journey, taking data from the CSV generated with [csvgen](https://github.com/TuxML/csvgen). All the Machine Learning is done here, to predict whether a kernel boots, what kernel is the smallest, quickest to boot, etc...

## Prerequisites

You need a whole lot of libs :

    pip3 install scikit-learn numpy scipy

## Usage

    ./statsTuxML.py file.csv
