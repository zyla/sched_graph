#!/bin/sh
export RDTSC_S=rdtsc_`uname`.s
exec cc -o timer timer.c $RDTSC_S
