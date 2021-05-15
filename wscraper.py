#!/usr/bin/python3

import datetime
import time
import hashlib
import wget
import os
import sys
import getopt
from urllib.request import urlopen

latest_hash = 'null'


# -----UTILITIES----- #
def log_info(message, color: bool):
    if color:
        print("{}[{}]{}[i]{}{}".format(
            "\033[1;34;40m ",
            datetime.datetime.now(),
            "\033[1;32;40m ",
            "\033[0;37;40m ",
            message
        ))
    else:
        print("[{}][i] ".format(datetime.datetime.now()) + message)


def log_error(message, color: bool):
    if color:
        print("{}[{}]{}[!]{}{}".format(
            "\033[1;34;40m ",
            datetime.datetime.now(),
            "\033[1;91;40m ",
            "\033[0;37;40m ",
            message
        ))
    else:
        print("[{}][!] ".format(datetime.datetime.now()) + message)


def calc_hash(url):
    connection = urlopen(url)
    max_file_size = 100 * 1024 * 1024
    md5sum = hashlib.md5()

    total_read = 0
    while True:
        data = connection.read(4096)
        total_read += 4096

        if not data or total_read > max_file_size:
            break

        md5sum.update(data)

    return md5sum.hexdigest()


# -----LOOP----- #
def start_downloading(webcam_url: str, sleep: int, color: bool):
    global latest_hash
    while True:
        try:
            curr_hash = calc_hash(webcam_url)
            log_info("Latest hash is " + latest_hash + " ; Server responded with hash " + curr_hash, color)
        except:
            log_error("Cannot get server image hash", color)

        try:
            if curr_hash != latest_hash:
                log_info("Downloading new image with hash " + curr_hash, color)
                filename = "output/" + str(time.time()) + "_" + curr_hash.upper() + ".jpg"
                wget.download(webcam_url, filename)
                latest_hash = curr_hash
                print()
        except:
            log_error("Cannot download new image", color)

        time.sleep(sleep)


def main(argv):
    url = ''
    delay = 60
    color = True
    try:
        opts, args = getopt.getopt(argv, "hu:d:c", ["url=", "delay=", "color="])
    except getopt.GetoptError:
        print('scrape.py -u <url> -d <delay> [-c]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('scrape.py -u <url> -d <delay> [-c]')
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-d", "--delay"):
            delay = arg
        elif opt in ("-c", "--color"):
            color = False
    log_info("Starting the scraper...", color)
    if not os.path.exists("output"):
        os.makedirs("output")
    start_downloading(url, int(delay), color)


if __name__ == "__main__":
    main(sys.argv[1:])
