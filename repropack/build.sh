#!/usr/bin/env bash

# Copyright 2022, Sabrina Haberl <sabrina.haberl@st.oth-regensburg.de>
# Copying an distribution of this file, with or without modification
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty
# SPDX-License-Identifier: FSFAP

# build docker container
docker build -t repropack .

# run image
docker run -it -p 445:445 -p 139:139 -d repropack

# copy output to output folder
mkdir output
last_id=$(docker ps -n -1 -q)
docker cp $last_id:/home/repro/Report.pdf ./output
docker cp $last_id:/home/repro/Report.tex ./output
docker cp $last_id:/home/repro/res/scripts/figure ./output
