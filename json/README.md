# Scope

This directory contains the files that set up the 
instrumental performance of the Roman Coronagraph Instrument
and the
parameters used in the Exposure Time Calculator.

Note: the directory `tmp` is used to store some temporary files.
   [README](tmp/README.md)

# EXOSIMS

The file `cgi_exosims.json` parses the instrumental
information of the Roman coronagraph to 
[EXOSIMS](https://github.com/dsavransky/EXOSIMS), which is
the software that is used to
actually derive the integration times for each target.
Notice that `cgi_exosims.json` is written in standard `json` format,
see [JSON](https://www.json.org/json-en.html).
__IMPORTANT__: `json` uses `:` instead of
   `=` for assignments. If you type `=`, you'll get a running error.

`cgi_exosims.json` 
has at the top the
variable `catalogPath`. It sets the location __and__ 
filename of the catalog of target stars that are 
used by the exposure time calculator, see [README](../catalog/README.md).

`cgi_exosims.json` also sets the level of local zodiacal light along the
    line of sight: `magZ`. More importantly, it sets the level of
    exozodiacal dust for the target system: `magEZ`. Notice
    that exozodi is assumed to be _perfectly_ subtracted from the
    data leaving only an imprint in the shot noise, see
  the [Bibliography](../README.md#bibliography) for more information.
  Thus, its influence is in the noise term only. 

Of all the other parameters in
`cgi_exosims.json`,
there is one that deserves some attention: __`ppFact`__,
and it is the reciprocal of the `factor above classical`,
    see this
[report](https://roman.ipac.caltech.edu/docs/sims/20210110_Roman_CGI_post_processing_report_URS_corrected_typo.pdf)
    for further details.
    The `factor above classical` measures the improvement in the 
    post-processing of the residual
    coronagraph speckles via different PSF techniques.
    The Roman Coronagraph Exposure Time Calculator
    makes use of the most recent values.

In almost all situations, none of the parameters 
in `cgi_exosims.json` needs to be updated by the user.
Perhaps, `catalogPath` is the only one in case the
user wants to set it to a different catalog file. 

The rest of the parameters are derived from
actual performance of the
coronagraph based both on simulations and lab measurements.
You may find some of this information in the public site
for the [Roman instrumental parameters
at IPAC](https://roman.ipac.caltech.edu/sims/Param_db.html).

# Exposure Time Calculator

The file `cgi_etc_setup.hjson` is where the 
the user can set up all the
interface parameters.
Notice that this file is written in `hjson` format, which is an extended
    version of `json` that allows one to, for instance, 
    introduce comments, see [HJSON](https://hjson.github.io)
    to know more about its features. 
__IMPORTANT__: both `json` and `hjson` use `:` instead of
    `=` for assignments. If you type `=`, you'll get a running error.

The next sections explain the different types of variables.

## Global variables

#### Output filename

`csvFileName` sets filename for the output CSV file. 
    The termination `.csv` will be appended if not provided. 
    For instance `self_luminous_1` or 
    `self_luminous_1.csv` are both valid

#### List of instrumental channels

`filterList` sets the list of instrumental channels to be considered.
    Each channel is identified with a wavelength band, `filter` for short. 

  -  There are three filters that may be set 
   (see [Roman at IPAC](https://roman.ipac.caltech.edu/sims/Param_db.html) 
       for details):

      - Narrow Field of View Imager: `NF_Imager`. The inner working angle, IWA, 
        is 155.6 mas (3.1 λ/D) and the outer working angle, OWA, is 
        436.7 mas (8.7 λ/D), where D is the diameter of the primary mirror, 
        2.36 m. 
        The central wavelength λ is 575 nm, and the 
        bandwidth is 10%

      - Single Slit, Prism-based Spectroscopy: `Amici_Spec`. IWA is 
      197.5 mas (3.1 λ/D) and OWA is 567.1 mas (8.9 λ/D). 
      The central wavelength is
      730 nm, and the bandwidth is 15%. The average resolving power is R= 50
  
      - Wide Field of View Imager: `WF_Imager`. IWA is 468.1 mas 
      (6.5 λ/D) and OWA is 1426 mas (19.8 λ/D). 
      The central wavelength is 825 nm, and the bandwidth is 10%.

  - Additionally, there are two __performance__ levels of the
    coronagraph: __optimistic__ and __conservative__:

    - Optimistic: it does not include model uncertainty factors

    - Conservative: it includes current best estimates for model 
        uncertainty factors. The actual IWA/OWA 
        can be found in `json/cgi_etc_exosims.json`.

The particular values for the model uncertainty factors, as well as other
    more specific instrumental parameters used in `cgi_exosims.json`
   can be found in the [tables](../tables/#README.md) directory

In summary, a possible choice for `filterList` could be `CONS_NF_Imager`
for instance. One may specify a list of choices: [`CONS_NF_Imager`, 
`OPTI_NF_Imager`, `CONS_WF_Imager`], etc.

#### Epochs of the observations

The user must specify the start and
    end dates of the observations, `CGI_epoch0` and `CGI_epoch1`, respectively. 
    The notional duration of the coronagraph 
    Tech Demo is 90 days spread along 18 months after
    its comissioning period. The Tech Demo starts
    about 3 months
    after the launch date. For instance, assuming a launch date in mid 2026,
    `CGI_epoch0` would be 09/01/2026 and `CGI_epoch1`
    03/01/2028. Feel free to explore other reasonable alternative dates.

Any time dependent properties of the target that are relevant to the 
    observations, e.g., the apparent location of the exoplanets or the 
    star-exoplanet flux ratio, must be consistent with
    whichever dates are chosen:

  - In the case of __self luminous__ exoplanets, the user must make sure
      that it is the case. See 
   [Self Luminous Exoplanets](#self-luminous-exoplanets) 

  - In the case of __reflected light__ exoplanets, either use the data
   from [Imaging Mission Database](https://plandb.sioslab.com/index.php) 
   or make sure they are consistent. See
   [Reflected Light Exoplanets](#reflected-light-exoplanets) and
   [imd/README](../imd/README.md)

  - For __exozodiacal light__ and __debris disks__, temporal effects shpuld be
      less relevant, if any. However, there are other aspects to take care 
      of, as explained in [Exodust Targets](#exodust-targets)

#### Type of target

The exposure time calculator allows
    one to consider the following types of targets:

  - Self luminous exoplanets: `targetType: 'self luminous'`

  - Reflected light exoplanets: `targetType: 'reflected light'`

  - Exodust targets: `targetType: 'exo dust'`.

More details about each of them can be found in the next sections.
We also provide some guidance about polarimetric observations:
[Polarization](#polarization)

## Self Luminous Exoplanets

The user must supply the values for the following 
list of variables:

- `SNRList`: a list of Signal-to-Noise Ratios, SNR, to be 
    achieved. The exposure time calculator
    will estimate the time that it takes to achieve each of them. If some 
    value cannot be reached, it will assign to it a NaN value 
    (it will look like an empty cell in the
    CSV file). 

Notice that `Roman_Coronagraph_ETC` 
    does not output the limiting SNR
    that might be achieved for each target. If you neeed such value, 
    since the precision of the SNR value should be fine with no more
    than two significant digits,
    you can run a set of SNR values and deduce the 
    limiting SNR value from the last case that
    outputs a real valued integration time, i.e., not a NaN

- `PName`: the exoplanet name. `PName` does
    not require a particular syntax. The common practice is to have the
    name of the host star and a latin letter for the exoplanet

- `hipPName`: for each of the exoplanets in `PName`,
    the corresponding
   [Hipparcos identifier](https://www.cosmos.esa.int/web/hipparcos/catalogues)
     of the host star.
    [EXOSIMS](https://github.com/dsavransky/EXOSIMS)
    will use the 
    Hipparcos identifier to find the stellar properties of the
   star in [SIMBAD](http://simbad.u-strasbg.fr/simbad/).
    DISCLAIMER:  `Roman_Coronagraph_ETC` does _not_ check 
    whether the host star names
    and the corresponding Hipparcos identifiers are correct

- `WA_arcsec`: the projected angular separation of 
    the exoplanet from its host star, measured in arcsec

- `d_AU`: the actual distance of the 
    exoplanet to its host star at the time of the observation, measured
    in Astronomical Units

- `I_deg`: the visual inclination of the exoplanet, measured in degrees

- `FR_filterName`: the star-exoplanet flux ratio 
    for each instrumnetal band under consideration, see `filterList` before

The file `json/cgi_etc_setup.hjson` provides specific examples
    for each of the variables above.

## Reflected Light Exoplanets

The user must supply the values for the following
list of variables:

- `SNRList`: see the description in 
[Self Luminous Exoplanets](#self-luminous-exoplanets)
 
- `PName`: see the description in
   [Self Luminous Exoplanets](#self-luminous-exoplanets). A difference
    with respect to the self luminous exoplanet case is that 
    `PName` is used to find the orbital epehemeris of the planet. Thus,
    although `PName` can be set to any string, it has to match
    the name used when storing the orbital ephemeris from 
  [Imaging Mission Database](https://plandb.sioslab.com/index.php). 
  See [imd/README](../imd/README.md)

- `hipPName`: see the description in
[Self Luminous Exoplanets](#self-luminous-exoplanets)

Optionally, in the case of reflected light planets, because of
    its greater exposure time and time variability of the exoplanet
    characteristics, the tool can show the result 
  as a bar plot. [output/figures/README](../output/figures/README.md). 
  The options are:

  - `bar_plot`: whether to get the plot or not

  - `maxIntTimeHours`: the maximum integration time per target that is 
         used as a cut-off in the bar plot

The file `json/cgi_etc_setup.hjson` provides specific examples
    for each of the variables above.

### Flux ratios in the case of reflected light exoplanets

This case is different to other types of targets because
    they may have a more noticeable
    orbital motion along the Technology Demonstration Phase
    of the Roman Coronagraph Instrument.
    For each reflected light exoplanet of interest, 
    the user must download from
  [Imaging Mission Database](https://plandb.sioslab.com/index.php)
    a file with the planetary ephemeris and store it in `imd/`:
    click on `Save All Orbit Data` at the top,
    left corner of the page with the exoplanet's information.
    `Roman_Coronagraph_ETC` will use this information to derive a set of
    integration times and choose the date
    with the shortest integration time.

Remember that the name of the exoplanet in the filename with the
  ephemeris must match `PName`.
  A simple choice is to use the same notation
  as in the filenames from 
  [Imaging Mission Database](https://plandb.sioslab.com/index.php).
  See [imd/README](../imd/README.md) for an example.
  `Roman_Coronagraph_ETC` provides one example in `json/cgi_etc_setup.hjson`
  and `imd/`.

If your exoplanet of interest is not available in 
   [Imaging Mission Database](https://plandb.sioslab.com/index.php), 
    or you would like to consider other orbital parameters, you can run
    `Roman_Coronagraph_ETC` as if it were
   the case of a [Self Luminous Exoplanet](#self-luminous-exoplanets)
    for a particular orbital epoch.

## Exodust Targets
 
The user must supply the values for the following
list of variables:

- `SNRList`: see the description in
[Self Luminous Exoplanets](#self-luminous-exoplanets)

- `starNameCommon`: any string that identifies your target.

- `starNameHip`: the 
  [Hipparcos identifier](https://www.cosmos.esa.int/web/hipparcos/catalogues)
    of the star in the system.

The file `json/cgi_etc_setup.hjson` provides specific examples
    for each of the variables above.

- `WA_arcsec`: the angular separation of the area of interest 
    from the host star, measured in arcsec

- `FR_filterName`: the equivalent point source flux ratio corresponding to 
    the estimated surface brightness of the area of interest

In the following we provide some guidance, but the process of translating
    the surface brightness of a exodust model to a point source equivalent is
    not trivial, and we invite you to read the references provided. 

First, one has to translate surface brightness from `SB` in mag/arcsec^2 to
    brightness per resolution element `resel`. 
    In the following, for simplicity, we will consider the
    case of a __spatially invariant PSF__. Otherwise, the expressions
    would need to account for the spatial PSF variation.
    The Roman Coronagraph Instrument team provides that information in
    a set of 
  [Public Simulated Images](https://roman.ipac.caltech.edu/sims/Coronagraph_public_images.html).
    
`resel` is commonly approximated by the area covered by a 
    square whose side is the Full Width at Half Maximum, FWHM,
    of the beam, also known as
    PSF core. With this assumption, the `brightness per resel` is:

`10^(-SB/2.5) * (FWHM_mas/1000)^2`

where `SB` is in units of mag/arcsec^2 and 
    `FWHM_mas` is in units of 
    milli-arcsec. The FWHM of the beam can be obtained from 
  [Public Simulated Images](https://roman.ipac.caltech.edu/sims/Coronagraph_public_images.html)
or approximated as an Airy disk from 
  [Roman's parameters at IPAC](https://roman.ipac.caltech.edu/sims/Param_db.html#coronagraph_mode)
    depending on the required precision.

The following step is to convert this `surface brightness per resel` to 
    an equivalent point source brightness. 
    This step is done to
    re-use the same exposure time methods in the case of exodust as
    in the case of exoplanets.
    Let's call this conversion factor, the __`gain_factor`__ factor, because it 
    represents the contribution from neighbor areas to the integrated flux 
    within a `resel`. 
    This conversion factor depends on several factors, 
    both instrumental (e.g., the spatial PSF model) and 
    astrophysical (e.g., the spatial distribution of the disk
    brightness once projected along the line of sight). We provide
    and example that gives an overview of the process involved, but a
    precise derivation requires some more computations.
    See, for instance,
[K. Milani, and E.S. Douglas (2021)](https://arxiv.org/abs/2106.09122)

John Debes (STScI) has kindly provided an example using the PSF
    model from the Roman Coronagraph Instrument 
  [OS9](https://roman.ipac.caltech.edu/sims/Coronagraph_public_images.html)
    for the case of the Narrow Field of View Imager and some
  [Circumstellar Disks Simulations](https://roman.ipac.caltech.edu/sims/Circumstellar_Disk_Sims.html) 
    publicly available
    The `gain_factor` was derived in two different scenarios: dust rings at
    different angular distances from the host star and a diffuse disk that
    extended beyond the Outer Working Angle of the Coronagraph (OWA).
    The PSF spatial distortion is greater near the Immer Working Angle (IWA),
    
The values of the `gain_factor` at different angular distances were:

- Rings: 2.1, 2.3, and 2.6 at 0.2 0.3, and 0.4 arcsec, respectively

- Extended disk: 2.8, 4.0, 5.0, and 5.0 at 0.15, 0.2, 0.3, and 0.4 arcsec, 
    respectively

In summary, the equivalent point source brightness 
in the case that the local spatial variation of the PSF can be neglected
within the area of interest can be approximated as:

`10^[(V_star - SB)/2.5] * (FWHM_mas/1000)^2 * gain_factor`

where `V_star` is the V magnitude of the host star, `SB` is the surface 
    brightness of the region of interest in units of mag/arcsec^2,
    `FWHM_mas` is the FWHM of the beam under consideration, 
    in units of milli-arcsec, and `gain_factor` is the factor explained
    previously. 

Finally, notice that sometimes one has an estimation
    of the "delta" magnitude of the exodust emission. In that case, the
    stellar magnitude has already been subtracted. 

__Remember that the above expressions may need to be integrated spatially__
__if the disk and/or PSF characteristics vary significantly within the
area of interest.__

## Polarization

Polarization with the Roman Coronagraph Instrument can be
approached in the following way for first order estimations:

- Convert the surface brightness of the source into an equivalent magnitude 
per resel, see [Exodust Targets](#exodust-targets).

- Take a factor of 2 hit in transmission from the polarizer

- The Signal-to-Noise requirement is nominally 100:1 per resel per single 
linear polarization which gives a required exposure time per Wollaston prism 
per telescope roll. Because there are two prisms and two rolls involved,
the exposure time will indeed be 4x longer than that estimate.

# Limitations

- `Roman_Coronagraph_ETC` supports the 3 nominal instrumental modes of the
  Roman Coronagraph Instrument, see [above](#list-of-instrumental-channels).
  Spectroscopy in Band 2 is not included

- If integration times are shorter than half an hour,
    they are a lower bound, because the noise models 
    do not include rapid changes of the speckle residuals. 
    On the other hand, since the integration times are short, one
    can usually set a higher SNR that requires longer integration times,
    and still be fine within an observing program

- Host stars must have a 
  [Hipparcos identifier](https://www.cosmos.esa.int/web/hipparcos/catalogues).
    This should not be a strong limitation since the Hipparcos catalog is
    complete for all stars that the Roman Coronagraph
    Instrument can acquire in coronagraphic mode with reasonable
    performance. See
  [catalog/README](../catalog/README.md).
  [EXOSIMS](https://github.com/dsavransky/EXOSIMS)
    can handle any host star. You can modify `Roman_Coronagraph_ETC` 
    accordingly (recall to create a new branch)

- In the case of `Reflected Light Exoplanets`, the orbital data are
  retrieved from [Imaging Mission Database](https://plandb.sioslab.com/index.php).
    Any type of limitations in Imaging Mission Database are inherited into
    `Roman_Coronagraph_ETC`. 
    If this is a limitation, let's recall that one can use the case of 
    `Self Luminous Exoplanets` and input values that correspond to a particular
  observation epoch, see [Self Luminous Exoplanets](#self-luminous-exoplanets)
  above

- `Roman_Coronagraph_ETC` does not provide the limiting value of the 
    Signal-to-Noise
    (SNR) that may be achieved for a given observation. It can be obtained 
    modifying the list of target SNR,
  see for instance [Self Luminous Exoplanets](#self-luminous-exoplanets) above, 
    and deriving an SNR cutoff based on some limiting integration time of
    your choice. Recall that empty cells in the output CSV files mean
    that the observation is not possible, 
  [output/README](../output/README.md)

- The level of exozodi is set by `magEZ` in `json/cgi_exosims.json`. 
    `Roman_Coronagraph_ETC` does not have an option to set a list of values.
  [Recall](#exosims) that the exozodiacal dust contributes to
    the shot noise only

- Current and upcoming Validation Activities, Ground Tests of the
    Roman Coronagraph Instrument and R&D activitites 
    will be conducted before its delivery and launch. 
    Some of the instrumental performance parameters can change. We will advertise
    such changes in the Git updates. You can also read the time stamp
  in the instrumental [tables](../tables/) directory

