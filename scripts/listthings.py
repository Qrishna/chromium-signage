#!/usr/bin/env python3
import glob
import os
htmlpages = glob.glob("html/*")
print(" ".join([os.path.abspath(htmlpages[x]) for x in range(0, len(htmlpages))]))