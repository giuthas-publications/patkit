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

[//]: # (And ofcourse if a version needs to be YANKED:)
[//]: # (## [version number] [data] [YANKED])


## [Unreleased]

### Added

- SATKIT will soon be available on pypi, probably under the long name:
  speech_articulation_toolkit.
- See [Roadmap](Roadmap.markdown) for an overview of what to expect in 1.0.

## [0.12.0] needs to be cleaned of merge overlaps below

### Highlights

- Configuration system now works less globally and more on a study-by-study
  basis. Local configuration overrides global.
- Exclusion is defined mainly separately for each operation/metric. This makes
  it easier to -- among other things -- run several versions of a Session level
  statistics.

## Added

- Introduced the concept of Scenarios: These are analysis results (i.e. derived 
  data) that each have their own configuration. This makes it possible to run 
  a given metric on the same data with conflicting parameters and save all 
  results for later use.
- Statistics are now saved along with Modalities and the rest on 'Save all'.
- Some helpful progress indicators to show how the data run is going.

## Changed

- Per-study or Scenario configuration instead of global configuration.
- Scenario based results saving too. 
- Major update to data management and the configuration system. 
  - Data is now separated to recorded and derived. Former is data originating 
    from outside sources and treated as immutable, latter is data originating 
    from SATKIT.
  - Data run parameters now live with the derived data.
  - TextGrids can live in both recorded data and derived data, with
    the derived version overriding recorded. This will have a future application  
    in generating practice scenarios.


### Removed

- Removed the `publish_distance_matrix` and `publish_aggregate_images`
  functions. The preferred way is to use the export functions which also
  automatically export the meta data to keep track of where an exported/published
  image came from.

### Fixed

- Saving and loading works again.
- [possibly] the issues in 0.11

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

- satkit.py will eventually be removed when running SATKIT will be moved to
  access points. This means SATKIT -- when correctly installed -- will run with
  from the command line with: `satkit [command] [arguments]`.

### Fixed

- AAA ultrasound importer now reads dates both in `%d/%m/%Y %H:%M:%S` and
  `%Y-%m-%d %I:%M:%S %p`.
- Parsing yaml exclusion lists should now work also when some of the headings
  are empty.
- Added the seaborn package to conda environment satkit-devel to make it work
  properly.

### Known issues

- Saving and loading are currently not functional. While saving seems to work,
  since new data structures like FileInformation etc. are not saved at all, the
  saved files will be unloadable.

## Version 0.9.0

- Simulated data and sensitivity analysis for metrics
  - Two contours for running sensitivity simulations for contour metrics.
  - Perturbation generation for the contours.
  - Functions for running metrics on the simulated data.
  - Lots of plotting routines to look at the results.
  
### Known issues:

- Same as in 0.8.0 plus
- Some perturbation related plotting functions have hard-coded subplot
  divisions because Comparison is not yet sortable.

## Version 0.8.0

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

## Version 0.7.0

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
