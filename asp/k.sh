#!/bin/bash

#clingo asp/knights_tour.lp -c n=8 --time-limit=300
clingo knights_tour.lp database.lp -c n=6 --time-limit=20