# Scope

This directory contains the file `hip_cgi_etc.txt`.
Simply add the HIP identifiers 
(see
[Hipparcos Catalogue](https://www.cosmos.esa.int/web/hipparcos/catalogues))
    of the stars to be considered.
    The HIP identifiers are used by 
  [EXOSIMS](https://github.com/dsavransky/EXOSIMS) 
    to find the stellar properties.
    We include some stars in the list that are of general interest for
    the three types of observations with the Coronagraph Instrument:

- Self luminous exoplanets
- Reflected Light exoplanets
- Exozodiacal Light and Debris Disks

We chose to order the stars from smaller to greater HIP id,
    but the order can be any other choice: 
  [EXOSIMS](https://github.com/dsavransky/EXOSIMS) 
    will match the HIP id in `hip_cgi_etc.txt`
    with the one in `json/cgi_etc_setup.hjson`.

## Additional Notes

The current version of the Roman
Coronagraph Exposure Time Calculator does not allow one
to define a star that is not in the __Hipparcos__ catalog.
The Hipparcos catalog is
complete for stars with V<=7.3&ndash;9.0 mag, 
depending on the galactic latitude. 
Therefore, it should have all targets of
interest for the Roman Coronagraph Instrument. 
Let us remind the reader that the coronagraph
performance starts to degrade for
stars with `V>5` 
We recommend to consider any star with `5<V<=7` as
a case beyond the nominal performance of
the Roman Coronagraph Instrument, the greater the value of V,
the more challenging. `V=7` is a reasonable cutoff to consider.

Another relevant quantity to consider when adding potential targets
for the Roman coronagrah is the apparent __stellar diameter__. 
If it is larger than about 2 milli-arcsec, 
the performance of the coronagraph degrades. 
For instance, this can happen 
with bright stars, such as Vega.

Also, there should not be an object as bright as or brighter than the target
star in a radius of 45 arcsec or less from the target star, or the 
__acquisition__ system of the Coronagraph Instrument could
be confused.

