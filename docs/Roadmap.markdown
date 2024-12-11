# SATKIT 1.0 Roadmap

- [ ] GUI
  - [ ] Boundaries and labels
    - [x] selection of tier that will be displayed over the graphs
    - [x] movable single boundaries
    - [ ] shift+drag moving of all boundaries at the same time point
    - [ ] label editing
    - [ ] adding boundaries
      - [ ] including interval selection and adding from that maybe
    - [ ] deleting boundaries
    - [ ] Viewing and selecting
      - [x] frame and time point selection
      - [x] zooming with Praat's shortcuts or something close
      - [ ] zooming with interval selection
      - [ ] toggle for displaying acoustic boundaries
      - [ ] toggles or similar for displaying different data modalities
      - [ ] note function for annotating individual tokens with free text
- [ ] Algorithms
  - For audio:
    - [x] Spectrogram
  - For video-like data:
    - [x] Pixel Difference
    - [ ] Optic flow
    - [ ] Principal component analysis (PCA) / dimensionality reduction
    - [x] Mean images and mean squared error metric for assessing ultrasound probe
      movement
  - For tongue splines:
    - [x] Average Nearest Neighbour Distance and Median Point-by-point Distance
    - [x] Some or all of the metrics by [Kathtrine M.
      Dawson](https://github.com/kdawson2/tshape_analysis)
    - [x] Simulated data and sensitivity analysis framework for metrics
  - For timeseries:
    - [x] automated peak and valley selection on time series
- [ ] Saving and loading
  - [ ] Data management model which separates recorded (external data) from
    derived (SATKIT generated) data, with local config in the filesystem 
    controlling the system's behaviour
  - [x] TextGrids
    - [x] loading
    - [x] saving
  - [x] loading ultrasound data from AAA
    - [x] old style
    - [x] new style
  - [ ] loading 3D/4D ultrasound data from RASL
  - [x] load splines from .csv files exported by AAA
  - [ ] load BIOPAC EMG data
  - [ ] load EVA and possibly other flow data
  - [x] SATKIT native formats
    - [x] saving results in implementation free, human-readable if possible, formats
    - [x] loading
- [ ] Documentation
  - [ ] update README and other relevant files
  - [ ] update both references to tools SATKIT provides and tools it uses
  - [ ] generate and publish automatic docs
    - [ ] update docstrings of at least the most important classes, methods and functions
    - [ ] include also graphs of how the central classes work and are used
- [ ] Code refactoring and quality control
