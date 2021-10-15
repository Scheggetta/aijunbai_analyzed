#!/usr/bin/env pypy

import common
import uct_statistics_common as usc

if __name__ == "__main__":
    # Creation of a csv file for statistics as well
    common.main(usc.uct)
