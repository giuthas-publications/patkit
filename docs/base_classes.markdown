# Base classes

It is good to know what the base classes 

Most SATKIT [core data structures](CoreDataStructures.markdown) derive from
DataObject. Those that contain data - Modalities and Statistics - inherit from
DataObject via DataContainer, and those that contain other DataObjects -
DataSets, Sessions, Trials, and Sources - inherit from DataAggregator.

The below diagram includes some non-standard UML to make it a bit more compact.
DataObject has several `recorded_` and `patkit_` properties which are not all
listed but just marked as `[recorded_paths]` and `[patkit_paths]`. See the API
documentation for what is available.  

![base data structures](base_data_structures.drawio.png)

The [PATKIT data management principles](DataManagement.markdown) are reflected
in how path data is actually stored. The `recorded_` and `patkit_` paths give
absolute locations of the files, but  the `file_info` field works recursively
with contained classes storing only their relative location to the containing
class. This means that using file_info  directly may lead to unexpected
results.