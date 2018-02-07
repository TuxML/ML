# ML

## Synopsis

Part of the [TuxML](https://github.com/TuxML) Project to predict kernel properties from a wide range of already tested kernels.

`ML` is the last leg of the journey, taking data from the database filled by the [ProjetIrma](https://github.com/TuxML/ProjetIrma) application. All the Machine Learning is done here, to predict whether a kernel boots, what kernel is the smallest, quickest to boot, etc...

## Prerequisites

Get a `allyes.config` from your kernel version and put it in the root folder

You need a whole lot of libs :

    pip3 install scikit-learn numpy scipy

## Usage

run `csvGeneratorBdd.py` to generate a csv for the ML to use