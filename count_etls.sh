#!/bin/bash
sort | uniq -c | tee >(awk '{s+=$1} END {printf "%d ETLs -------", s}') | cat
