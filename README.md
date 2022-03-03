![](logo_Roman_Coronagraph_ETC.png)
Roman Coronagraph Exposure Time Calculator

# Scope of the Roman Coronagraph Exposure Time Calculator

The Roman Coronagraph Exposure Time Calculator
    (`Roman_Coronagraph_ETC` for short)
    is the public version of the 
    exposure time calculator of the 
  [Coronagraph Instrument](https://roman.gsfc.nasa.gov/coronagraph.html) 
    aboard the 
  [Nancy Grace Roman Space Telescope](https://roman.gsfc.nasa.gov)
  funded by [NASA](https://www.nasa.gov).
    `Roman_Coronagraph_ETC` methods are based upon peer reviewed research
    articles (see [Bibliography](#bibliography))
    and a collection of instrumental and 
    modeling parameters of both the Coronagraph Instrument
    and the Nancy Grace Roman Space Telescope. The values in these 
    files do not contain any ITAR or export control information. 
    `Roman_Coronagraph_ETC` is licensed under
  [Apache v2](https://www.apache.org/licenses/LICENSE-2.0).

# Running the Roman Coronagraph ETC

In [IPAC/Roman's page](https://roman.ipac.caltech.edu/sims/ETC.html) you
can find a presentation and a live tutorial.

- Follow the [Installation Notes](#installation-notes)

- Move to the directory where `Roman_Coronagraph_ETC` is installed

- Verify that `scripts/config.py` has your local installation path

- Verify that you have copied `json/cgi_etc_setup_ref.hjson` to
    `json/cgi_etc_setup.hjson` and `json/cgi_etc_exosims_ref.json`
    to `json/cgi_etc_exosims.json`, see 
  [Installation Notes](#installation-notes)

- Activate conda's environment: 
    `conda activate <your_roman_coronagraph_etc_environment>`

- Edit `json/cgi_etc_setup.hjson`. See the documentation below.

- Get the results running `python roman_coronagraph_etc.py`

The screen will print out some messages from EXOSIMS modules.
    The __output__ is stored as CSV tables in `output/csv/`. 
  [README](output/README.md)

Read the documentation in each directory for further details.
In alphabetical order:

- `catalog/`: add your stars of interest.
[README](catalog/README.md)

- `imd/`: it contains files
with specific exoplanetary predictions. [README](imd/README.md)

- `json/`: setup files for 
  [EXOSIMS](https://github.com/dsavransky/EXOSIMS)
    and for `Roman_Coronagraph_ETC`. __Read this first__. 
  [README](json/README.md)

- `output/`: directory where the integration times are stored. 
There is also an optional figure for the case of reflected 
light exoplanets, only.
[README](output/README.md)

- `scripts/`: directory with the `Roman_Coronagraph_ETC` methods.
[README](scripts/README.md)

- Target accessibility can be derived from

  - Either 
[CGI Target Accessibility](https://github.com/nasavbailey/CGI_target_accessibility).
Follow the examples in its Jupyter Notebook.
  - Or, the ouput CSV file in `output/csv/` 
[README](output/README.md)

- List of current [Limitations](json/README.md#limitations) 
and [FAQ](faq/README.md)

# Installation Notes

Both [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)
  and [GitHub Desktop](https://desktop.github.com)
    are used in the instructions below.
    At this time, 
  [astroconda](https://astroconda.readthedocs.io/en/latest/getting_started.html)
    does not support Microsoft Windows.
  [Additional Installation Notes](#additional-installation-notes)
    have some suggestions on how to install `Roman_Coronagraph_ETC`
    in case some of the steps below cannot be followed, 
    albeit without any additional support, neither we provide any
    technical support for sorting out third-party software 
  installation issues, including [python](https://www.python.org).

Follow these steps:

- Install/Update 
[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).
A common choice is to install miniconda, ~350 Mb, in any directory
other than `$HOME`. Pick up python 3.7 if possible because some of the 
packages from STScI are for 3.7 or less.

- Run these two commands from
[STScI](https://astroconda.readthedocs.io/en/latest/installation.html#configure-conda-to-use-the-astroconda-channel%20[https://astroconda.readthedocs.io/en/latest/installation.html#configure-conda-to-use-the-astroconda-channel]):

	- `conda config --add channels http://ssb.stsci.edu/astroconda`
	
	- `conda create -n <roman_coronagraph_etc_environment> python=3.x stsci`

    where `<roman_coronagraph_etc_environment>` is the name you want to give to 
    the conda environment related to
    `Roman_Coronagraph_ETC`.
    For instance, 
    `conda create -n cgi_etc python=3.x stsci`, where
    `3.x` is the python version
    installed in the previous step. If you need 
    to remove
    this conda environment at any time, follow the steps
  in [Uninstalling the Roman Coronagraph Exposure Time Calculator](#uninstalling-the-roman-coronagraph-exposure-time-calculator)

- __Activate your environment__:
    `conda activate <roman_coronagraph_etc_environment>`

- Install [pandas](https://pandas.pydata.org): 
    `conda install -c anaconda pandas`

- Install [hjson](https://hjson.github.io): 
    `conda install -c databand.ai hjson`. If you ever have an issue with hjson's installation, check 
  [anaconda packages](https://anaconda.org/search?q=hjson) 
    for a more recent package. 

- Install/Update [GitHub Desktop](https://desktop.github.com). 
    Note: if you cannot,
  see [Additional Installation Notes](#additional-installation-notes).

- Use GitHub Desktop to clone
  [EXOSIMS](https://github.com/dsavransky/EXOSIMS) (`File->Clone Repository`)
    choosing any `local path` of your preference: for instance, you 
    can choose/create `/Users/user_name/.../GitHub/` or _any_ other directory

- Follow
  [EXOSIMS](https://github.com/dsavransky/EXOSIMS) 
    quick installation instructions: 
    open a terminal session, move to its installation directory, 
    then into `EXOSIMS/` (containing setup.py) and execute
    `pip install -e .`

- Install `Roman_Coronagraph_ETC`:

  - Use GitHub Desktop to clone
  this repository (`File->Clone Repository`)
    choosing any `local path` of your preference: for instance, you
    can choose/create `/Users/user_name/.../GitHub/` or _any_ other directory 

  - Open a terminal session, move to its installation directory, and 
    make this local copy of `config_ref.py`:

    - `cp config_ref.py config.py`

    Edit `config.py`, which will not be traced by git,
    and set `INSTALLATION_PATH` to the full installation path. 
    For instance, following the suggestion before:
    `INSTALLATION_PATH=/Users/user_name/.../GitHub/Roman_Coronagraph_ETC/`

      
  - Execute `python cgi_etc_test.py` in the installation directory. 
    If the installation is succesful, 
    the following message will be printed out: 

```
    >> All modules related to Roman Coronagraph ETC succesfully loaded
    >> The installation path in config.py is <INSTALLATION_PATH>
```
   - Verify `<INSTALLATION_PATH>` is the installation 
       path of `Roman_Coronagraph_ETC`. Otherwise, edit `config.py` accordingly

  - Make this local copy of the setup files in `json/`:
    
    - `cp json/cgi_etc_setup_ref.hjson json/cgi_etc_setup.hjson`

    - `cp json/cgi_etc_exosims_ref.json json/cgi_etc_exosims.json`

    `json/cgi_etc_setup.hjson` and `json/cgi_etc_setup.hjson` are
        the setup files that the user will edit, not the ones with `_ref`,
        which are part of git

  - If there is an issue importing EXOSIMS, follow these steps 
    (needed only once). Add 
    `export PYTHONPATH=$PYTHONPATH:<Full_Local_Path_Installation_Of_EXOSIMS`
    to your runcom shell script (most likely `.zshrc` or `.bashrc`).
    Execute `source ~/.zshrc` (or `source ~/.bashrc`). 
    Execute `conda activate <roman_coronagraph_etc_environment>`. 
    Make sure you are in the installation path of 
    `Roman_Coronagraph_ETC` and execute `python cgi_etc_test.py` again

  - If you decide to modify the code make sure to create a new branch for 
your work

You are ready to run the Roman Coronagraph Exposure Time Calculator.
  Read [Running the Roman Coronagraph ETC](#running-the-roman-coronagraph-etc)

# Uninstalling the Roman Coronagraph Exposure Time Calculator

Since it is a git repository, you have two options:

- Either delete everything in your local copy, e.g., in
    `/Users/user_name/.../GitHub/Roman_Coronagraph_ETC/`,
    executing `rm -rf /Users/user_name/.../GitHub/Roman_Coronagraph_ETC/`.
    This is a _forced_ remove. Make sure what you'll be deleting before
    pressing INTRO. Note: you can also remove it from `Git` only:
    `rm -rf /Users/user_name/.../GitHub/Roman_Coronagraph_ETC/.git`

Finally, you may also want to remove the conda environment (and
    the packages that were installed with it):

- conda deactivate (in case you are in `<roman_coronagraph_etc_environment>`)

- `conda env remove -n <roman_coronagraph_etc_environment>`

# Additional Installation Notes

The following suggestions are provided without any additional support. 
If you encounter any issues, please consult the online,
free documentation of each third-party software.

- If you cannot use `GitHub Desktop`:

   -  Open a terminal session. Move to the local 
  directory where both [EXOSIMS](https://github.com/dsavransky/EXOSIMS) and  
  the Roman Coronagraph ETC will be installed, 
    for instance, `/Users/user_name/.../GitHub/`

  - Execute `git clone https://github.com/dsavransky/EXOSIMS.git`.

    - If GitHub requires you to provide a token
        associated with your user, follow the instructions about
  [GitHub Tokens](https://github.com/settings/tokens). 
        Copy the (long) password safely somewhere.
        Tip: if you want, you can avoid its expiration. 
        After installing the token, execute these two commands
        in a terminal: 
        `git config --global credential.helper cache`, and 
        `git config --global credential.helper "cache --timeout=2500000"`

    - Continue with EXOSIMS installation:
        move into `EXOSIMS/` (containing setup.py) and execute
        `pip install -e .`



  - Roman Coronagraph ETC: move to the installation directory,
        for instance, `/Users/user_name/.../GitHub/`
    - Execute `git clone https://github.com/hsergi/Roman_Coronagraph_ETC.git`.
        Use the token generated before or geenrate a new token following
        similar steps as explained before

- If you already have `astropy` installed, it's usually convenient to keep 
it up to date. If you have installed `conda`, 
you can update `astropy` executing `conda astropy update` in any terminal 
session

# Persons of Contact
- Sergi Hildebrandt Rafels (sergi.hildebrandt.rafels@jpl.nasa.gov)

# Affiliation
Jet Propulsion Laboratory, California Institute of Technology

# Acknowledgement 
© 2021. Government sponsorship acknowledged. The research was 
carried out in part at the Jet Propulsion Laboratory, California Institute of 
Technology, under a contract with the National Aeronautics and Space 
Administration. __Sergi Hildebrandt Rafels__ 
acknowledges support by NASA Grant NNG16PJ27C, 
which supports the Turnbull Roman CGI Science Investigation Team.
The Roman Coronagraph Instrument Exposure Time Calculator
is a user interface based upon previous work done in the
Roman Coronagraph Instrument team.
In particular, __Bijan Nemati__ (University of Alabama in Huntsville) 
and collaborators have developed a 
detailed exposure time calculator, written in Excel, 
that is used by the Roman Coronagraph team,
see the [Bibliography](#bibliography).
__Brian Kern__ (Jet Propulsion Laboratory,
California Institute of Technology) has provided the
public version of the CSV tables.
__Corey Spohn__ and __Dmitry Savransky__ 
(Cornell University, SIOSlab) have
developed a python version of the exposure time calculator.
Other significant contributions
have been made by __Vanessa Bailey__
(Jet Propulsion Laboratory, California 
Institute of Technology), 
__John Debes__ (STScI), 
__Ewan S. Douglas__ (The University of Arizona), 
__Dean Keithly__ (Cornell University, SIOSlab)
and __Leah Sheldon__ (University of Alabama in Huntsville).

# Bibliography

- Bijan Nemati, "Photon counting and precision photometry for the 
Roman Space Telescope Coronagraph," Proc. SPIE 11443, 
Space Telescopes and Instrumentation 2020: Optical, 
Infrared, and Millimeter Wave, 114435F (13 December 2020). 
[doi: 10.1117/12.2575983](https://doi.org/10.1117/12.2575983)

- Bijan Nemati, H. Philip Stahl, Mark T. Stahl, 
Garreth J. J. Ruane, Leah J. Sheldon,
"Method for deriving optical telescope performance specifications for 
Earth-detecting coronagraphs,"
J. of Astronomical Telescopes, Instruments, and Systems, 6(3), 
039002 (2020). 
[doi:10.1117/1.JATIS.6.3.039002](https://doi.org/10.1117/1.JATIS.6.3.039002)

- Dmitry Savransky, C. Delacroix, D. Garrett, "EXOSIMS: Exoplanet Open-Source 
Imaging Mission Simulator," Astrophysics Source Code Library, 6, 2017. 
[2017ascl.soft0610S](https://ui.adsabs.harvard.edu/abs/2017ascl.soft06010S/abstract)

- Dean Keithly, D. Savransky, D. Garrett, C. Delacroix, G. Soto,
"Optimal scheduling of exoplanet direct imaging single-visit observations 
of a blind search survey,"  J. of Astronomical Telescopes, Instruments, and Systems, 6(2), 027001,
(2020). 
[doi:10.1117/1/JATIS.6.2.027001](https://doi.org/10.1117/1.JATIS.6.2.027001)


- Dmitry Savransky, D. Garrett,
"WFIRST-AFTA coronagraph science yield modeling with EXOSIMS,"
J. of Astronomical Telescopes, Instruments, and Systems, 2(1), 011006,
(2015). [doi:10.1117/1.JATIS.2.1.011006](https://doi.org/10.1117/1.JATIS.2.1.011006)

# Use Policy

If you use this code in presentations or publications, please adhere to the follwing policy use:

- Add the 5 references posted on the bibliography section on GitHub: bibliography
 
- If data from Imaging Mission Database were used, adhere to their use policy: IMD policy
 
- Cite the ACSL entry of the Roman CGI ETC tool: https://ascl.net/code/v/3217

