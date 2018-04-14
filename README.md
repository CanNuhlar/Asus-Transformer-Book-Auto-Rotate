# Auto Rotate Script For Asus Transformer Books And Derivatives

This is a python script that runs on background and rotates your screen based on orientation via using your devices acceloremeter data. Therotically it should work on all Asus Transformer Books, Asus Flip Books and derivatives which has Invensense G-Sensor.

# Installation & Usage

It depends on iio-sensor-proxy package.
Installation on ubuntu:

    apt-get install iio-sensor-proxy

On Arch:

    pacman -S iio-sensor-proxy

On Debian:

    dnf install iio-sensor-proxy

Clone the repo or download as zip. Make py file executable 

    chmod +x rotate
   
Run manually or set it up as a startup program. Auto rotation of X server will be enabled when you flip your lid (a.k.a. enable tablet mode) 

# TODO

 - Make a GTK Applet version
 - Better orientation detection
 - Use distutils to make script installable

