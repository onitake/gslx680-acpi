About
=====

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
=====================

The device requires firmware/configuration data to work.
Example firmware for some devices is included.

You may either extract the firmware from an Android or Windows
driver for this panel or use one of the supplied images.

The Android driver can be found under this path (or similar):
/system/vendor/modules/gslx680.ko
Copy this to a SD card or use a GNU/Linux chroot to scp it over, or use
adb pull.
On your build machine, on the command line, use the script
'firmware/fw_extractor' to extract the firmware to its own file.

    ./firmware/fw_extractor my_android_gslx680.ko my_tablets.fw

The Android driver may well contain multiple firmwares to support
different hardware configurations with the same driver. The extractor
will spit those out as seperate files. We currently have no way of
knowing which is right for your device. You will have to try each.

If you have a Windows driver instead, the firmware either comes in
the form of a file named TS_CFG.h or SileadTouch.fw. The latter
is just a scrambled version of TS_CFG.h and can be easily
converted by XORing every byte with 0x88.

Any of these three firmware formats must be converted into the
compact format supported by gslx680-acpi. Use ./firmware/fwtool
to handle this job. It also sets some non-generic device
parameters, such as panel width and height, tracking support, etc.

The file format is described in 'firmware/Firmware/Silead.pm'.
Use perldoc or a text editor to read.

Example usage:

    ./fwtool -c gslxxxx.fw -m 1680 -w 940 -h 750 -t 10 -f track silead_ts.fw

This will read legacy gslxxxx.fw, convert it into silead_ts.fw in
the new format, then set the controller type to GSL1680, the panel
width to 940 dots, the height to 750 dots, the maximum number
of touch points to 10 and enable software finger tracking.

To convert the scrambled SileadTouch.fw from a Windows driver:

    ./fwtool -c SileadTouch.fw -3 -m 1680 -w 940 -h 750 -t 10 silead_ts.fw

And for an unscrambled TS_CFG.h:

    ./fwtool -c TS_CFG.h -2 -m 1680 -w 940 -h 750 -t 10 silead_ts.fw

You might still need to calibrate the touchscreen later, if
the numbers are unknown or not accurate. Note that the maximum
width and height are 4095. The driver is currently hardcoded
to a touch point limit of 10 fingers, so specifying more than
that will not work.

The resulting firmware should be named silead_ts.fw and
installed into /lib/firmware so the driver can find it.

To convert a firmware image back into legacy format, use:

    ./fwtool -x gslxxxx.fw silead_ts.fw

Note that memory page order is not preserved. This should not
pose a problem for the controller, however.


Build Instructions
==================

If you don't need to cross compile, just make sure you have headers
for your running Linux kernel installed, then type

    make

This will produce gslx680_ts_acpi.ko

If you need to cross compile, pass appropriate KDIR, ARCH and
CROSS_COMPILE variables to the make command. For example:

    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- KDIR=../linux-arm


Install Instructions
====================

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

This can be fixed by installing xinput_calibrate and using it to
generate a configuration file for your touchscreen. Some desktop
environments may offer their own touchscreen calibrator,
which you can also use.

xinput_calbrator, when run from an X terminal,  will present a
series of points on the screen. Touch each of them when prompted,
then save the configuration printed to the terminal to the
indicated location.

After restarting X, you should have a working touchscreen.
