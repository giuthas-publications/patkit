# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[//]: # (Possible headings in a release:)
[//]: # (Highlights for shiny new features.)
[//]: # (Added for new features.)
[//]: # (Changed for changes in existing functionality.)
[//]: # (Refactor when functionality does not change but moves.)
[//]: # (Documentation for updates to docs.)
[//]: # (Testing for updates to tests.)
[//]: # (Deprecated for soon-to-be removed features.)
[//]: # (Removed for now removed features.)
[//]: # (Bugs for any known issues, especially in use before 1.0.)
[//]: # (Fixed for any bug fixes.)
[//]: # (Security in case of vulnerabilities.)
[//]: # (New contributors for first contributions.)

[//]: # (And of course if a version needs to be YANKED:)
[//]: # (## [version number] [data] [YANKED])


## [Unreleased]

### Added

- 0.17 is planned to update the GUI with more complete TextGrid modification.
- 0.18 is planned to be a release of automated segmentation exercises.
- 0.19 is planned to be a data structure update giving support for multiple data
  sources per trial.
- 0.20 will update configuration handling.
- 0.21 will add further GUI features
- 0.22 is planned to be an implementation of kymography. This might get moved 
  to a release after 0.23.
- After 0.23 there are planned updates to CLI, GUI, ultrasound frame
  interpolation, processing speed by implementing multiprocessing, new
  algorithms (optic flow, LPC for tongues, kymography, ...), new data sources,
  code testing, documentation and finally a 1.0 release.


## [0.17.0] - 2025-05-28

### Highlights

- Improved zooming and panning:'
  - Panning works
  - Zooming has better short cut conformity
- Audio playback
- New list view of recordings.

### Added

- Audio playback
- Clickable list view of recordings
- Documentation for keyboard shortcuts

### Changed

- Panning with keyboard shortcuts has been added.
- Zooming shortcuts work more consistently.
- Zooming centers on cursor if a cursor has been placed.

### Fixed

- There is a minimal three recording example again.

### Bugs

- To start zooming you need to click on the main figure - also outside the
  graph areas will do.
- Zooming very far in makes the plotting behave strangely.


## [0.16.0] - 2025-05-26

### Highlights

- New configuration and data management model separates recorded and PATKIT
  data into different directories.

### Changed

- Configuration now happens with files that are always named the same. Opening
  a directory that contains the correct config files is equivalent to opening
  the files.
- Derived/saved data is stored in the same directory as the configuration files
  or in subdirectories.
- PATKIT files apart from `patkit_manifest.yaml` are no longer stored with
  recorded/external data.

### Removed

- The main config file has been removed.

### Bugs

- Exclusion lists are disabled until reimplementation in most likely version
  0.20.


## [0.15.2] - 2025-04-22

### Highlights

- Fixed changelog parsing.

### Fixed

- Only change is that changelog headers now all conform to Keep a Changelog and
  should parse correctly in automated release not generation.


## [0.15.1] - 2025-04-22

### Highlights

- A menu option for selecting if the mean image, the frame at selection cursor
  - raw or interpolated - gets displayed in the image panel.

### Added

- A menu option for selecting if the mean image, the frame at selection cursor
  - raw or interpolated - gets displayed in the image panel.

### Fixed

- Attempting to fix the GitHub automated release, which failed previously due to
  a parsing error.


## [0.15.0] 2025-04-21

### Highlights

- Re-implementation of the simulation code that was originally released for
  Ultrafest 2024.

### Added

- `patkit simulate` command for simulating different metrics on spline data. It
  uses the simulation_parameters.yaml file.

### Changed

- Release notes are going to be automatically populated from the Changelog for
  better readability.
- Planned release schedule has changed.

### Fixed

- GitHub actions should now run a bit smoother and not attempt to run in forks.
- Hopefully fixed an older error complaining that `\i` is not a valid escape
  sequence in `\infty`.


## [0.14.2] 2025-04-11

### Highlights

- PATKIT is available on pypi under the name patkit.
- Fixed the build and distribution / installation issue: PATKIT should now run
  on linux, mac, and windows.
- Alpha/beta/rc releases will be made on test-pypi for those interested in
  running bleeding edge versions.
  - Also, pre-releases now work on GitHub.

### Added

- Conditional import of readline or pyreadline3 so that the interpreter mode
  should work also on windows.

### Fixed 

- Installation problems resulting in an empty package that would not run.


## [0.14.1] 2025-02-18

### Added 

- Automated releases on testpypi, pypi and github. Testpypi will in the future
  be used for pre-releases (alpha, beta, release candidate/rc) and pypi for
  regular releases. 
- Technically the software is still in alpha status as a whole but will get
  occasional alpha/beta/rc releases of the 0.x releases.


## [0.14.0] 2025-01-31

### Highlights

- New name! This program and library are now called PATKIT for Phonetic Analysis
  ToolKIT.
- PyPi package will be available very shortly after release of 0.14.
- There's a new and shiny command line interface. With the new installation
  procedure, PATKIT can be run as any regular command line tool.
- There's a new installation procedure with uv. Fast, neat, gives us the
  previous easily.

### Added

- Dark/Light mode support. See bugs below, though.

### Changed and Refactored

- Moved the project directory to src layout. Updated pyproject.toml to reflect
  this. 
- Moved to installation with uv and updated pyproject.toml to work with
  this too. 
- Command line is now implemented with `click` rather than `argparse`.
  Neater look, easier maintenance and with the new installation also working
  command line tool with subcommands.
- PATKIT now uses PyQt6 instead of 5 for the GUI.

### Docs

- Docs are now again correctly generated.
- Some preliminary docs on configuration. Expect these to update in the next
  two-three releases.

### Deprecated

- One of the next updates - probably 0.16 - will move from centralised
  single config system to per-dataset config system.
- Another soon to happen change is the expansion of the classes derived from 
  DataAggregator. Recording will be split to Source and Trial, and DataSet added
  as a class that contains Sessions.
- There maybe references to the old name (SATKIT) in documentation and source
  code. These will be updated as they are found. Please let us know if you spot
  one.

### Bugs

- Switching the operating system between dark/light mode while the annotator is
  running may or may not update the plots, and may even break them. However,
  restarting the annotator will update the plots.
- Implementing the subcommand `patkit simulate` is still underway. Expected to
  be available in 0.15.
- Errors like these can show up at startup, but can be safely ignored:
```shell
/home/jpalo/.local/share/uv/tools/patkit/lib/python3.13/site-packages/patkit/annotations/peaks.py:293: SyntaxWarning: invalid escape sequence '\i'
  categories = ["l$\infty$" if metric ==
/home/jpalo/.local/share/uv/tools/patkit/lib/python3.13/site-packages/patkit/plot_and_publish/publish.py:188: SyntaxWarning: invalid escape sequence '\i'
  plot_categories = ["l$\infty$" if metric ==
```

## [0.13.0] 2025-01-07

### Highlights

- Production version of downsampling functionality based on paper published at
  ISSP 2024.

### Added

- Downsampling of derived modalities.
- Modality legend names and formatting from config.

### Bugs

- Docs are not necessarily fully generated due to some naming issues. This
  should be fixed in 0.14.
- SatPoint in SatGrid references the old config_dict global variable. This will
  make any calls to `SatPoint.contains` crash. This will be fixed in 0.14.
- Not specifying ylim in GUI configuration crashes. This has already been fixed
  in the branch that will become 0.14.

## [0.12.0] 2024-12-29

### Highlights

- Experimental interactive workflow. 
  - Supported by interface and data initialisation being collected into some
    simple-to-use functions.
  - Also supported by temporary script file `patkit_interactive.py`.
    - Runs like `patkit.py` but instead of starting the GUI annotator, starts an 
      interactive Python session.
- Exporting data from Modalities into DataFrames for external analysis.

### Added

- Exporting data from modalities into DataFrames for external analysis.
  - Includes an option of exporting with label info from TextGrids.
  - Experimentally enabled export of several derived modalities into the same csv
    file.
- A script to run PATKIT as an interactive interpreter. 
  - The same commands can obviously be copy-pasted into an interpreter to get some
    data loaded and processable in interactive mode.
- Some helpful progress indicators to show how the data loading is going.
- Y limits of modality axes and spectrograms can be controlled from the gui
  parameter file.

### Changed

- A lot of functionality that lived in `patkit.py` is now in regular patkit
  library functions and in the new `patkit/patkit.py` module.
- Undefined fields are no longer allowed in config files.

### Removed

- Dismantled the `scripting_interface` submodule.

### Fixed

- Saving and loading works again.

### Bugs

- Same as previous versions.
- Command history does not yet work when running PATKIT as an interactive
  interpreter with `patkit_interactive.py`.
- Undefined fields in config files should have a clearer error message. And so
  should errors in config files in general.


## [0.11.0] 2024-11-20

### Added

- Simulating ultrasound probe rotation (misalignment) by selecting different
  sub-sectors from recorded raw data.
- DistanceMatrices can now be sorted by a list of substrings into or simply by 
  prompt.
  - DistanceMatrices can also specify their own exclusion list in the config.
- Saving the selected frame with metadata so that example frames can be 
  reproduced.
- Saving AggregateImages, DistanceMatrices and the main figure (of the GUI) 
  with metadata.
- Expanded SatGrid (the editable TextGrid extension) to include Points and Point
  Tiers.
- Automatic x limits now work properly in the GUI.

### Bugs

- Displaying exclusion is not quite working with the new feature of exclusion
  working both globally and per metric. This leads to some warnings when trying to
  plot modalities that didn't get calculated. Will be fixed in the future as the
  configuration system gets a makeover.
- When data run config and exclusion are at odds (especially sort) there should
  be an informative message to the user. This too will get better when the
  configuration system gets a makeover.

## [0.10.1] 2024-10-18

### Added

- Added some docstring documentation.

### Fixed

- Removed some tracing that was left from debugging.

## [0.10.0] 2024-10-18

### Highlights

- Diagnosing ultrasound probe alignment is now possible by generating a
  DistanceMatrix of a Session with the metric `mean_squared_error`.

### Added

- Statistic is a new kind of derived data class. It is meant as the base class
  for data that is not time-dependent.
- There are now new abstract base classes that Session, Recording, Statistic, and
  Modality derive from. These are meant for gathering common functionality of the
  four main classes together rather than direct inheritance.
- AggregateImage is a new Statistic and its current only implementation is the
  metric 'mean', which is used to calculate mean images.
- Mean Images are used as the basis of calculating another Statistic: 

### Deprecated

- patkit.py will eventually be removed when running PATKIT will be moved to
  access points. This means PATKIT -- when correctly installed -- will run with
  from the command line with: `patkit [command] [arguments]`.

### Fixed

- AAA ultrasound importer now reads dates both in `%d/%m/%Y %H:%M:%S` and
  `%Y-%m-%d %I:%M:%S %p`.
- Parsing yaml exclusion lists should now work also when some of the headings
  are empty.
- Added the seaborn package to conda environment patkit-devel to make it work
  properly.

### Known issues

- Saving and loading are currently not functional. While saving seems to work,
  since new data structures like FileInformation etc. are not saved at all, the
  saved files will be unloadable.

## [0.9.0]

- Simulated data and sensitivity analysis for metrics
  - Two contours for running sensitivity simulations for contour metrics.
  - Perturbation generation for the contours.
  - Functions for running metrics on the simulated data.
  - Lots of plotting routines to look at the results.
  
### Known issues:

- Same as in 0.8.0 plus
- Some perturbation related plotting functions have hard-coded subplot
  divisions because Comparison is not yet sortable.

## [0.8.0]

- Splines
  - Spline loading from AAA export files.
  - Several spline metrics now work and can be displayed.
  - Splines can be displayed on the ultrasound frame.
- Some updates to clean the code in general.

### Known issues:

- Same as in 0.7.0 plus
- Synchronising spline metrics and splines with ultrasound is currently
  unreliable. This is because the timestamps in spline files have proven to
  have either drift or just inaccuracies and testing why this is so is a job
  for the future. This may eventually be solved just by matching splines with
  ultrasound frames and reporting when that becomes too unreliable.

## [0.7.0]

- Saving and loading to/from native formats for derived Modalities.
  - Saved data can be loaded on startup or opened afterwards. This means
    derived Modalities don't need to be re-generated every time and switching
    between recording sessions is fast.
  - Metadata of derived Modalities is now saved in human-readable form while
    the numeric data is saved in numpy native formats.
  - Database is also saved in human-readable formats for easy checking of data
    integrity.
  - Opening (ctrl+'o') and saving (ctrl+shift+'s') work in the GUI. Overwrites
    are verified when saving, but the logic of that part may change before 1.0.
    The most obvious alternative to approving overwrites on a file-by-file
    basis alongside the 'Yes to all' option, is to only have the latter.
- Zooming in, out and to all now works with 'i', 'o' and 'a' respectively.

### Known issues:

- ctrl+'i' and ctrl+'a' zoom but ctrl+'o' is bound to opening a recording
  session. The fix will be removing the first two bindings which are
  unintentional.
