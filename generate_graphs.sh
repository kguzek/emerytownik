#!/bin/sh

pushd machine_learning/data
python plot_synthetic_data.py --no-show
popd
mv machine_learning/data/*.html frontend/public/
