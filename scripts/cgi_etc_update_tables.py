# Run it in a python session having activated the corresponding environment
# IMPORTANT: it may be helpful to first *discard* all the cahnges in GitHub Desktop about csv_fix files,
# update CGI_Perf, and then run these lines below:

# This step is used to format the csv files from CGI_Perf so that EXOSIMS has no issues accessing the values
from EXOSIMS.util.csv_fix import csv_fix

csv_fix('/Users/srhildeb/Documents/GitHub/CGI_Perf/EBcsvData/', # Replace by your local installation of CGI_Perf
        CS_ = [("\"#", "#"),
               ("\n\"","\"")],
        CGPERF=[("I", "intensity"),
                ("occTrans", "occ_trans"),
                ("contrast", "core_contrast"),
                ("PSFpeak","core_mean_intensity"),
                ("area_sq_arcsec", "core_area"),
                ("coreThruput", "core_thruput")])

