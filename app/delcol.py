# coding=utf-8

import models
import sys

if __name__ == "__main__":
    models.connect()
    for i in range(1,len(sys.argv)):
        models.delcol(sys.argv[i])
