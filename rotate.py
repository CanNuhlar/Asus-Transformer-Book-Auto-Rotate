#!/usr/bin/env python3

import time
import threading
import socket
from subprocess import call

is_flipped = False
auto_rotate_on = True
current_rotation = "normal"
fetch_interval = 3

class lid_acpi_message_listener(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global is_flipped, current_rotation
		print("Started acpi listener.")
		while True:
			s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			s.connect('/var/run/acpid.socket')
			acpi_message = s.recv(4096).hex()
			if(acpi_message == "2030423343424233352d453343322d3435ff2030303030303066662030303030303030300a"):
				print("Lid flip!")
				is_flipped = not is_flipped
				if current_rotation != "normal":
					print("Exiting tablet mode.")
					call(["xrandr", "-o", "normal"])
				

class auto_rotate_screen(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global is_flipped, current_rotation
		print("Started orientation listener.")
		while True:
			if is_flipped and auto_rotate_on:
				print("Tablet mode ", is_flipped)
				#read x axis
				with open('/sys/bus/iio/devices/iio:device0/in_accel_x_raw') as fp:
					accel_x = int(fp.readline())
					fp.close()
				#read y axis
				with open('/sys/bus/iio/devices/iio:device0/in_accel_y_raw') as fp:
					accel_y = int(fp.readline())
					fp.close()
				#read z axis
				with open('/sys/bus/iio/devices/iio:device0/in_accel_z_raw') as fp:
					accel_z = int(fp.readline())
					fp.close()

				print("X axis raw accelerometer value ", accel_x)
				print("Y axis raw accelerometer value ", accel_y)
				print("Z axis raw accelerometer value ", accel_z)

				if(accel_y > abs(accel_x) and current_rotation != "right"):
					print("Device rotated left, setting xrandr orientation right.")
					current_rotation = "right"
					call(["xrandr", "-o", "right"])
				elif(accel_y < 0 and abs(accel_y) > accel_x and current_rotation != "left"):
					print("Device rotated right, setting xrandr orientation left.")
					current_rotation = "left"
					call(["xrandr", "-o", "left"])
				elif(accel_x > abs(accel_y) and current_rotation != "normal"):
					print("Device in normal position, setting orientation normal")
					current_rotation = "normal"
					call(["xrandr", "-o", "normal"])
				elif(abs(accel_x) > accel_z and accel_y > 0 and current_rotation != "inverted"):
					print("Device in inverted position, setting orientation inverted")
					current_rotation = "inverted"
					call(["xrandr", "-o", "inverted"])

				time.sleep(fetch_interval)


if __name__ == "__main__":
	lid_listener = lid_acpi_message_listener()
	lid_listener.daemon = True

	lid_listener.start()
	#lid_listener.join()

	auto_rotate = auto_rotate_screen()
	auto_rotate.daemon = True

	auto_rotate.start()
	auto_rotate.join()
