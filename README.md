This program can visualize how your OS scheduler schedules processes.

WARNING: This is "research quality" (read: buggy, undocumented and hard to use)
software. But it produces pretty pictures, see `example_Linux.png` and `example_Minix.png`.

Restrictions:

- Uses x86-specific instructions

## Usage on Linux

Go to `timer` directory, run `build.sh`.

The `timer` program will create as many processes as arguments given to it.
The arguments are arbitrary integers passed to `setup_process` function.

*Important*. The program has to run on the same CPU core the whole time, else
the results will be pretty random.

Example:

    cd timer
    taskset -c 0 ./timer 1 2 3

The `taskset` command binds the process to the first CPU core.

Some data files should appear in the `timer/data` directory. Pass them to the
`plot.py` script like this:

    ./plot.py timer/data/p*.log

and see resulting image in `lol.png`.

The script requires `Pillow` library for Python.

## Usage on Minix

Copy the `timer` directory to your Minix partition. `build.sh` should work also
on Minix.

Minix is not SMP, but the VM you're running it in can also jump between cores.
Solution: run the VM also using `taskset -c 0`.

Tested with `QEMU`.

`plot.py` obviously won't work on Minix, unless you port Python to it. You have
to copy the resulting files (data/p\*.log) back to a Linux machine (or anything
that supports Python).
