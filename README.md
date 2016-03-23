About
-----

This is a generic Linux kernel driver for the Silead GSLx68y
series of touch screen controllers.
It is currently designed to work on ACPI platforms, but
support for DeviceTree/OpenFirmware is also in the works.

The code was adapted from the platform specific driver here:
https://github.com/jabjoe/sunxi-gslx680

Kernel-based finger tracking is available and can be enabled if
the hardware doesn't support it. It works reasonably well,
but touches close to the edges are not registered reliably,
and dragging is very inaccurate.


Firmware Instructions
---------------------

The controller requires firmware to work properly. Firmware
images extracted from vendor drivers are maintained in a separate
repository: https://github.com/onitake/gsl-firmware

If your device is not mentioned yet, or the required silead_ts.fw
is not available, please post a request in the issue tracker there,
or consult [gsl-firmware/README.md](https://github.com/onitake/gsl-firmware/blob/master/README.md)
for information on how to obtain the firmware yourself.


Build Instructions
------------------

If you don't need to cross compile, just make sure you have headers
for your running Linux kernel installed, then type

    make

This will produce gslx680_ts_acpi.ko

If you need to cross compile, pass appropriate KSRC, ARCH and
CROSS_COMPILE variables to the make command. For example:

    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- KSRC=../linux-arm

CROSS_COMPILE is the compiler prefix (i.e. gcc will become
arm-linux-gnueabihf-gcc with CROSS_COMPILE=arm-linux-gnueabihf-), ARCH
is the target architecture as understood by the kernel (note: use i386
for 32 bit Intel platforms) and KSRC is the path to the target
kernel sources or kernel headers.


Install Instructions
--------------------

Install appropriate firmware for your device, as per the Firmware
Instructions above.

Load and test the driver with

    insmod ./gslx680_ts_acpi.ko

Running dmesg should produce some output if the device was matched
by the driver. You should also see a message from the input
subsystem that a new input device was added.

You may then observe the output from evtest. X.org touchscreen input
should work too, but you will notice that the touch points are
off if the panel width and height were not set accurately.

This can be fixed by installing xinput_calibrator and using it to
generate a configuration file for your touchscreen. Some desktop
environments may offer their own touchscreen calibrator,
which you can also use.

xinput_calibrator, when run from an X terminal,  will present a
series of points on the screen. Touch each of them when prompted,
then save the configuration printed to the terminal to the
indicated location.

After restarting X, you should have a working touchscreen.
