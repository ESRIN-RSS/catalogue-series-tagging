import logging
import re, os
import time
from datetime import datetime, timedelta
import shutil
import argparse
import subprocess
import requests
import zipfile
import uuid

def setup_cmd_args():
    """Setup command line arguments."""
    parser = argparse.ArgumentParser(description="Automatically check the results for each datatset in the list\n", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--dslist", help="The dataset list.")
    parser.add_argument("--storage", help="Folder to look for data.")
    return parser.parse_args()


def get_list_of_results(url, regex, max_retries=10, auth=('', '')):
    """Obtain the number of results found in the response message of
    a catalog query.

    :param url: catalog query url
    :param regex: regex to obtain the totalResults from the response message
    :param max_retries: repeat X times if query fails
    :param auth: tuple with (user,password) if url needs authentication
    :return: number of total results obtained by the query
    """
    resultslist = []
    for _ in range(max_retries):
        page = requests.get(url, auth=auth)
        if not page.status_code==200:
            time.sleep(5)
            continue
        else:
            break
    if not regex is None:
        for m in re.finditer(regex, str(page.content)):
            resultslist.append(m.group(1))
    else:
        resultslist = page.text.split("\n")
        resultslist = list(filter(None, resultslist))
    return resultslist, len(resultslist)


def find(root, file, first=False):
    for d, subD, f in os.walk(root):
        if file in f:
            print("{0} : {1}".format(file, d))
            if first == True:
                break


def main():
    args = setup_cmd_args()
    # logging.basicConfig(filename=os.path.join(args.outputlist, 'gpod_cophub_sync_check.log'), level=logging.INFO,
    #                     format='INFO: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    # logging.info("------STARTED RUN------")

    with open(args.dslist, "r") as ll:
        datasets = ll.readlines()
    datasets = list(map(lambda x: x.strip(), datasets))

    print("Dataset, Products_in_GPOD, Path_in_storage")
    for ds in datasets:
        url = "http://grid-eo-catalog.esrin.esa.int/catalogue/gpod/{}/files?count=*".format(ds)
        try:
            results_list_gpod_i, results_list_gpod_count = get_list_of_results(url, None)
        except:
            logging.info(f"Some problem occurred when connecting to GPOD!")

        path_in_data = [line[2:] for line in subprocess.check_output(f"find {args.storage} -maxdepth 3 -name '{ds}'", shell=True).splitlines()]
        print(f"{ds}, {results_list_gpod_count}, {path_in_data}")

        # for p in results_list_gpod_i:
        #     paths = [line[2:] for line in subprocess.check_output(f"find . -iname '{p}'", shell=True).splitlines()]
        #     # find(f'/data/eo/',p)
        #     print(paths)


if __name__ == '__main__':
    main()