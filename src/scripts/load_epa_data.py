"""
Script for automating the load of data from EPA
"""


import argparse
import logging
import sys
import os
import urllib2
import zipfile
import subprocess
import shutil

# EPA raw dir
# Hardcoded because it is hardcoded in the R Script
eparaw_dir = "epa-raw" 

# Argument parsing
parser = argparse.ArgumentParser("python load_epa_data.py")
parser.add_argument("--r_script",
                    dest='r_script',
                    action='store',
                    default='leer_epa.R',
                    help="Path to R script to process the data")
parser.add_argument("--zipfile_url",
                    dest='zipfile_url',
                    action='store',
                    default='ftp://www.ine.es/temas/epa/datos_1t14.zip',
                    help="URL to the EPA ZIP file")
parser.add_argument("-v",
                    dest='verbose',
                    action='store_true',
                    help="Verbose mode")
parser.add_argument("--logfile",
                    dest='logfile',
                    default=None,
                    help="Optional log file")
args = parser.parse_args()

# Logging settings
loglevel = logging.INFO if args.verbose else logging.ERROR
logger = logging.getLogger("load_epa_data")
logger.setLevel(loglevel)
formatter = logging.Formatter('%(levelname)s: %(asctime)s: %(message)s')
if args.logfile:
    handler = logging.FileHandler(args.logfile)
else:
    handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Execution of the main script
logger.info("Starting the execution {}".format(" ".join(sys.argv)))

# ZIP file download and extract
logger.info("Downloading file from {}".format(args.zipfile_url))
zip_raw = urllib2.urlopen(args.zipfile_url).read()
if not os.path.exists(eparaw_dir):
    logger.info("Creating {}".format(eparaw_dir))
    os.mkdir(eparaw_dir)
zip_dest = os.path.join(eparaw_dir, os.path.basename(args.zipfile_url))
logger.info("Storing the file in {}".format(zip_dest))
zip_file = open(zip_dest, "wb")
zip_file.write(zip_raw)
zip_file.close()
with zipfile.ZipFile(zip_dest, "r") as z_file:
    logger.info("Extracting {} to {}".format(" ".join(z_file.namelist()),
                                             eparaw_dir))
    res = z_file.extractall(eparaw_dir)
# Cleanup
logger.info("Deleting {}".format(zip_dest))
os.remove(zip_dest)

# Execution of the R Script
logger.info("Executing Rscript {}".format(args.r_script))
p = subprocess.Popen(["Rscript", args.r_script], stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
res, err = p.communicate()
logger.info("Exection of Rscript {} has finished".format(args.r_script))

# Tailoring the csv file
csv_file = "datos_epa.csv"  # Fixed filename
logger.info("Trimming first line of {}".format(csv_file))
csv_f = open(csv_file, "r")
csv_lines = csv_f.readlines()
csv_f.close()
# Remove the first line
csv_f = open(csv_file, "w")
csv_f.writelines(csv_lines[1:])
csv_f.close()

# Execution of the loadmicrodata.py script
logger.info("Executing python load_microdata.py {}".format(csv_file))
p = subprocess.Popen(["python", "load_microdata.py", csv_file],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
res, err = p.communicate()
if err:
    logger.error("Error executing load_microdata.py: {}".format(err))
    raise SystemExit(1)
logger.info("Finished python load_microdata.py {}".format(csv_file))

# Execution of the load_ratequeries.py script
logger.info("Executing python load_ratequeries.py")
p = subprocess.Popen(["python", "load_ratequeries.py"],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
res, err = p.communicate()
if err:
    logger.error("Error executing load_ratequeries.py: {}".format(err))
    raise SystemExit(1)
logger.info("Finished python load_ratequeries.py")

# Cleanup
logger.info("Deleting {}".format(csv_file))
os.remove(csv_file)
logger.info("Deleting {}".format(eparaw_dir))
shutil.rmtree(eparaw_dir)

# Finish
logger.info("Finished the execution of {}".format(" ".join(sys.argv)))
