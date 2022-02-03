# Scope

This directory contains CSV files with:

- The estimated integration times

- The accessibility of the targets during the observing period

Most of the output variables are related to the ones set in 
  `json/cgi_etc_setup`, [json/README](../../json/README.md). 
    If you use Excel, make the columns wider to see the 
    variables names clearly.

# Exposure Time

As mentioned in [json/README](../../json/README.md), 
    the name of the output filename is set in 
    `json/cgi_etc_setup.hjson`. 
    The file has some
    additional information depending on the type of target.

An empty cell in the output csv file means that the target cannot
    be observed with the Roman Coronagraph Instrument. DISCLAIMER: 
    the tool does not provide
    an explanation of what is the reason. It may be 
    the flux ratio, orbital
    epehemeris, the angular separation of the target, 
    or the requested
    Signal-to-Noise ratio. 
    It is possible to figure it out by running the 
    same target with slightly different parameters, 
    and comparing the outputs. One can also
    print out the internal variables in the 
    `scripts` directory, and/or in
  [EXOSIMS](https://github.com/dsavransky/EXOSIMS)

In the following, we describe the meaning of the output variables for
each of the observing types of the Roman Coronagraph Instrument:
self luminous exoplanets, reflected light exoplanets, and exodust.

## Self Luminous Exoplanets

- `Planet Name`: the common name of the planet as set in 
    `json/cgi_etc_setup.hjson`

- `WA (mas)`: the angular separation between the exoplanet and its host star
    in units of milli-arcsec

- `d (AU)`: the physical distance between the exoplanet and its host star
    in units of AU

- `I (deg)`: the visual inclination of the system in units of degrees

- `FR_(Instrumental Mode)`: the exoplanet to host star flux
    ratio for the instrumental mode under consideration.
    `Instrumental Mode` will have one of these values:
    `NF` for Narrow Field of View Imager,
    `Spec` for single Slit, Prism-based Spectroscopy, or
    `WF` for Wide Field of View Imager

- `(Performance Scenario)_(Instrumental Mode) (kpp=value)`:
  This line is used to separate the output
  according to the `Performance Scenario`.
  The `Performance Scenario` can be
  either `OPTI` for optimistic, or `CONS` for conservative
  -see [`json/README`](../../json/README.md) for details.
  `Instrumental Mode` is defined in `FR_(Instrumental Mode)`.
  `kpp` is the so-called `factor above classical` and 
  represents a post-procesing gain based on
  some PSF techniques and analysis, [`json/README`](../../json/README.md)

- Integration times. `T_(Performance Scenario)_(Instrumental Mode)_SNR(Value)`: the time
    in __hours__ to achieve a SNR equal to `value` 
    for a given `Instrumental Mode` 
    (see `FR_(Instrumental Mode)`) and 
    `Performance Scenario`
    (See `(Performance Scenario)_(Instrumental Mode) (kpp=value)`)

## Reflected Light Exoplanets

-`Planet Name`: the common name of the planet as set in 
    `json/cgi_etc_setup.hjson`

- `FR_(instrumental mode) (kpp=value)`: the exoplanet to host star flux
    ratio for the instrumental mode under consideration.
    `Instrumental Mode` will have one of these values:
    `NF` for Narrow Field of View Imager,
    `Spec` for single Slit, Prism-based Spectroscopy, or
    `WF` for Wide Field of View Imager.
    `kpp` is the so-called `factor above classical` and
    represents a post-procesing gain based on
  some PSF techniques and analysis, [`json/README`](../../json/README.md)

- `DoM_(Performance Scenario)_(Instrumental Mode)`: 
    the number of days after the first
    epoch,  set in `json/cgi_etc_setup.hjson`,
    with the shortest integration time to achive the SNR goal. The date is
    always within an accessible period, i.e, when the observatory can point
    to the target.
    `Instrumental Mode` is defined in `FR_(instrumental mode) (kpp=value)`.
    The `Performance Scenario` can be
    either `OPTI` for optimistic, or `CONS` for conservative.
    See `json/README.md' for details

- `WA_(Performance Scenario)_(Instrumental Mode)`: 
    the angular separation between the exoplanet and its host star
    in units of milli-arcsec
    for the epoch with the shortest integration time to achive the SNR goal.
    `Performance Scenario` is defined in 
    `DoM_(Performance Scenario)_(Instrumental Mode)` 
    and `Instrumental mode` in `FR_(instrumental mode) (kpp=value)`

- `FR_(Performance Scenario)_(Instrumental Mode)`:
    The exoplanet to host star flux ratio
    for the epoch with the shortest integration time to achive the SNR goal.
    `Performance Scenario` is defined in
    `DoM_(Performance Scenario)_(Instrumental Mode)`
    and `Instrumental mode` in `FR_(instrumental mode) (kpp=value)`

- `SNRMax_(Performance Scenario)_(Instrumental Mode)`:
    the maximum SNR that can be achieved for each target. It is constrained by
    either the target's photon rate, the detector noise properties or the time
    the target is accessible to the observatory.

- `T_(Performance Scenario)_(Instrumental Mode)_SNRMax`: the time in __hours__
    to achieve the maximum SNR. It is always less than or equal to the time
    that the target is accessible to the observatory.

- Integration times. `T_(Performance Scenario)_(Instrumental Mode)_SNR(Value)`: the time
    in __hours__ to achieve a SNR equal to `value`
    for the `Performance Scenario` and `Instrumental mode` 
    under consideration.
    See the `DoM_(Performance Scenario)_(Instrumental Mode)`
    option for the meaning of `Performance Scenario` and `Instrumental mode`

## Exo Dust

- `Disk name`: the common name of the disk as set in `json/cgi_etc_setup.hjson`

- `WA (mas)`: the angular separation between the (diffuse)
    region of interest and the host star
    in units of milli-arcsec

- `FR_(Instrumental Mode)`: the flux ratio between the (diffuse) region of
    interest and the host star for the instrumental mode under consideration.
    `Instrumental Mode` will have one of these values:
    `NF` for Narrow Field of View Imager,
    `Spec` for single Slit, Prism-based Spectroscopy, or
    `WF` for Wide Field of View Imager.

- `(Performance Scenario)_(Instrumental Mode) (kpp=value)`:
    This line is used to separate the output
    according to the `Performance Scenario`.
    The `Performance Scenario` can be
    either `OPTI` for optimistic, or `CONS` for conservative
    -see [`json/README`](../../json/README.md) for details.
    `Instrumental Mode` is defined in `FR_(Instrumental Mode)`.
    `kpp` is the so-called `factor above classical` and
    represents a post-procesing gain based on
    some PSF techniques and analysis, [`json/README`](../../json/README.md).

- Integration times. `T_(Performance Scenario)_(Instrumental Mode)_SNR(Value)`: the time
    in __hours__ to achieve a SNR equal to `value`
    for a given `Instrumental Mode`
    (see `FR_(Instrumental Mode)`) and
    `Performance Scenario`
    (See `(Performance Scenario)_(Instrumental Mode) (kpp=value)`)

# Accessibility

The CSV files starting with `accessibility` contain in each column:

- `Host star name (average, %)`: the accessibility of the host star after 
    taking into consideration keep out dates during the Roman coronagraph 
    observations due to the coordinates of the host star and 
    observatory's constraints.
    The value represents the percentage that the target is accessible during
    the two epochs set in `json/cgi_etc_setup.hjson`

- `Host star name (days after Initial Epoch)`: 
    the daily accessibility of the host star after
    taking into consideration keep out dates during the Roman coronagraph
    observations due to observational and observatory's constraints. 

Notice that the accessibility refers to the host star only, and 
    it does not imply that the exoplanet is within the field of
    view of the `Instrument Mode`, or if it is _detected_ with
    some SNR.
    The target detectability is given by the integration times.

Alternatively, one can derive the accessibility of the Roman CGI targets
with [CGI Target Accessibility](https://github.com/nasavbailey/CGI_target_accessibility).
Follow the examples in its Jupyter Notebook.
