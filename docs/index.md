
# PATKIT Documentation

Until the 1.0 release none of the documentation is final nor necessarily
correct.

## Installation and use

- [Installation and use for analysis](Installing_and_using.markdown).
- Set PATKIT up for development
  - [Old instructions for conda/mamba](SetupForDevelopment.markdown)
  - Current instructions: 
    - Fork PATKIT on github.
    - Clone your forked PATKIT repository to your local machine.
    - Get `uv` if you don't already have it.
    - Do your test runs with `uv run patkit [arguments]` or install your local
      repo with `uv tool install .` in the PATKIT repository.
    - The `uv tool install` has been at least in the recent past been more
      reliable if used with `uv tool uninstall patkit` when an update is ready
      to be tried.

## GUI user guide

[Being slowly written, please contribute if you want to hasten this up.]

Currently we only have:
- [Keyboard shortcuts](Keyboard_shortcuts.markdown)

## Commandline user guide

[To be written] but already available in a rudimentary form by running
`patkit --help`

## PATKIT Runtime data structures

PATKIT's class structure aims for efficiency without sacrificing clarity.
Clarity of code brings easy maintainability and that is more important in the
long run than gains in execution speed.

- Introduction to PATKIT Data Structures
  - [Core Data Structures](CoreDataStructures.markdown)
  - [Modalities for Recorded Data](ModalitiesforRecordedData.markdown)
  - [Modalities for Derived Data](ModalitiesforDerivedData.markdown)
  - [Modalities in Practice](ModalitiesinPractice.markdown) including notes on
    specific Modalities
    - [Splines in PATKIT](Splines.markdown)
  - [Database Classes](DatabaseClasses.markdown)
- Extending PATKIT
  - Before starting, please read Coding conventions in [PATKIT development
    guide](Development_guide).
  - Implementing a New Datasource
  - [Writing a New Modality](WritingNewModality.markdown)

## PATKIT API

[API Documentation](api/index.html)

## PATKIT Files

- Data files
  - [Guidelines for Data Directory Structure](DirectoryStructure.markdown)
  - Importing and Exporting
  - [Saving and Loading](Saving_and_loading.markdown)
- [Configuration files](Configuration.markdown)
  - Command history
  - Global configuration
    - General parameters
    - GUI parameters
    - Data processing parameters
  - Local configuration
