# python-badlands
Python scripts for manipulating and plotting badlands data

## Scritps to use for sampling raster data
SampleDEMmanual.py - given a model AOI and spacing, create a node registered array and sample the elevation values from a DEM. Requires UTM projection.

SampleErodabilityManual.py - given the same spacing above, sample a geologic map (saved as a raster) and output a numpy array of rocktypes that can be further pre-processed to erodability values.

SamplePrecipManual.py - sample a precipitation raster with the same array above to create an a numpy array of precipitation values in m/a.

## Scripts to use for pre-processing sampled data
SortDisplacement.py - sort the displacement grid from Coulomb 3.4 (MATLAB), into the correct ordered format for badlands input.

RemapErodabilityValues.py - remap the rock type numbers from SampleErodabilityManual.py to values of erodability and output to badlands format.

GridEdit.py - edit grid values with a GUI, currently set to modify erroneous elevation values but could be adapted to modify any other input grid.

## Scripts to use for post-processing badlands outputs
plothdf5.py - script to plot maps of badlands outputs (e.g. ero/dep, flow (m3/s), chi, topography). Also serves as a base for extracting data from hdf5 files.

CatchEro.py - extract a catchment given a model coordinate within it, plot the erosion/deposition of the catchment, calculate the volume of sediment removed for a given timestep and thus the catchment average erosion rate.
