# Scope

This directory contains files
from [Imaging Mission Database](https://plandb.sioslab.com/index.php)
that provide information about the planet's ephemeris,
the star-planet flux ratio along the orbit, for different
levels of cloud density, see the 
[documentation](https://plandb.sioslab.com/docs/html/index.html) 
in [Imaging Mission Database](https://plandb.sioslab.com/index.php). 
It also provides completeness predictions for the different 
instrumental performance scenarios covered by this ETC, namely:
conservatuve and optimistic.

# Filenames and Planet Names in the Setup File

The filenames downloaded from 
[Imaging Mission Database](https://plandb.sioslab.com/index.php)
have the name of the exoplanet with `_` (underscores).
As explained in [json/README](../json/README.md),
`PName` in `json/cgi_etc_setup.hjson` must be set to the _same_
name with `_` replaced by ` ` (blank spaces). For instance,
`14_Her_b` would be written in `json/cgi_etc_setup.hjson` as
`14 Her b`. See `json/cgi_etc_setup.hjson` for a complete example.
