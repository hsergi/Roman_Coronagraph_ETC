# Scope

This directory contains the high-level methods that estimate the 
    integration times of the Roman Coronagraph Instrument
    aboard the Nancy Grace Roman Space Telescope,
    `Roman_Coronagraph_ETC` for short.
    The actual computations for a specific target happen in 
  [EXOSIMS](https://github.com/dsavransky/EXOSIMS), 
  see [Acknowledgement](../README.md#acknowledgement). 

# Scripts

There are three scripts related with integration times.
    One for each target type:

- `cgi_etc_sl.py` is used for self luminous exoplanets 

- `cgi_etc_rv_shortest_integration_time.py` is used for reflected 
    light exoplanets

- `cgi_etc_dust.py` is used for exodust targets

# How to run them

[json/README.md](../json/README.md) describes in detail how to run the
`Roman_Coronagraph_ETC`, and some other specifics of each target type. 

# Output

The output is a CSV file. [output/README](../output/README.md)

# Limitations

Read the [Limitations](../json/README.md#limitations) in the main README file

