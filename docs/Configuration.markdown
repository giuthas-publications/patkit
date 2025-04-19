# Configuration files

NOTE: Parts of the description haven't yet been implemented for version 0.15.

TODO 0.16: See that the below description actually corresponds to reality.

There are some configuration files that appear under both global and local
below. Local overrides global in all cases. These could also be called user
specific (global) and data specific (local) configuration. The global options
are set by files in the user's `~/.patkit` (on Linux/macOS) or
`%userprofile%\.patkit` (on Windows) folder. The local options live with the
data as is explained below in [Local Configuration](#local-configuration).

There are examples of configuration files in the GitHub repository in the
`example_configs` folder.

## Command history

By default, the command history of the interactive commandline is stored with
the global (user specific) configuration in the `.patkit` folder inside the
`history` file. It is plain text and of the same format as the `.python_history`
file. In fact, with a bit of tweaking a user could use `.python_history` instead
because the PATKIT interactive interpreter is actually just a Python interpreter
with PATKIT data preloaded. However, this is only recommended if you know what
you are doing.

## Global configuration

### General parameters

These are set globally so that they may be omitted locally. They can be
overridden locally though and should be when, for example, different parts of
the data have been recorded in areas with different mains frequencies. 

```yaml
# What precision is treated as equal when comparing annotation boundaries.
epsilon: 0.00001

# Used in filtering sound signals before beep detection.
mains_frequency: 50
```

### GUI parameters

Most of these parameters deal with data display.

#### General parameters for axes in the main plot

Height ratio of data display area vs textgrid tier display area. This does not
control directly the height of individual data displays nor individual tier
displays, but instead controls the ratio between the sum of data displays vs sum
of tier displays.

```yaml
data_and_tier_height_ratios: 
  data: 2
  tier: 1
```

```yaml
# Which data axes to display. Currently used only to decide the number to
# create. Number of lines gives the number of axis, modalities on the same line
# will be drawn on the same axes.
general_axes_params:
  data_axes:
    sharex: True
  tier_axes:
    sharex: True
```

#### Axes definitions for the main plot

```yaml
data_axes:
  PD l1:
    modalities:
      - PD l1 on RawUltrasound
#    modality_names:
#      - l1
    sharex: True
    auto_ylim: True
  PD l2:
    modalities:
      - PD l2 on RawUltrasound
#    modality_names:
#      - l2
    sharex: True
    ylim:
      - 100
      - 2000
  PD normalised:
    modalities:
      - PD l1 on RawUltrasound
      - PD l2 on RawUltrasound
    modality_names:
      - l1
      - l2
    sharex: True
    normalisation: both # none, peak, bottom, both
  spectrogram2:
    sharex: True
  wav:
    sharex: True
  # density:
  #   sharex: False
```

#### TextGrid display parameters

```yaml
# Tiers drawn on the data axes. Ignored if not found.  
pervasive_tiers:
  - Segment
  - Segments
  - segment
  - segments
  - phoneme
```

#### X (time) axis parameters

```yaml
# Initial limits for x-axis
#xlim:
#  - -.25
#  - 1.5
auto_xlim: True
```

#### General display style parameters

```yaml
# Font parameters
default_font_size: 10
```

Dark vs light mode. Accepted values are `dark`, `follow_system`, and `light`.
```yaml
color_scheme: dark
```


## Local configuration

All of the global parameters can be set locally by using the same file names
within the data directories. In addition, [Data processing
parameters](#data-processing-parameters) are only set locally with the data.
They may -- however -- be overridden for parts of the data.

### GUI parameters

It is especially useful to override global GUI parameters at the data to
guarantee a given set of display settings is used for segmentation or other
analysis.

### Data processing parameters


### Simulation parameters

Simulations are run on mock up tongue splines/contours extracted manually from
Peter Ladefoged's Vowels and Consonants. A commented version of the
configuration walked through below can be found on PATKIT's GitHub repository in
the `example_configs` folder.

The first parameters define where to save the resulting plots and what message
prefix should be used in logging messages.

```yaml
output_directory: "ultrafest2024/"
logging_notice_base: "Ultrafest 2024 simulation: "
```

Sound/contour selection is defined with IPA characters:

```yaml
sounds: 
  - 'æ'
  - 'i'
```

This parameter defines the used point-wise perturbations in millimeters.

```yaml 
perturbations: 
  - -2 
  - -1 
  - -.5 
  - .5 
  - 1 
  - 2
```

This parameter group defines the spline distance metric simulation.

```yaml
contour_distance:
  metric: "annd"
  timestep: 1
  sound_pair_params:
    sounds:
      - 'æ'
      - 'i'
    perturbed:
      - 'second'
      - 'first'
    combinations: full_cartesian # only_cross, only_self
```

This (rather simple) parameter group defines the spline shape metric simulation.

```yaml
spline_shape_params:
  metric: 'mci'
```

And finally the result figures are defined with the following parameter groups.
To omit a figure from the final plotting just comment out or delete the group
from the configuration file.

```yaml
# This produces a plot with change in the distance metric plotted
# as a ray on the perturbed point of the contour.
distance_metric_ray_plot:
  figure_size:
    - 10.1
    - 4.72
  scale: 200
  color_threshold:
    - .1
    - -.1

# Same as distance_metric_ray_plot but for shape metrics.
shape_metric_ray_plot:
  figure_size:
    - 7
    - 3.35
  scale: 20
  color_threshold:
    - 2
    - .5

# Two panel plot that demonstrates how the perturbations are applied.
# See the Ultrafest 2024 extended abstract for an example.
demonstration_contour_plot:
  filename: "demonstration_contour_plot.pdf"
  figure_size:
    - 6.4
    - 4.8
  sounds:
    - 'æ'
    - 'i'
```



