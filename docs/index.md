
# PATKIT Documentation

Until the 1.0 release none of the documentation is final nor necessarily
correct. Corrections and but reports are always welcome.

## Installation and basic use

- [Installing](Installing.markdown)
- [Running](Running.markdown)

## GUI user guide

[Being slowly written, please contribute if you want to hasten this up.]

Currently we only have:
- [Automated exercises](Automated_exercises.markdown)
- [Keyboard shortcuts](Keyboard_shortcuts.markdown)

## Commandline user guide

[To be written] but already available in a rudimentary form by running
`patkit --help` which also works on the subcommands (`open`, ).

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
