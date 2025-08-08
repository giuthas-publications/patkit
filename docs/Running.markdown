# Running PATKIT

First [install](Installing.markdown) PATKIT to run from the commandline.

- Patkit runs from the commandline with `patkit`. 
- Try `patkit --help` for instructions.
- This will analyse a minimal three recording example and open the GUI `patkit
  recorded_data/minimal`

## If running fails on Linux

- If on Linux of the debian variety (ubuntu, popos, others), you may also need 
to run the following:
```shell
apt-get update
apt-get upgrade
sudo apt-get install -y libxcb-cursor-dev
```
Try this in case trying to run patkit complains about a missing `xcb` plugin.

## Running the examples

TODO 0.19: update this

Get the [test data](Test_data.markdown).

There are three small datasets included in the distribution. You can
run tests on them with the test script `pd_test.py`. Currently, the
following work and produce a new spaghetti_plot.pdf and a transcript
in `[method_name].log`.

``` shell
patkit recorded_data/tongue_data_1_1
```

The first example directory contains recordings with all files present
while the second is intentionally missing some files. The latter case
should therefore produce warnings in the resulting log. Running
without the exclusion list specified should produce a plot with a
couple more curves in it.

The routines to deal with a directory structure like that of `test2`
are yet to be implemented.

## Running the tests

Proper testing is yet to be implemented.
