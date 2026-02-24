##
## Copyright (c) 2019-2026
## Pertti Palo, Scott Moisik, Matthew Faytak, and Motoki Saito.
##
## This file is part of the Phonetic Analysis ToolKIT
## (see https://github.com/giuthas/patkit/).
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.
##
## The example data packaged with this program is licensed under the
## Creative Commons Attribution-NonCommercial-ShareAlike 4.0
## International (CC BY-NC-SA 4.0) License. You should have received a
## copy of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
## International (CC BY-NC-SA 4.0) License along with the data. If not,
## see <https://creativecommons.org/licenses/by-nc-sa/4.0/> for details.
##
## When using the toolkit for scientific publications, please cite the
## articles listed in README.md. They can also be found in
## citations.bib in BibTeX format.
##

# Return instructions for how to run PATKIT
patkit
patkit --help

# Run with the default configuration and show 3 recordings in the GUI.
patkit scenarios/minimal
patkit open scenarios/minimal/

# Run 10 recordings and show in the GUI
patkit scenarios/tongue_data_1_1/

# TODO 0.20: Update the scenarios below and create a new minimal example.
# The same but in interactive interpreter mode
patkit interact scenarios/minimal/

# A bit more extensive with 10 files
#   - Missing files
patkit recorded_data/tongue_data_1_2/

#   - Missing files, exclusion list in .csv format
patkit recorded_data/tongue_data_1_2/ -e recorded_data/tongue_data_1_2/exclusion_list.csv

#   - Missing files, exclusion list in .yaml format
patkit recorded_data/tongue_data_1_2/ -e recorded_data/tongue_data_1_2/exclusion_list.yaml

# This requires example_configs from the github repository:
# github.com/giuthas/patkit/example_configs
# It will generate some simulation plots in the directory ultrafest24
# which will be created if it does not exist.
patkit simulate example_configs/ultrafest24/

# Same, explicitly specifying the  simulation configuration file.
patkit simulate example_configs/ultrafest24/patkit-simulation.yaml
