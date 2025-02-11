#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This code was modified by D. Juers and S. Stothers from Whitman College over 2021-25:
#	- add gradient flow capabilities
#		- linear gradient
#		- equal volume injections
#	- change available units 
#	- add move to zero and move to max volume, with maximum speed
#	- add take photos after each injection in auto run
#	- add monitoring of stepper motor moves, updating display of positions in real time
# 	- add Tool Tips on various widgets for context-enriched help
#	- add help screen with basic directions
#	- establish a default acceleration near the maximum, with user-selected accelerations as an option. This essentially makes the moves constant speed by default.
#	- add a mixing option during gradient runs, where the solution is mixed in the injection tube before injecting into the reservoir
#	
#  
import serial
import time
import glob
import sys
from datetime import datetime
import time
import os
# This gets the Qt stuff

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

import cv2
# note, had to use version 3.2.0.8 otherwise it had its own
# pyqt packages that conflicted with mine

import numpy as np
from decimal import Decimal
# This is our window from QtCreator
import poseidon_controller_gf_gui
import pdb
import traceback, sys

# ##############################
# MULTITHREADING : SIGNALS CLASS
# ##############################
class WorkerSignals(QtCore.QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    '''
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(int)
###
###
###
# class Worker(QtCore.QObject):
# 	progress = QtCore.pyqtSignal(int)
# 	completed = QtCore.pyqtSignal(int)
# 
# 	@Slot(int)
# 	def do_work(self,n):
# 		for i in range (1, n+1):
# 			time.sleep(1)
# 			self.progress.emit(i)
# 			
# 		self.completed.emit(i)
	

# #############################
# MULTITHREADING : WORKER CLASS
# #############################
class WorkerThread(QtCore.QThread):
	progress_updated = QtCore.pyqtSignal(int)
	
	def run(self):
		for i in range (10):
			print (i)
			time.sleep(0.1)
			self.progress_updated.emit(i)
		

class Thread(QtCore.QThread):
	def __init__(self, fn, *args, **kwargs):
		parent = None
		super(Thread, self).__init__(parent)
		self.runs = True
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
		self.signals = WorkerSignals()

	def run(self):
		try:
			#self.serial.flushInput()
			#self.serial.flushOutput()
			result = self.fn(*self.args, **self.kwargs)
		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
		else:
			self.signals.result.emit(result)  # Return the result of the processing
		finally:
			self.signals.finished.emit()  # Done
			self.stop()

			print("Job completed")

	def stop(self):
		self.runs = False




# #####################################
# ERROR HANDLING : CANNOT CONNECT CLASS
# #####################################
class CannotConnectException(Exception):
	pass

# #######################
# GUI : MAIN WINDOW CLASS
# #######################
class MainWindow(QtWidgets.QMainWindow, poseidon_controller_gf_gui.Ui_MainWindow):

	# =======================================================
	# INITIALIZING : The UI and setting some needed variables
	# =======================================================
	def __init__(self):

		# Setting the UI to a class variable and connecting all GUI Components
		super(MainWindow, self).__init__()
		self.ui = poseidon_controller_gf_gui.Ui_MainWindow()
		self.ui.setupUi(self)
		
		# Default acceleration (in steps/s/s). This essentially will default to constant speed. 
		# The maximum accelerations of steppers appears to be a few thousand steps/s/s.
		self.user_accelerations = False
		self.default_accel = 4000.0

		# Put comments here
		self.populate_microstepping()
		self.populate_syringe_sizes()
		self.populate_pump_jog_delta()
		self.populate_pump_units()
		self.setting_variables()
		self.populate_ports()
		self.set_port()
#		self.set_p1_accel()



		self.connect_all_gui_components()
		self.grey_out_components()
		self.grey_out_accelerations()

		# Declaring start, mid, and end marker for sending code to Arduino
		self.startMarker = 60# <
		self.endMarker = 62  # ,F,0.0>
		self.midMarker = 44 # ,

		# Initializing multithreading to allow parallel operations
		self.threadpool = QtCore.QThreadPool()
		print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())


		# Camera setup
		self.timer = QtCore.QTimer()
		self.timer.setInterval(1000)
		self.timer.timeout.connect(self.recurring_timer)
		self.timer.start()
		self.counter = 0

		# Random other things I need
		self.image = None
		self.speed_for_resetting=1000 #Use ~maximum speed for resetting the syring position
		self.update_displays()
		#self.microstepping = 1
		#print(self.microstepping)
        
        #Set initial state
#		self.connect() #Connect to arduino
#		self.start_camera() # Connect to camera
#		self.send_all()
		self.update_displays()

	def recurring_timer(self):
		self.counter +=1

	# =============================
	# SETTING : important variables
	# =============================
	def setting_variables(self):

		self.set_p1_syringe()
		self.set_p2_syringe()
		self.set_p3_syringe()



		#self.set_p1_units()
		#self.set_p2_units()
		#self.set_p3_units()

		self.is_p1_active = False
		self.is_p2_active = False
		self.is_p3_active = False

		self.is_premix_active = False
		self.is_photos_active = False

		self.experiment_notes = ""
		
		# Auto
		
		self.set_auto_variables()

	def thread_finished(self, th):
		print("Your thread has completed. Now terminating..")
		th.stop()
		print("Thread has been terminated.")
		print("=============================\n\n")
		# here is where you need to end the thread


	# ===================================
	# CONNECTING : all the GUI Components
	# ===================================
	def connect_all_gui_components(self):

		# ~~~~~~~~~~~~~~~
		# MAIN : MENU BAR
		# ~~~~~~~~~~~~~~~
		self.ui.load_settings_BTN.triggered.connect(self.load_settings)
		self.ui.save_settings_BTN.triggered.connect(self.save_settings)

		# ~~~~~~~~~~~~~~~~
		# TAB : Controller
		# ~~~~~~~~~~~~~~~~

		# Px active checkboxes
		self.ui.p1_activate_CHECKBOX.stateChanged.connect(self.toggle_p1_activation)
		self.ui.p2_activate_CHECKBOX.stateChanged.connect(self.toggle_p2_activation)
		self.ui.p3_activate_CHECKBOX.stateChanged.connect(self.toggle_p3_activation)

		self.ui.photos_CHECKBOX.stateChanged.connect(self.toggle_photos)
		self.ui.premix_CHECKBOX.stateChanged.connect(self.toggle_premix)

		# Px display (TODO)

		# Px syringe display
		self.ui.p1_syringe_DROPDOWN.currentIndexChanged.connect(self.display_p1_syringe)
		self.ui.p2_syringe_DROPDOWN.currentIndexChanged.connect(self.display_p2_syringe)
		self.ui.p3_syringe_DROPDOWN.currentIndexChanged.connect(self.display_p3_syringe)


		# Px speed display
		self.ui.p1_units_DROPDOWN.currentIndexChanged.connect(self.display_p1_speed)
		self.ui.p2_units_DROPDOWN.currentIndexChanged.connect(self.display_p2_speed)
		self.ui.p3_units_DROPDOWN.currentIndexChanged.connect(self.display_p3_speed)

		self.ui.accel_CHECKBOX.stateChanged.connect(self.toggle_user_accelerations)


		#self.populate_pump_units()

		# Px amount
		self.ui.p1_amount_INPUT.valueChanged.connect(self.set_p1_amount)
		self.ui.p2_amount_INPUT.valueChanged.connect(self.set_p2_amount)
		self.ui.p3_amount_INPUT.valueChanged.connect(self.set_p3_amount)

		# Px jog delta
		#self.ui.p1_jog_delta_INPUT.valueChanged.connect(self.set_p1_jog_delta)
		#self.ui.p2_jog_delta_INPUT.valueChanged.connect(self.set_p2_jog_delta)
		#self.ui.p3_jog_delta_INPUT.valueChanged.connect(self.set_p3_jog_delta)

		# Action buttons
		self.ui.run_BTN.clicked.connect(self.run)


		self.ui.pause_BTN.clicked.connect(self.pause)


		self.ui.setzero_BTN.clicked.connect(self.zero)
		self.ui.mv2zero_BTN.clicked.connect(self.mv2zero)
		self.ui.mv2maxvol_BTN.clicked.connect(self.mv2maxvol)
		self.ui.stop_BTN.clicked.connect(self.stop)


		self.ui.jog_plus_BTN.clicked.connect(lambda:self.jog(self.ui.jog_plus_BTN))
		self.ui.jog_minus_BTN.clicked.connect(lambda:self.jog(self.ui.jog_minus_BTN))

		# Set coordinate system
#		self.ui.absolute_RADIO.toggled.connect(lambda:self.set_coordinate(self.ui.absolute_RADIO))
#		self.ui.incremental_RADIO.toggled.connect(lambda:self.set_coordinate(self.ui.incremental_RADIO))
        
        # Auto
		self.ui.auto_tabs.currentChanged.connect(self.auto_display_time)
		
		self.ui.auto_volume_INPUT.valueChanged.connect(self.set_auto_volume)
		self.ui.auto_inject_number_INPUT.valueChanged.connect(self.set_auto_injection_number)
		self.ui.auto_latent_time_INPUT.valueChanged.connect(self.set_auto_latent_time)
		
		self.ui.auto_pinject_DROPDOWN.currentIndexChanged.connect(self.set_auto_pinject)
		self.ui.auto_pextract_DROPDOWN.currentIndexChanged.connect(self.set_auto_pextract)
		
		self.ui.autorun_BTN.clicked.connect(self.auto_run)
		self.ui.autorun_stop_BTN.clicked.connect(self.auto_stop)
		
		self.ui.p1_units_DROPDOWN.currentIndexChanged.connect(self.set_auto_units)
		self.ui.p2_units_DROPDOWN.currentIndexChanged.connect(self.set_auto_units)
		self.ui.p3_units_DROPDOWN.currentIndexChanged.connect(self.set_auto_units)
		
		self.ui.latent_time_units_DROPDOWN.currentIndexChanged.connect(self.set_latent_time_units)
		
		# Linear
		self.ui.linear_initial_concentration_INPUT.valueChanged.connect(self.set_linear_initial_concentration)
		self.ui.linear_syringe_concentration_INPUT.valueChanged.connect(self.set_linear_syringe_concentration)
		self.ui.linear_target_concentration_INPUT.valueChanged.connect(self.set_linear_target_concentration)
		#self.ui.linear_latent_time_INPUT.valueChanged.connect(self.set_linear_latent_time)
		
		'''self.ui.linear_pinject_DROPDOWN.currentIndexChanged.connect(self.set_linear_pinject)
		self.ui.linear_pextract_DROPDOWN.currentIndexChanged.connect(self.set_linear_pextract)'''
		
		self.ui.linearrun_BTN.clicked.connect(self.linear_run)
		self.ui.linearrun_stop_BTN.clicked.connect(self.linear_stop)
		
		
		
		self.ui.p1_syringe_DROPDOWN.currentIndexChanged.connect(self.set_linear_syringe)
		self.ui.p2_syringe_DROPDOWN.currentIndexChanged.connect(self.set_linear_syringe)
		self.ui.p3_syringe_DROPDOWN.currentIndexChanged.connect(self.set_linear_syringe)
		
		self.ui.p1_units_DROPDOWN.currentIndexChanged.connect(self.set_linear_units)
		self.ui.p2_units_DROPDOWN.currentIndexChanged.connect(self.set_linear_units)
		self.ui.p3_units_DROPDOWN.currentIndexChanged.connect(self.set_linear_units)
		
		self.ui.linear_solution_volume_INPUT.valueChanged.connect(self.set_linear_solution_volume)
		self.ui.linear_concentration_slope_INPUT.valueChanged.connect(self.set_linear_concentration_slope)
		self.ui.linear_duty_ratio_INPUT.valueChanged.connect(self.set_linear_duty_ratio)
		#self.ui.linear_concentration_units_DROPDOWN.currentIndexChanged.connect(self.linear_concentration_units_display)
		

		# ~~~~~~~~~~~~
		# TAB : Camera
		# ~~~~~~~~~~~~

		# Setting camera action buttons
		self.ui.camera_connect_BTN.clicked.connect(self.start_camera)
		self.ui.camera_disconnect_BTN.clicked.connect(self.stop_camera)
		self.ui.camera_capture_image_BTN.clicked.connect(self.save_image)

		# ~~~~~~~~~~~
		# TAB : Setup
		# ~~~~~~~~~~~

		# Port, first populate it then connect it (population done earlier)
		self.ui.refresh_ports_BTN.clicked.connect(self.refresh_ports)
		self.ui.port_DROPDOWN.currentIndexChanged.connect(self.set_port)

		self.ui.experiment_notes.editingFinished.connect(self.set_experiment_notes)

		# Set the microstepping value, default is 1
		self.ui.microstepping_DROPDOWN.currentIndexChanged.connect(self.set_microstepping)

		# Set the log file name
		self.date_string =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.date_string = self.date_string.replace(":","_") # Replace semicolons with underscores

		# Px syringe size, populate then connect (population done earlier)
		self.ui.p1_syringe_DROPDOWN.currentIndexChanged.connect(self.set_p1_syringe)
		self.ui.p2_syringe_DROPDOWN.currentIndexChanged.connect(self.set_p2_syringe)
		self.ui.p3_syringe_DROPDOWN.currentIndexChanged.connect(self.set_p3_syringe)
		
		self.ui.p1_syringe_DROPDOWN.currentIndexChanged.connect(self.set_auto_syringe)
		self.ui.p2_syringe_DROPDOWN.currentIndexChanged.connect(self.set_auto_syringe)
		self.ui.p3_syringe_DROPDOWN.currentIndexChanged.connect(self.set_auto_syringe)

		self.ui.p1_syringe_DROPDOWN.currentIndexChanged.connect(self.update_displays)
		self.ui.p2_syringe_DROPDOWN.currentIndexChanged.connect(self.update_displays)
		self.ui.p3_syringe_DROPDOWN.currentIndexChanged.connect(self.update_displays)

		# warning to send the info to the controller
		self.ui.p1_syringe_DROPDOWN.currentIndexChanged.connect(self.send_p1_warning)
		self.ui.p2_syringe_DROPDOWN.currentIndexChanged.connect(self.send_p2_warning)
		self.ui.p3_syringe_DROPDOWN.currentIndexChanged.connect(self.send_p3_warning)

		# Px units
		self.ui.p1_units_DROPDOWN.currentIndexChanged.connect(self.set_p1_units)
		self.ui.p2_units_DROPDOWN.currentIndexChanged.connect(self.set_p2_units)
		self.ui.p3_units_DROPDOWN.currentIndexChanged.connect(self.set_p3_units)

		self.ui.p1_units_DROPDOWN.currentIndexChanged.connect(self.update_displays)
		self.ui.p2_units_DROPDOWN.currentIndexChanged.connect(self.update_displays)
		self.ui.p3_units_DROPDOWN.currentIndexChanged.connect(self.update_displays)
		# warning to send the info to the controller
		self.ui.p1_units_DROPDOWN.currentIndexChanged.connect(self.send_p1_warning)
		self.ui.p2_units_DROPDOWN.currentIndexChanged.connect(self.send_p2_warning)
		self.ui.p3_units_DROPDOWN.currentIndexChanged.connect(self.send_p3_warning)

		# Px speed
		self.ui.p1_speed_INPUT.valueChanged.connect(self.set_p1_speed)
		self.ui.p2_speed_INPUT.valueChanged.connect(self.set_p2_speed)
		self.ui.p3_speed_INPUT.valueChanged.connect(self.set_p3_speed)
		
		self.ui.p1_speed_INPUT.valueChanged.connect(self.set_auto_speed_and_accel)
		self.ui.p2_speed_INPUT.valueChanged.connect(self.set_auto_speed_and_accel)
		self.ui.p3_speed_INPUT.valueChanged.connect(self.set_auto_speed_and_accel)
		# warning to send the info to the controller
		self.ui.p1_speed_INPUT.valueChanged.connect(self.send_p1_warning)
		self.ui.p2_speed_INPUT.valueChanged.connect(self.send_p2_warning)
		self.ui.p3_speed_INPUT.valueChanged.connect(self.send_p3_warning)

		# Px accel
		self.ui.p1_accel_INPUT.valueChanged.connect(self.set_p1_accel)
		self.ui.p2_accel_INPUT.valueChanged.connect(self.set_p2_accel)
		self.ui.p3_accel_INPUT.valueChanged.connect(self.set_p3_accel)
		
		self.ui.p1_accel_INPUT.valueChanged.connect(self.set_auto_speed_and_accel)
		self.ui.p2_accel_INPUT.valueChanged.connect(self.set_auto_speed_and_accel)
		self.ui.p3_accel_INPUT.valueChanged.connect(self.set_auto_speed_and_accel)
		# warning to send the info to the controller
		self.ui.p1_accel_INPUT.valueChanged.connect(self.send_p1_warning)
		self.ui.p2_accel_INPUT.valueChanged.connect(self.send_p2_warning)
		self.ui.p3_accel_INPUT.valueChanged.connect(self.send_p3_warning)

		# Px jog delta (setup)
		self.ui.p1_setup_jog_delta_INPUT.currentIndexChanged.connect(self.set_p1_setup_jog_delta)
		self.ui.p2_setup_jog_delta_INPUT.currentIndexChanged.connect(self.set_p2_setup_jog_delta)
		self.ui.p3_setup_jog_delta_INPUT.currentIndexChanged.connect(self.set_p3_setup_jog_delta)
		# warning to send the info to the contorller
		self.ui.p1_setup_jog_delta_INPUT.currentIndexChanged.connect(self.send_p1_warning)
		self.ui.p2_setup_jog_delta_INPUT.currentIndexChanged.connect(self.send_p2_warning)
		self.ui.p3_setup_jog_delta_INPUT.currentIndexChanged.connect(self.send_p3_warning)


		# Px send settings
		self.ui.p1_setup_send_BTN.clicked.connect(self.send_p1_settings)
		self.ui.p2_setup_send_BTN.clicked.connect(self.send_p2_settings)
		self.ui.p3_setup_send_BTN.clicked.connect(self.send_p3_settings)
		# remove warning to send settings
		self.ui.p1_setup_send_BTN.clicked.connect(self.send_p1_success)
		self.ui.p2_setup_send_BTN.clicked.connect(self.send_p2_success)
		self.ui.p3_setup_send_BTN.clicked.connect(self.send_p3_success)

		# Connect to arduino
		self.ui.connect_BTN.clicked.connect(self.connect)
		self.ui.disconnect_BTN.clicked.connect(self.disconnect)

		# Send all the settings at once
		self.ui.send_all_BTN.clicked.connect(self.send_all)

	def send_p1_warning(self):
		self.ui.p1_setup_send_BTN.setStyleSheet("background-color: green; color: black")

	def send_p2_warning(self):
		self.ui.p2_setup_send_BTN.setStyleSheet("background-color: green; color: black")

	def send_p3_warning(self):
		self.ui.p3_setup_send_BTN.setStyleSheet("background-color: green; color: black")

	def send_p1_success(self):
		self.ui.p1_setup_send_BTN.setStyleSheet("background-color: none")

	def send_p2_success(self):
		self.ui.p2_setup_send_BTN.setStyleSheet("background-color: none")

	def send_p3_success(self):
		self.ui.p3_setup_send_BTN.setStyleSheet("background-color: none")

	def grey_out_components(self):
		# ~~~~~~~~~~~~~~~~
		# TAB : Controller
		# ~~~~~~~~~~~~~~~~
		self.ui.run_BTN.setEnabled(False)
		self.ui.pause_BTN.setEnabled(False)
		self.ui.setzero_BTN.setEnabled(False)
		self.ui.mv2zero_BTN.setEnabled(False)
		self.ui.mv2maxvol_BTN.setEnabled(False)
		self.ui.stop_BTN.setEnabled(False)
		self.ui.jog_plus_BTN.setEnabled(False)
		self.ui.jog_minus_BTN.setEnabled(False)
		self.ui.autorun_BTN.setEnabled(False)
		self.ui.autorun_stop_BTN.setEnabled(False)

		# ~~~~~~~~~~~~~~~~
		# TAB : Setup
		# ~~~~~~~~~~~~~~~~
		self.ui.p1_setup_send_BTN.setEnabled(False)
		self.ui.p2_setup_send_BTN.setEnabled(False)
		self.ui.p3_setup_send_BTN.setEnabled(False)
		self.ui.send_all_BTN.setEnabled(False)

	def ungrey_out_components(self):
		# ~~~~~~~~~~~~~~~~
		# TAB : Controller
		# ~~~~~~~~~~~~~~~~
		self.ui.run_BTN.setEnabled(True)
		self.ui.pause_BTN.setEnabled(True)
		self.ui.setzero_BTN.setEnabled(True)
		self.ui.mv2zero_BTN.setEnabled(True)
		self.ui.mv2maxvol_BTN.setEnabled(True)
		self.ui.stop_BTN.setEnabled(True)
		self.ui.jog_plus_BTN.setEnabled(True)
		self.ui.jog_minus_BTN.setEnabled(True)
		self.ui.autorun_BTN.setEnabled(True)
		self.ui.autorun_stop_BTN.setEnabled(True)
		
		self.ui.run_BTN.setStyleSheet("background-color: green; color: black")
		self.ui.pause_BTN.setStyleSheet("background-color: yellow; color: black")
		self.ui.stop_BTN.setStyleSheet("background-color: red; color: black")

		# ~~~~~~~~~~~~~~~~
		# TAB : Setup
		# ~~~~~~~~~~~~~~~~
		self.ui.p1_setup_send_BTN.setEnabled(True)
		self.ui.p2_setup_send_BTN.setEnabled(True)
		self.ui.p3_setup_send_BTN.setEnabled(True)
		self.ui.send_all_BTN.setEnabled(True)
		
	def grey_out_accelerations(self):
		self.ui.p1_accel_INPUT.setEnabled(False)		
		self.ui.p1_accel_INPUT.setDisabled(True)		
		self.ui.p2_accel_INPUT.setEnabled(False)		
		self.ui.p2_accel_INPUT.setDisabled(True)		
		self.ui.p3_accel_INPUT.setEnabled(False)		
		self.ui.p3_accel_INPUT.setDisabled(True)		

	def ungrey_out_accelerations(self):
		self.ui.p1_accel_INPUT.setEnabled(True)		
		self.ui.p1_accel_INPUT.setDisabled(False)		
		self.ui.p2_accel_INPUT.setEnabled(True)		
		self.ui.p2_accel_INPUT.setDisabled(False)		
		self.ui.p3_accel_INPUT.setEnabled(True)		
		self.ui.p3_accel_INPUT.setDisabled(False)		

	# ======================
	# FUNCTIONS : Controller
	# ======================

	def toggle_p1_activation(self):
		if self.ui.p1_activate_CHECKBOX.isChecked():
			self.is_p1_active = True
		else:
			self.is_p1_active = False

	def toggle_p2_activation(self):
		if self.ui.p2_activate_CHECKBOX.isChecked():
			self.is_p2_active = True
		else:
			self.is_p2_active = False

	def toggle_p3_activation(self):
		if self.ui.p3_activate_CHECKBOX.isChecked():
			self.is_p3_active = True
		else:
			self.is_p3_active = False

	def toggle_user_accelerations(self):
		if self.ui.accel_CHECKBOX.isChecked():
			self.user_accelerations = True
			self.ungrey_out_accelerations()
			self.set_p1_accel()
			self.set_p2_accel()
			self.set_p3_accel()
		else:
			self.user_accelerations = False
			self.grey_out_accelerations()
			self.set_p1_accel()
			self.set_p2_accel()
			self.set_p3_accel()
			
			
	def toggle_premix(self):
		if self.ui.premix_CHECKBOX.isChecked():
			self.is_premix_active = True
		else:
			self.is_premix_active = False
		
	def toggle_photos(self):
		if self.ui.photos_CHECKBOX.isChecked():
			self.is_photos_active = True
		else:
			self.is_photos_active = False
		
	# Get a list of active pumps (IDK if this is the best way to do this)
	def get_active_pumps(self):
		pumps_list = [self.is_p1_active, self.is_p2_active, self.is_p3_active]
		active_pumps = [i+1 for i in range(len(pumps_list)) if pumps_list[i]]
		return active_pumps

	def display_p1_syringe(self):
		self.ui.p1_syringe_LABEL.setText(self.ui.p1_syringe_DROPDOWN.currentText())
	def display_p2_syringe(self):
		self.ui.p2_syringe_LABEL.setText(self.ui.p2_syringe_DROPDOWN.currentText())
	def display_p3_syringe(self):
		self.ui.p3_syringe_LABEL.setText(self.ui.p3_syringe_DROPDOWN.currentText())

	def display_p1_speed(self):
		self.ui.p1_units_LABEL.setText(str(self.p1_speed) + " " + self.ui.p1_units_DROPDOWN.currentText())
	def display_p2_speed(self):
		self.ui.p2_units_LABEL.setText(str(self.p2_speed) + " " + self.ui.p2_units_DROPDOWN.currentText())
	def display_p3_speed(self):
		self.ui.p3_units_LABEL.setText(str(self.p3_speed) + " " + self.ui.p3_units_DROPDOWN.currentText())

	# Set Px distance to move
	def set_p1_amount(self):
		self.p1_amount = self.ui.p1_amount_INPUT.value()
	def set_p2_amount(self):
		self.p2_amount = self.ui.p2_amount_INPUT.value()
	def set_p3_amount(self):
		self.p3_amount = self.ui.p3_amount_INPUT.value()

	# Set Px jog delta
	#def set_p1_jog_delta(self):
	#	self.p1_jog_delta = self.ui.p1_jog_delta_INPUT.value()
	#def set_p2_jog_delta(self):
	#	self.p2_jog_delta = self.ui.p2_jog_delta_INPUT.value()
	#def set_p3_jog_delta(self):
	#	self.p3_jog_delta = self.ui.p3_jog_delta_INPUT.value()

	# Set the coordinate system for the pump
	def set_coordinate(self, radio):
		if radio.text() == "Abs.":
			if radio.isChecked():
				self.coordinate = "absolute"
		if radio.text() == "Incr.":
			if radio.isChecked():
				self.coordinate = "incremental"
	#
	# Manual control 
	#

	def run(self):
		self.statusBar().showMessage("You clicked RUN")
		testData = []

		active_pumps = self.get_active_pumps()
		if len(active_pumps) > 0:
			
			p1_input_displacement = str(self.convert_displacement(self.p1_amount, self.p1_units, self.p1_syringe_area, self.microstepping))
			p2_input_displacement = str(self.convert_displacement(self.p2_amount, self.p2_units, self.p2_syringe_area, self.microstepping))
			p3_input_displacement = str(self.convert_displacement(self.p3_amount, self.p3_units, self.p3_syringe_area, self.microstepping))

			pumps_2_run = ''.join(map(str,active_pumps))

			cmd = "<RUN,DIST,"+pumps_2_run+",0.0,F," + p1_input_displacement + "," + p2_input_displacement + "," + p3_input_displacement + ">"

			testData.append(cmd)

			deltasteps=self.getSteps(testData[0])
			calib=np.loadtxt("calibration.txt")
			targetPos=calib[1,:]+deltasteps

			print("Sending RUN command..")
			thread = Thread(self.runTest, testData)
			thread.finished.connect(lambda:self.thread_finished(thread))
			thread.start()
			print("RUN command sent.")	
			self.update_target(cmd)
		
			time.sleep(0.1);
			
			direction=np.array([np.sign(float(p1_input_displacement)),np.sign(float(p2_input_displacement)),np.sign(float(p3_input_displacement))])
			threadm = Thread(self.monitorMoves,targetPos)
			threadm.finished.connect(lambda:self.thread_finished(threadm))
			threadm.start()			
			while not threadm.isFinished():
				QtWidgets.QApplication.processEvents()
				pass


		else:
			self.statusBar().showMessage("No pumps enabled.")

	# Clean up this text
	def pause(self):
		active_pumps = self.get_active_pumps()
		pumps_2_run = ''.join(map(str,active_pumps))

		if self.ui.pause_BTN.text() == "Pause":
			self.statusBar().showMessage("You clicked PAUSE")
			testData = []
			cmd = "<PAUSE,BLAH," + pumps_2_run + ",BLAH,F,0.0,0.0,0.0>"
			testData.append(cmd)

			print("Sending PAUSE command..")
			thread = Thread(self.runTest, testData)
			thread.finished.connect(lambda:self.thread_finished(thread))
			thread.start()
			print("PAUSE command sent.")

			self.ui.pause_BTN.setText("Resume")

		elif self.ui.pause_BTN.text() == "Resume":
			self.statusBar().showMessage("You clicked RESUME")
			testData = []
			cmd = "<RESUME,BLAH," + pumps_2_run + ",BLAH,F,0.0,0.0,0.0>"
			testData.append(cmd)

			print("Sending RESUME command..")
			thread = Thread(self.runTest, testData)
			thread.finished.connect(lambda:self.thread_finished(thread))
			thread.start()
			print("RESUME command sent.")

			self.ui.pause_BTN.setText("Pause")
	#####################################
	# Zeroing the syringe positions etc.#
	#####################################
	def zero(self):
		self.statusBar().showMessage("You clicked ZERO")
		testData = []

		cmd = "<ZERO,BLAH,BLAH,BLAH,F,0.0,0.0,0.0>"

		print("Sending ZERO command..")
		thread = Thread(self.runTest, testData)
		thread.finished.connect(lambda:self.thread_finished(thread))
		thread.start()
#		
		print("ZERO command sent.")
		calib=np.loadtxt("calibration.txt")
		print("Previous calibration:",calib)
		active_pumps = 1-np.array([self.is_p1_active, self.is_p2_active, self.is_p3_active])

		calib=np.array([active_pumps*calib[0,:],active_pumps*calib[1,:]])
		np.savetxt("calibration.txt",calib)
		print("Current calibration:",calib)
		self.update_displays()

	def mv2zero(self):
		self.statusBar().showMessage("You clicked mv2ZERO")
		testData = []
		active_pumps = self.get_active_pumps()
		if len(active_pumps) > 0:

			calib=np.loadtxt("calibration.txt")
			
			p1_input_displacement = str(calib[0,0]-calib[1,0])
			p2_input_displacement = str(calib[0,1]-calib[1,1])
			p3_input_displacement = str(calib[0,2]-calib[1,2])

			pumps_2_run = ''.join(map(str,active_pumps))
			# First adjust to max speed
			testData.append("<SETTING,SPEED,1,1000,F,0.0,0.0,0.0>")
			testData.append("<SETTING,SPEED,2,1000,F,0.0,0.0,0.0>")
			testData.append("<SETTING,SPEED,3,1000,F,0.0,0.0,0.0>")

			print("Ajusting speeds to maximum...")
			thread = Thread(self.runTest, testData)
			thread.finished.connect(lambda:self.thread_finished(thread))
			thread.start()
			print("Speeds adjusted.")
			time.sleep(0.1)
			
			testData = []
			

			cmd = "<RUN,DIST,"+pumps_2_run+",0.0,F," + p1_input_displacement + "," + p2_input_displacement + "," + p3_input_displacement + ">"

			testData.append(cmd)

			print("Sending RUN command..")
			thread = Thread(self.runTest, testData)
			thread.finished.connect(lambda:self.thread_finished(thread))
			thread.start()
			print("RUN command sent.")
			time.sleep(0.1)

			targetPos=self.update_target(cmd)		
			direction=np.array([np.sign(float(p1_input_displacement)),np.sign(float(p2_input_displacement)),np.sign(float(p3_input_displacement))])
			threadm = Thread(self.monitorMoves,targetPos)
			threadm.finished.connect(lambda:self.thread_finished(threadm))
			threadm.start()			
			while not threadm.isFinished():
				QtWidgets.QApplication.processEvents()
				pass
			
			self.send_all()
			
			
		else:
			self.statusBar().showMessage("No pumps enabled.")

		
	def mv2maxvol(self):
		self.statusBar().showMessage("You clicked mv2maxvol")
		testData = []
		active_pumps = self.get_active_pumps()
		if len(active_pumps) > 0:

			calib=np.loadtxt("calibration.txt")
			p1_max_displ = self.mL2steps(self.syringe_volumes[self.syringe_options.index(self.p1_syringe)],self.syringe_areas[self.syringe_options.index(self.p1_syringe)],self.microstepping)
			p2_max_displ = self.mL2steps(self.syringe_volumes[self.syringe_options.index(self.p1_syringe)],self.syringe_areas[self.syringe_options.index(self.p1_syringe)],self.microstepping)
			p3_max_displ = self.mL2steps(self.syringe_volumes[self.syringe_options.index(self.p1_syringe)],self.syringe_areas[self.syringe_options.index(self.p1_syringe)],self.microstepping)
			p1_input_displacement = str(p1_max_displ-calib[1,0])
			p2_input_displacement = str(p2_max_displ-calib[1,1])
			p3_input_displacement = str(p3_max_displ-calib[1,2])

			pumps_2_run = ''.join(map(str,active_pumps))
			# First adjust to max speed
			testData.append("<SETTING,SPEED,1,1000,F,0.0,0.0,0.0>")
			testData.append("<SETTING,SPEED,2,1000,F,0.0,0.0,0.0>")
			testData.append("<SETTING,SPEED,3,1000,F,0.0,0.0,0.0>")

			print("Ajusting speeds to maximum...")
			thread = Thread(self.runTest, testData)
			thread.finished.connect(lambda:self.thread_finished(thread))
			thread.start()
			print("Speeds adjusted.")
			time.sleep(0.1)

			cmd = "<RUN,DIST,"+pumps_2_run+",0.0,F," + p1_input_displacement + "," + p2_input_displacement + "," + p3_input_displacement + ">"
			
			testData=[]
			testData.append(cmd)

			print("Sending RUN command..")
			thread = Thread(self.runTest, testData)
			thread.finished.connect(lambda:self.thread_finished(thread))
			thread.start()
			print("RUN command sent.")
			time.sleep(0.1)

			targetPos=self.update_target(cmd)		
			direction=np.array([np.sign(float(p1_input_displacement)),np.sign(float(p2_input_displacement)),np.sign(float(p3_input_displacement))])
			threadm = Thread(self.monitorMoves,targetPos)
			threadm.finished.connect(lambda:self.thread_finished(threadm))
			threadm.start()			
			while not threadm.isFinished():
				QtWidgets.QApplication.processEvents()
				pass

			self.send_all()
			
		else:
			self.statusBar().showMessage("No pumps enabled.")

	def stop(self):
		self.statusBar().showMessage("You clicked STOP")
		cmd = "<STOP,BLAH,BLAH,BLAH,F,0.0,0.0,0.0>"

		print("Sending STOP command..")
		thread = Thread(self.send_single_command, cmd)
		thread.finished.connect(lambda:self.thread_finished(thread))
		thread.start()
		print("STOP command sent.")
		time.sleep(0.1)
		self.ui.p1_absolute_DISP.display(self.ui.p1_curr_DISP.value())
		self.ui.p2_absolute_DISP.display(self.ui.p2_curr_DISP.value())
		self.ui.p3_absolute_DISP.display(self.ui.p3_curr_DISP.value())
		p1steps=self.convert_displacement(self.ui.p1_curr_DISP.value(), self.p1_units, self.p1_syringe_area, self.microstepping)
		p2steps=self.convert_displacement(self.ui.p2_curr_DISP.value(), self.p2_units, self.p2_syringe_area, self.microstepping)
		p3steps=self.convert_displacement(self.ui.p3_curr_DISP.value(), self.p3_units, self.p3_syringe_area, self.microstepping)
		calib=np.loadtxt("calibration.txt")
		calib[1,:]=[p1steps,p2steps,p3steps]
		np.savetxt("calibration.txt",calib)


	def jog(self, btn):
		self.statusBar().showMessage("You clicked JOG")
		#self.serial.flushInput()
		testData = []
		active_pumps = self.get_active_pumps()
		if len(active_pumps) > 0:
			pumps_2_run = ''.join(map(str,active_pumps))

			one_jog = str(self.p1_setup_jog_delta_to_send)
			two_jog = str(self.p2_setup_jog_delta_to_send)
			three_jog = str(self.p3_setup_jog_delta_to_send)

			if btn.text() == "Jog +":
				self.statusBar().showMessage("You clicked JOG +")
				f_cmd = "<RUN,DIST," + pumps_2_run +",0,F," + one_jog + "," + two_jog + "," + three_jog + ">"
				testData.append(f_cmd)

				print("Sending JOG command..")

				thread = Thread(self.runTest, testData)
				thread.finished.connect(lambda:self.thread_finished(thread))
				thread.start()
				print("JOG command sent.")
				time.sleep(0.1)
				
				targetPos=self.update_target(f_cmd)
				direction=np.array([1,1,1])
				threadm = Thread(self.monitorMoves,targetPos)
				threadm.finished.connect(lambda:self.thread_finished(threadm))
				threadm.start()	
				time.sleep(0.1)		
				while not threadm.isFinished():
					QtWidgets.QApplication.processEvents()
					pass

			elif btn.text() == "Jog -":
				self.statusBar().showMessage("You clicked JOG -")
				b_cmd = "<RUN,DIST," + pumps_2_run +",0,B," + one_jog + "," + two_jog + "," + three_jog + ">"
				testData.append(b_cmd)

				print("Sending JOG command..")
				thread = Thread(self.runTest, testData)
				thread.finished.connect(lambda:self.thread_finished(thread))
				thread.start()
				print("JOG command sent.")
				time.sleep(0.1)
				
				targetPos=self.update_target(b_cmd)
				direction=np.array([1,1,1])
				threadm = Thread(self.monitorMoves,targetPos)
				threadm.finished.connect(lambda:self.thread_finished(threadm))
				threadm.start()	
				time.sleep(0.1)		
				while not threadm.isFinished():
					QtWidgets.QApplication.processEvents()
					pass

		else:
			self.statusBar().showMessage("No pumps enabled.")
     
	########################################            
    # Auto run routines (i.e. equal volume)#
    ########################################
	'''def auto_switch_tabs(self):
		pass'''
	
	def auto_display_time(self, *time_left):
		tab_index = self.ui.auto_tabs.currentIndex()
		if self.auto_counter != 0:
			self.ui.auto_time_left_LCD.display(self.auto_displayTime)
			self.ui.auto_time_passed_LCD.display(self.auto_time_counter)
		elif self.linear_counter != -1:
			self.ui.auto_time_left_LCD.display(self.linear_displayTime)
			self.ui.auto_time_passed_LCD.display(self.linear_time_counter)
		else:
			if tab_index == 0:
				self.ui.auto_time_left_LCD.display(self.auto_displayTime)
				self.ui.auto_time_passed_LCD.display(self.auto_time_counter)
			else:
				self.ui.auto_time_left_LCD.display(self.linear_displayTime)
				self.ui.auto_time_passed_LCD.display(self.linear_time_counter)
	
	def set_auto_volume(self):
		
		self.auto_volume = self.ui.auto_volume_INPUT.value()
		self.set_auto_total_time()
		#print("Auto Volume %f" % self.auto_volume)
		
	def set_auto_injection_number(self):

		self.auto_injection_number = self.ui.auto_inject_number_INPUT.value()
		
		#using -1 for the counter might be better when it is not running, see if there are problems with equal volume
		if self.auto_counter == 0 and self.linear_counter == -1:
			self.ui.auto_injection_left_LCD.display(self.auto_injection_number)
		#print("Auto Inject %d" % self.auto_injection_number)
		
		
		
		self.set_auto_latent_time()
		self.set_linear_total_time()
		#self.linear_display_initial_injection_size() total time does this
		
	def set_auto_latent_time(self):
		
		self.auto_latent_time = self.convert_time(self.ui.auto_latent_time_INPUT.value())
		self.set_auto_total_time()
		
	def set_auto_total_time(self):
		self.auto_find_inject_time()
		self.auto_total_time = (self.auto_latent_time + self.auto_inject_time) * (self.auto_injection_number - 1) + self.auto_inject_time
#		print(self.auto_latent_time, self.auto_inject_time)
		if self.auto_counter == 0:
			self.auto_displayTime = self.auto_total_time
			self.auto_display_time()
		
	def set_auto_pinject(self):

		self.p_auto_inject = self.ui.auto_pinject_DROPDOWN.currentText()
		
		self.set_auto_units()
		self.set_auto_syringe()
		self.set_auto_speed_and_accel()
		
		self.set_linear_units()
		self.set_linear_syringe()
#		self.set_linear_accel()
		
		
	def set_auto_pextract(self):

		self.p_auto_extract = self.ui.auto_pextract_DROPDOWN.currentText()
		
		self.set_auto_units()
		self.set_auto_syringe()
		self.set_auto_speed_and_accel()
		
		self.set_linear_units()
		self.set_linear_syringe()
#		self.set_linear_accel()
		
	def set_auto_units(self):
		
		p1 = self.ui.p1_units_DROPDOWN.currentText()
		p2 = self.ui.p2_units_DROPDOWN.currentText()
		p3 = self.ui.p3_units_DROPDOWN.currentText()
		pump_units = (p1,p2,p3)

		#since the units should be the same, there is no need to have two variables for this

		inject_units = pump_units[int(self.p_auto_inject) - 1]
		extract_units = pump_units[int(self.p_auto_extract) - 1]

		if inject_units != extract_units:
			self.p_auto_units = False
		else:
			self.p_auto_units = inject_units

		self.display_auto_units()
		self.set_auto_total_time()
			
	def set_auto_speed_and_accel(self):
		
		p1 = self.ui.p1_speed_INPUT.value()
		p2 = self.ui.p2_speed_INPUT.value()
		p3 = self.ui.p3_speed_INPUT.value()
		pump_speeds = (p1,p2,p3)

		inject_speed = pump_speeds[int(self.p_auto_inject) - 1]
		extract_speed = pump_speeds[int(self.p_auto_extract) - 1]

		if inject_speed != extract_speed:
			self.p_auto_speed = False
		else:
			self.p_auto_speed = inject_speed

		p1 = self.ui.p1_accel_INPUT.value()
		p2 = self.ui.p2_accel_INPUT.value()
		p3 = self.ui.p3_accel_INPUT.value()
		pump_accels = (p1,p2,p3)

		inject_accel = pump_accels[int(self.p_auto_inject) - 1]
		extract_accel = pump_accels[int(self.p_auto_extract) - 1]

		if inject_accel != extract_accel:
			self.p_auto_accel = False
		else:
			self.p_auto_accel = inject_accel

		self.set_auto_total_time()
	
	def display_auto_units(self):
		
		if isinstance(self.p_auto_units, str):
			auto_unit_text = self.p_auto_units.split("/")[0]
			self.ui.auto_injection_units_LABEL.setText(auto_unit_text)
		else:
			self.ui.auto_injection_units_LABEL.setText("???")
			
	def set_auto_syringe(self):
		p1 = self.ui.p1_syringe_DROPDOWN.currentText()
		p2 = self.ui.p2_syringe_DROPDOWN.currentText()
		p3 = self.ui.p3_syringe_DROPDOWN.currentText()
		pump_syringes = (p1,p2,p3)

		#p_auto_inject_syringe isn't a class variable because it isn't needed outside of the function at the moment

		inject_syringe = pump_syringes[int(self.p_auto_inject) - 1]
		extract_syringe = pump_syringes[int(self.p_auto_extract) - 1]

		if inject_syringe != extract_syringe:
			self.p_auto_syringe_area = False

		else:
			self.p_auto_syringe_area = self.syringe_areas[self.syringe_options.index(inject_syringe)]

		#self.p_auto_inject_syringe_area = self.syringe_areas[self.syringe_options.index(p_auto_inject_syringe)]
		#self.p_auto_extract_syringe_area = self.syringe_areas[self.syringe_options.index(p_auto_extract_syringe)]	
		self.set_auto_total_time()
	
	def set_latent_time_units(self):
		if self.auto_counter == 0:
			self.latent_time_units = self.ui.latent_time_units_DROPDOWN.currentText()
			self.set_auto_total_time()
		
	def auto_find_inject_time(self):
		
#		print(self.p_auto_units, self.p_auto_syringe_area, self.p_auto_speed, self.p_auto_accel)
		if self.p_auto_units and self.p_auto_syringe_area and self.p_auto_speed !=0 and self.p_auto_accel != 0:
			
			
			inject_displacement = self.convert_displacement(self.auto_volume, self.p_auto_units, self.p_auto_syringe_area, self.microstepping) #steps
			inject_speed = self.convert_speed(self.p_auto_speed, self.p_auto_units, self.p_auto_syringe_area, self.microstepping) #steps/s
			inject_accel = self.convert_speed(self.p_auto_speed, self.p_auto_units, self.p_auto_syringe_area, self.microstepping) #steps/(s^2)
			
			displacement_when_reach_vmax = (inject_speed ** 2) / (2 * inject_accel)
			
			if inject_displacement <= displacement_when_reach_vmax:
				self.auto_inject_time = ((2 * inject_displacement) / inject_accel) ** 0.5
			else:
				t1 = ((2 * displacement_when_reach_vmax) / inject_accel) ** 0.5
				displacement_after_reach_vmax = inject_displacement - displacement_when_reach_vmax
				t2 = displacement_after_reach_vmax / inject_speed
				self.auto_inject_time = t1 + t2
		else:
			self.auto_inject_time = 0

	def auto_run(self):
		'''print(self.p_auto_inject_syringe,self.p_auto_extract_syringe)
		print("\n####################################\n")
		print(self.p_auto_inject_syringe_area,self.p_auto_extract_syringe_area)
		print("\n####################################\n")
		print(self.p_auto_inject_speed,self.p_auto_extract_speed)
		print("\n####################################\n")
		print(self.p_auto_inject_accel,self.p_auto_extract_accel)'''
		
		self.statusBar().showMessage("You clicked Auto Run")
		
		#think about including support for different units from setup (split up unit funtions, put ui for displaying pump units)
		#maybe progress bar?
		
		#make it so auto_run button is disabled when a bunch of the critera aren't met
		#incorporate pause/stop ability
		#maybe split some functions (like speed accel)
		
		#apparently the condition of just a string or a float is interpreted as true
		
		
		active_and_different = (self.p_auto_inject != self.p_auto_extract)
		#same_units = isinstance(self.p_auto_units, str)
		#same_syringe_area = isinstance(self.p_auto_syringe_area, float)
		#same_speed_accel = isinstance(self.p_auto_speed, float) and isinstance(self.p_auto_accel, float)
		non_zero = (self.p_auto_speed != 0) and (self.p_auto_accel != 0) and self.auto_volume != 0 and self.auto_latent_time != 0
		
		#making sure inject time is up to date, might be unnessesary
		self.auto_find_inject_time()
		
		delay_long_enough = self.auto_latent_time >= self.auto_inject_time
							
		if (not active_and_different):
			self.statusBar().showMessage("Injection and extraction pumps must be enabled in 'Syringe Control' and be different.")
		elif (not self.p_auto_units):
			self.statusBar().showMessage("The two pumps must have the same units.")
		elif (not self.p_auto_syringe_area):
			self.statusBar().showMessage("The two pumps must have the same kind of syringe.")
		elif (not (self.p_auto_speed and self.p_auto_accel)):
			self.statusBar().showMessage("The two pumps must have the same acceleration and speed.")
		elif (not non_zero):
			self.statusBar().showMessage("Speeds, accelerations, injection volume, and latent time must all be non-zero.")
		elif (not delay_long_enough):
			self.statusBar().showMessage("The latent time needs to be longer than %fs with these settings." % self.auto_inject_time)
		else:
			
			activation_instructions = [False,False,False]
			
			activation_instructions[int(self.p_auto_inject) - 1] = True
			activation_instructions[int(self.p_auto_extract) - 1] = True
			
			self.ui.p1_activate_CHECKBOX.setChecked(activation_instructions[0])
			self.ui.p2_activate_CHECKBOX.setChecked(activation_instructions[1])
			self.ui.p3_activate_CHECKBOX.setChecked(activation_instructions[2])
			
			self.auto_counter = 0
			
			injection_n = self.auto_injection_number
			volume = self.auto_volume
			units = self.p_auto_units
			area = self.p_auto_syringe_area
			microstepping = self.microstepping
			inject = self.p_auto_inject
			extract = self.p_auto_extract
			total_time = self.auto_total_time
			
			self.auto_timer = QtCore.QTimer(self)
			
			#lambda is used so that if the UI is changed during a run it won't affect the variables
			
			self.auto_timer.timeout.connect(lambda:self.auto_update(injection_n, volume, units, area, microstepping, inject, extract))
			self.auto_time_timer = QtCore.QTimer(self)
			self.auto_time_timer.timeout.connect(lambda:self.auto_time_update(total_time))
			
			self.auto_update(injection_n, volume, units, area, microstepping, inject, extract)
			time_interval = self.auto_latent_time + self.auto_inject_time
			self.auto_timer.start(time_interval * 1000)
			
			self.auto_time_counter = 0

			self.auto_time_update(total_time)
			self.auto_time_timer.start(1000)
				
		
	
	def auto_update(self, injection_n, volume, units, area, microstepping, inject, extract):
		self.auto_counter += 1
		print("\n\nStarting AUTO RUN command #%d..." % (self.auto_counter))
		
		if self.auto_counter > injection_n:
			self.auto_update_stop()
			return
		
		testData = []
		active_pumps = self.get_active_pumps()
		pumps_2_run = ''.join(map(str,active_pumps))
		pump_instruction_list = ['0','0','0']

		
		if self.is_photos_active:
			self.save_image

		if self.is_premix_active:

			p_inject_displacement = str(self.convert_displacement(volume, units, area, microstepping))
			p_extract_displacement = str(self.convert_displacement(0, units, area, microstepping))

			pump_instruction_list[int(inject) - 1] = p_inject_displacement
			pump_instruction_list[int(extract) - 1] = p_extract_displacement

			cmd_reverse = "<RUN,DIST," + pumps_2_run + ",0,F,%s,%s,%s>" % tuple(pump_instruction_list)

			print("Executing reverse pipetting")
			
			testData = []			
			testData.append(cmd_reverse)
			thread = Thread(self.runTest, testData)
			thread.finished.connect(lambda:self.thread_finished(thread))
			thread.start()
			time.sleep(0.1)
			
			
			targetPos=self.update_target(cmd_reverse)
			direction=np.array([np.sign(float(pump_instruction_list[0])),np.sign(float(pump_instruction_list[1])),np.sign(float(pump_instruction_list[2]))])
			threadm = Thread(self.monitorMoves,targetPos)
			threadm.finished.connect(lambda:self.thread_finished(threadm))
			threadm.start()	
			time.sleep(0.1)		
			while not threadm.isFinished():
				QtWidgets.QApplication.processEvents()
				pass

			p_inject_displacement = str(self.convert_displacement(-2*volume, units, area, microstepping))
			p_extract_displacement = str(self.convert_displacement(volume, units, area, microstepping))

			pump_instruction_list[int(inject) - 1] = p_inject_displacement
			pump_instruction_list[int(extract) - 1] = p_extract_displacement

			cmd_forward = "<RUN,DIST," + pumps_2_run + ",0,F,%s,%s,%s>" % tuple(pump_instruction_list)



		else:
			p_inject_displacement = str(self.convert_displacement(-volume, units, area, microstepping))
			p_extract_displacement = str(self.convert_displacement(volume, units, area, microstepping))

			pump_instruction_list[int(inject) - 1] = p_inject_displacement
			pump_instruction_list[int(extract) - 1] = p_extract_displacement

			cmd_forward = "<RUN,DIST," + pumps_2_run + ",0,F,%s,%s,%s>" % tuple(pump_instruction_list)


		testData=[]
		testData.append(cmd_forward)
		thread = Thread(self.runTest, testData)
		thread.finished.connect(lambda:self.thread_finished(thread))
		thread.start()
		time.sleep(0.1)
		
		targetPos=self.update_target(cmd_forward)		
		direction=np.array([np.sign(float(pump_instruction_list[0])),np.sign(float(pump_instruction_list[1])),np.sign(float(pump_instruction_list[2]))])
		threadm = Thread(self.monitorMoves,targetPos)
		threadm.finished.connect(lambda:self.thread_finished(threadm))
		threadm.start()		
		while not threadm.isFinished():
			QtWidgets.QApplication.processEvents()
			pass

		self.ui.auto_injection_number_LCD.display(self.auto_counter)
		self.ui.auto_injection_left_LCD.display(injection_n - self.auto_counter)
		
		print("AUTO RUN command #%d sent." % (self.auto_counter))
		
		#print(testData)
		
	def auto_update_stop(self):
		self.ui.auto_injection_left_LCD.display(self.auto_injection_number)
		self.ui.auto_injection_number_LCD.display(0)
		self.auto_counter = 0
		self.auto_timer.stop()
		
		self.ui.p1_activate_CHECKBOX.setChecked(False)
		self.ui.p2_activate_CHECKBOX.setChecked(False)
		self.ui.p3_activate_CHECKBOX.setChecked(False)
		
		print("Finished Auto Run. \n\n\n")
		self.send_all()
		
		#think about this
		#self.auto_time_stop()
		
		
	def auto_time_update(self, total_time):
		self.auto_time_counter += 1
		
		self.auto_displayTime = total_time - self.auto_time_counter
		self.auto_display_time()
		#self.ui.auto_time_left_LCD.display(total_time - self.auto_time_counter)
		#self.ui.auto_time_passed_LCD.display(self.auto_time_counter)
		if self.auto_time_counter >= total_time:
			self.auto_time_stop()
		#print(testData)
		
	def auto_time_stop(self):
		
		self.auto_displayTime = self.auto_total_time
		self.auto_time_counter = 0
		
		self.auto_display_time()
		self.auto_time_timer.stop()
		
		#think about this
		self.auto_update_stop()
		
	def auto_stop(self):
		self.stop()
		self.auto_update_stop()
		self.auto_time_stop()
		
	####################################################
	# Linear run routines (these are for the gradient) #
	####################################################
	
	def set_linear_initial_concentration(self):
		self.linear_initial_concentration = self.ui.linear_initial_concentration_INPUT.value()
		if self.linear_counter == -1:
			self.ui.linear_current_concentration_LCD.display(self.linear_initial_concentration)
		
		self.set_linear_total_time()
		#self.linear_display_initial_injection_size() this is called in total time
		
	def set_linear_syringe_concentration(self):
		self.linear_syringe_concentration = self.ui.linear_syringe_concentration_INPUT.value()
		
		self.linear_display_initial_injection_size()
		
	def set_linear_target_concentration(self):
		self.linear_target_concentration = self.ui.linear_target_concentration_INPUT.value()
		self.set_linear_total_time()
		
	'''def set_linear_latent_time(self):
		self.linear_latent_time = self.ui.linear_latent_time_INPUT.value()
		
	def set_linear_pinject(self):
		self.p_linear_inject = self.ui.linear_pinject_DROPDOWN.currentText()
		
		self.set_linear_units()
		self.set_linear_syringe()
		self.set_linear_speed_and_accel()
		
		
	def set_linear_pextract(self):
		self.p_linear_extract = self.ui.linear_pextract_DROPDOWN.currentText()
		
		self.set_linear_units()
		self.set_linear_syringe()
		self.set_linear_speed_and_accel()'''
	
	def set_linear_duty_ratio(self):
		self.linear_duty_ratio = self.ui.linear_duty_ratio_INPUT.value()
		if self.premix_is_active:
			self.linear_duty_ratio = min(self.linear_duty_ratio,0.5)
		#print(self.ui.auto_injection_number_LCD.value())
		#self.set_linear_concentration_slope() total time calls this
		self.set_linear_total_time()
	
	def set_linear_total_time(self):
		if self.linear_m != 0 and (self.linear_target_concentration - self.linear_initial_concentration) > 0:
			self.linear_total_time = (self.linear_target_concentration - self.linear_initial_concentration) / self.linear_m
		else:
			self.linear_total_time = 0
		
		self.injecting_total_time = self.linear_total_time * self.linear_duty_ratio
		#print(self.experiment_time_length, self.linear_total_time)
		if self.linear_counter == -1:
			self.linear_displayTime = self.linear_total_time
			self.auto_display_time()
			
		self.linear_display_initial_injection_size()
		
		
		
	def set_linear_units(self):
		p1 = self.ui.p1_units_DROPDOWN.currentText()
		p2 = self.ui.p2_units_DROPDOWN.currentText()
		p3 = self.ui.p3_units_DROPDOWN.currentText()
		
		pump_units = (p1,p2,p3)
		
		inject_units = pump_units[int(self.p_auto_inject) - 1]
		extract_units = pump_units[int(self.p_auto_extract) - 1]
		
		if inject_units != extract_units:
			self.p_linear_units = False
		else:
			self.p_linear_units = inject_units
			
		self.linear_concentration_units_display()
		
	def set_linear_syringe(self):
		p1 = self.ui.p1_syringe_DROPDOWN.currentText()
		p2 = self.ui.p2_syringe_DROPDOWN.currentText()
		p3 = self.ui.p3_syringe_DROPDOWN.currentText()
		
		pump_syringes = (p1,p2,p3)
		
		inject_syringe = pump_syringes[int(self.p_auto_inject) - 1]
		extract_syringe = pump_syringes[int(self.p_auto_extract) - 1]
		
		if inject_syringe != extract_syringe:
			self.p_linear_syringe_area = False
		else:
			self.p_linear_syringe_area = self.syringe_areas[self.syringe_options.index(inject_syringe)]
		
	def linear_inject_volume_state(self, t, ins_cons, syr_cons, m):
		return np.log(syr_cons - ins_cons - m * t)
			
	def set_linear_solution_volume(self):
		self.linear_container_volume = self.ui.linear_solution_volume_INPUT.value()
		
		self.linear_display_initial_injection_size()
		
	def set_linear_concentration_slope(self):
		self.linear_m = self.ui.linear_concentration_slope_INPUT.value()# average concentration/time
		
		local_m = self.linear_m / self.linear_duty_ratio # Will be larger than average_m
#		print(self.linear_m)
		#print(self.linear_m)
		#self.linear_m = self.ui.linear_concentration_slope_INPUT.value()
		self.set_linear_total_time()# Total time for run
		#self.linear_display_initial_injection_size() total time calls this
		
	def linear_concentration_units_display(self):
		#units = self.ui.linear_concentration_units_DROPDOWN.currentText()
		units = "M"
		self.ui.linear_initial_concentration_LABEL.setText(units)
		self.ui.linear_syringe_concentration_LABEL.setText(units)
		self.ui.linear_target_concentration_LABEL.setText(units)
		if self.p_linear_units:
			self.ui.linear_concentration_gradient_LABEL.setText(units + "/" + self.p_linear_units.split("/")[1])
			if self.p_linear_units.split("/")[0] == "mm":
				self.ui.linear_solution_volume_LABEL.setText("μL")
				self.ui.linear_injection_size_LABEL.setText("Injection Size (μL)")
			else:
				self.ui.linear_solution_volume_LABEL.setText(self.p_linear_units.split("/")[0])
				self.ui.linear_injection_size_LABEL.setText("Injection Size (%s)" % self.p_linear_units.split("/")[0])
		else:
			self.ui.linear_concentration_gradient_LABEL.setText(units + "/???")
			self.ui.linear_solution_volume_LABEL.setText("???")
			self.ui.linear_injection_size_LABEL.setText("Injection Size (???)")
			
	def linear_display_initial_injection_size(self):
		
		time_interval = self.linear_total_time / self.auto_injection_number

		state_final = self.linear_inject_volume_state(time_interval, self.linear_initial_concentration, self.linear_syringe_concentration, self.linear_m)
		
		state_initial = self.linear_inject_volume_state(0, self.linear_initial_concentration, self.linear_syringe_concentration, self.linear_m)
		
		volume = -self.linear_container_volume * (state_final - state_initial)
		
		if volume == float("inf"):
			self.ui.linear_injection_size_LCD.display(99999)
		elif np.isnan(volume):
			self.ui.linear_injection_size_LCD.display(0)
		else:
			self.ui.linear_injection_size_LCD.display(volume)
		
		self.ui.injection_interval_LCD.display(time_interval)		
		
		
	
	def linear_run(self):
		
		self.statusBar().showMessage("You clicked Linear Run")
		
		print("Linear run started")
		active_and_different = (self.p_auto_inject != self.p_auto_extract)
		#same_units = isinstance(self.p_linear_units, str)
		#same_syringe_area = isinstance(self.p_linear_syringe_area, float)
		#same_accel = isinstance(self.p_linear_accel, float)
		self.linear_total_time = (self.linear_target_concentration - self.linear_initial_concentration) / self.linear_m
		self.injection_interval = self.linear_total_time / self.auto_injection_number
		print("Time between injections:",self.injection_interval)

		non_zero = self.linear_syringe_concentration != 0 and self.linear_target_concentration != 0 and self.linear_container_volume != 0 and self.linear_m != 0
		concentration_order = self.linear_syringe_concentration > self.linear_target_concentration and self.linear_target_concentration > self.linear_initial_concentration
		
		if (not active_and_different):
			self.statusBar().showMessage("Injection and extraction pumps must be enabled in 'Syringe Control' and be different.")
		elif (not self.p_linear_units):
			self.statusBar().showMessage("The two pumps must have the same units.")
		elif (not self.p_linear_syringe_area):
			self.statusBar().showMessage("The two pumps must have the same kind of syringe.")
		elif (not non_zero):
			self.statusBar().showMessage("Non-initial concentrations, solution volume, and concentration gradient must all be non-zero.")
		elif (not concentration_order):
			self.statusBar().showMessage("The syringe concentration must be greater than the target concentration, which must be greater than the initial concentration.")
		elif (self.injection_interval < 10.0):
			self.statusBar().showMessage("The period between injections must be greater than 10 seconds.")
		else:
			
			activation_instructions = [False,False,False]
			
			activation_instructions[int(self.p_auto_inject) - 1] = True
			activation_instructions[int(self.p_auto_extract) - 1] = True
			
			self.ui.p1_activate_CHECKBOX.setChecked(activation_instructions[0])
			self.ui.p2_activate_CHECKBOX.setChecked(activation_instructions[1])
			self.ui.p3_activate_CHECKBOX.setChecked(activation_instructions[2])
			
			#apparently a number times True equals the number and times False it equals 0
			self.ui.p1_accel_INPUT.setValue(4000 * activation_instructions[0])
			self.ui.p2_accel_INPUT.setValue(4000 * activation_instructions[1])
			self.ui.p3_accel_INPUT.setValue(4000 * activation_instructions[2])
			
			testData = []
			
			print("Sending accelerations")
			testData.extend(["<SETTING,ACCEL,1," + str(self.p1_accel_to_send) + ",F,0.0,0.0,0.0>", "<SETTING,ACCEL,2," + str(self.p2_accel_to_send) + ",F,0.0,0.0,0.0>", "<SETTING,ACCEL,3," + str(self.p3_accel_to_send) + ",F,0.0,0.0,0.0>"])
		
			thread = Thread(self.runTest, testData)
			thread.finished.connect(lambda:self.thread_finished(thread))
			thread.start()
			time.sleep(1)
			
			
			if self.linear_duty_ratio == 1:
				self.auto_injection_number = 1
				self.ui.auto_inject_number_INPUT.setValue(1)
			
			self.linear_counter = 0
			self.linear_time_counter = 0
			self.concentration_counter = 0
			
			
			injection_n = self.auto_injection_number
			cont_volume = self.linear_container_volume
			units = self.p_linear_units
			area = self.p_linear_syringe_area
			microstepping = self.microstepping
			inject = self.p_auto_inject
			extract = self.p_auto_extract
			total_time = self.linear_total_time# Total time for gradient, including time waiting
			exp_time = self.injecting_total_time# Time spent injecting only
			
			ini_cons = self.linear_initial_concentration
			syr_cons = self.linear_syringe_concentration
			m = self.linear_m
			
			
			self.linear_timer = QtCore.QTimer(self)
			self.linear_timer.timeout.connect(lambda:self.linear_update(injection_n, cont_volume, units, area, microstepping, inject, extract, exp_time, ini_cons, syr_cons, m))
# 			self.linear_timer.timeout.connect(lambda:self.linear_update_testing(injection_n, cont_volume, units, area, microstepping, inject, extract, exp_time, ini_cons, syr_cons, m))
			
			self.linear_time_timer = QtCore.QTimer(self)
			self.linear_time_timer.timeout.connect(lambda:self.linear_time_update(total_time, exp_time, injection_n, ini_cons, m))
			
			self.linear_update(injection_n, cont_volume, units, area, microstepping, inject, extract, exp_time, ini_cons, syr_cons, m)
# 			self.linear_update_testing(injection_n, cont_volume, units, area, microstepping, inject, extract, exp_time, ini_cons, syr_cons, m)
			self.linear_time_update(total_time, exp_time, injection_n, ini_cons, m)
			
			if self.linear_duty_ratio != 1:
				self.linear_timer.start(self.injection_interval * 1000)
			
			self.linear_time_timer.start(1000)

	def linear_update_testing(self, injection_n, cont_volume, units, area, microstepping, inject, extract, exp_time, ini_cons, syr_cons, m):
		
#		self.ui.p2_absolute_DISP.display(0)
#		self.ui.p3_absolute_DISP.display(0)

# 		self.threadTest1()
# 		time.sleep(1)
# 		self.threadTest2()
# 		thread = Thread(self.runTest, testData)
# 		thread.finished.connect(lambda:self.thread_finished(thread))
# 		thread.start()
		
		self.linear_counter += 1
		
		print("Linear update, injection number:",self.linear_counter)		
		self.ui.p1_absolute_DISP.display(self.linear_counter)
		self.ui.p2_absolute_DISP.display(-1)
# 		self.thread1 = WorkerThread()
# 		self.thread1.progress_updated.connect(self.update_volume2)
# 		self.thread1.start()
		thread1 = Thread(self.threadTest1)
		thread1.finished.connect(lambda:self.thread_finished(thread1))
		thread1.start()
		while not thread1.isFinished():
			QtWidgets.QApplication.processEvents()
			pass
# 		self.thread2 = WorkerThread()
# 		self.thread2.progress_updated.connect(self.update_volume3)
# 		self.thread2.start()

		time.sleep(0.1)
		thread2 = Thread(self.threadTest2)
		thread2.finished.connect(lambda:self.thread_finished(thread2))
		thread2.start()
		
		if self.linear_counter > injection_n:
			self.linear_update_stop()
			return
		

	
	def linear_update(self, injection_n, cont_volume, units, area, microstepping, inject, extract, exp_time, ini_cons, syr_cons, m):
		self.linear_counter += 1
		
		if self.linear_counter > injection_n:
			self.linear_update_stop()
			return
		
		t_interval = exp_time / injection_n
		t_next = t_interval * self.linear_counter
		t = t_interval * (self.linear_counter - 1)
		
			
		
		inject_volume = -cont_volume * (self.linear_inject_volume_state(t_next, ini_cons, syr_cons, m) - self.linear_inject_volume_state(t, ini_cons, syr_cons, m))
		self.ui.linear_injection_size_LCD.display(inject_volume)
		
		#have it set speed properly, make sure to adjust for units
		
		
		#check this, convert volume makes the inject volume in mm^3 to match syringe area (mm^2), units sent to convert speed 
		print("Inject volume",inject_volume)
		print("Area:",area)
		print("Time Interval",t_interval)
		p_linear_speed = (self.convert_volume(inject_volume) / area) / t_interval
		if self.is_premix_active:
			p_linear_speed=p_linear_speed*2
	
		
		print("Time:",t_interval,"Speed",p_linear_speed)
		
		p_linear_speed = self.convert_speed(p_linear_speed, "mm" + "/" + units.split("/")[1], area, microstepping)
		
		print("Time:",t_interval,"Speed",p_linear_speed)

		inject_speed = "<SETTING,SPEED,%s,%f,F,0.0,0.0,0.0>" % (inject, p_linear_speed)
		extract_speed = "<SETTING,SPEED,%s,%f,F,0.0,0.0,0.0>" % (extract, p_linear_speed)
		
		print("Writing speeds")
		testData = []
		testData.append(inject_speed)
		testData.append(extract_speed)
		
		thread = Thread(self.runTest, testData)
		thread.finished.connect(lambda:self.thread_finished(thread))
		thread.start()
		time.sleep(1.0)

		testData=[]
		active_pumps = self.get_active_pumps()
		pumps_2_run = ''.join(map(str,active_pumps))
		pump_instruction_list = ['0','0','0']

		if self.ui.photos_CHECKBOX.isChecked():
			self.save_image()
		#print(cmd)

		if self.is_premix_active:

			p_inject_displacement = str(self.convert_displacement(inject_volume, units, area, microstepping))
			p_extract_displacement = str(self.convert_displacement(0, units, area, microstepping))

			pump_instruction_list[int(inject) - 1] = p_inject_displacement
			pump_instruction_list[int(extract) - 1] = p_extract_displacement

			cmd_reverse = "<RUN,DIST," + pumps_2_run + ",0,F,%s,%s,%s>" % tuple(pump_instruction_list)

			print("Executing reverse pipetting")


			
			
			testData = []			
			testData.append(cmd_reverse)
			thread = Thread(self.runTest, testData)
			thread.finished.connect(lambda:self.thread_finished(thread))
			thread.start()
			time.sleep(0.1)
			
			
			targetPos=self.update_target(cmd_reverse)
			direction=np.array([np.sign(float(pump_instruction_list[0])),np.sign(float(pump_instruction_list[1])),np.sign(float(pump_instruction_list[2]))])
			threadm = Thread(self.monitorMoves,targetPos)
			threadm.finished.connect(lambda:self.thread_finished(threadm))
			threadm.start()	
			time.sleep(0.1)		
			while not threadm.isFinished():
				QtWidgets.QApplication.processEvents()
				pass

			p_inject_displacement = str(self.convert_displacement(-2*inject_volume, units, area, microstepping))
			p_extract_displacement = str(self.convert_displacement(inject_volume, units, area, microstepping))

			pump_instruction_list[int(inject) - 1] = p_inject_displacement
			pump_instruction_list[int(extract) - 1] = p_extract_displacement

			cmd_forward = "<RUN,DIST," + pumps_2_run + ",0,F,%s,%s,%s>" % tuple(pump_instruction_list)



		else:
			p_inject_displacement = str(self.convert_displacement(-inject_volume, units, area, microstepping))
			p_extract_displacement = str(self.convert_displacement(inject_volume, units, area, microstepping))

			pump_instruction_list[int(inject) - 1] = p_inject_displacement
			pump_instruction_list[int(extract) - 1] = p_extract_displacement

			cmd_forward = "<RUN,DIST," + pumps_2_run + ",0,F,%s,%s,%s>" % tuple(pump_instruction_list)

		testData=[]
		testData.append(cmd_forward)
		thread = Thread(self.runTest, testData)
		thread.finished.connect(lambda:self.thread_finished(thread))
		thread.start()
		time.sleep(0.1)
		
		targetPos=self.update_target(cmd_forward)		
		direction=np.array([np.sign(float(pump_instruction_list[0])),np.sign(float(pump_instruction_list[1])),np.sign(float(pump_instruction_list[2]))])
		threadm = Thread(self.monitorMoves,targetPos)
		threadm.finished.connect(lambda:self.thread_finished(threadm))
		threadm.start()		
		while not threadm.isFinished():
			QtWidgets.QApplication.processEvents()
			pass
			
		self.ui.auto_injection_number_LCD.display(self.linear_counter)
		self.ui.auto_injection_left_LCD.display(injection_n - self.linear_counter)
		#self.ui.linear_current_concentration_LCD.display(ini_cons + (m * t_interval * self.linear_counter))

		'''if self.linear_counter == injection_n:
			self.linear_update_stop()'''
			
		
		#print("\n\n SPEED: %f                       DISPLACEMENT: %s \n\n" % (p_linear_speed, p_inject_displacement))
	def linear_update_stop(self):
		self.ui.auto_injection_left_LCD.display(self.auto_injection_number)
		self.ui.auto_injection_number_LCD.display(0)
		self.linear_display_initial_injection_size()
		self.linear_counter = -1
		self.linear_timer.stop()
		print("Finished Linear Run. \n\n\n")
		
		self.ui.p1_activate_CHECKBOX.setChecked(False)
		self.ui.p2_activate_CHECKBOX.setChecked(False)
		self.ui.p3_activate_CHECKBOX.setChecked(False)
# 		
# 		self.ui.p1_accel_INPUT.setValue(0)
# 		self.ui.p2_accel_INPUT.setValue(0)
# 		self.ui.p3_accel_INPUT.setValue(0)
# 		
# 		testData = []
# 		testData.extend(["<SETTING,ACCEL,1,0,F,0.0,0.0,0.0>", "<SETTING,ACCEL,2,0,F,0.0,0.0,0.0>", "<SETTING,ACCEL,3,0,F,0.0,0.0,0.0>"])
# 		
# 		thread = Thread(self.runTest, testData)
# 		thread.finished.connect(lambda:self.thread_finished(thread))
# 		thread.start()

		self.send_all()

		
		#self.linear_time_stop()
		
		
	def linear_time_update(self, total_time, exp_time, injection_n, ini_cons, m):
		self.linear_time_counter += 1
		
		
		self.linear_displayTime = total_time - self.linear_time_counter
		
		self.auto_display_time()
		
		t_interval = exp_time / injection_n
		injection_interval = total_time / injection_n
		
		
		
		#concentration = ini_cons
		
		if (self.linear_time_counter % injection_interval) <= t_interval and self.linear_counter > -1 and (self.linear_time_counter % injection_interval) > 0:
			leap_update = np.ceil(np.modf(t_interval)[0] - np.modf(self.linear_time_counter % injection_interval)[0]) * int(np.ceil(np.modf(self.linear_time_counter % injection_interval)[0]))
			
			increment = t_interval / (int(t_interval) + leap_update)
			self.concentration_counter += increment
			#concentration = ini_cons + (m * ((self.linear_time_counter % t_interval) + ((self.linear_counter - 1) * t_interval) + isinstance(self.linear_time_counter / t_interval, int)))
			
			concentration = ini_cons + m * self.concentration_counter
			
			self.ui.linear_current_concentration_LCD.display(concentration)
			print(leap_update, self.linear_time_counter, self.linear_time_counter % injection_interval, injection_interval, t_interval)
			#print("TIME: %f" % ((self.linear_time_counter % t_interval) + (self.linear_counter * t_interval)))
		
		if self.linear_time_counter >= total_time:
			self.linear_time_stop()
			
		#print(testData)
		
		#time timer starts after the update function has been run once, meaning from the start linear counter = 1 here (hence the -1)
		
	def linear_time_stop(self):
		
		self.linear_displayTime = self.linear_total_time
		self.linear_time_counter = 0
		
		self.auto_display_time()
		self.linear_time_timer.stop()
		self.linear_update_stop()
		
	def linear_stop(self):
		self.stop()
		self.linear_update_stop()
		self.linear_time_stop()
		
	# ======================
	# FUNCTIONS : Camera
	# ======================

	# Initialize the camera
	def start_camera(self):
		self.statusBar().showMessage("You clicked START CAMERA")
		camera_port = 0
		self.capture = cv2.VideoCapture(camera_port)
		#TODO check the native resolution of the camera and scale the size down here
		self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
		self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 400)

		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.update_frame)
		self.timer.start(5)

	# Update frame function
	def update_frame(self):
		ret, self.image = self.capture.read()
		self.image = cv2.flip(self.image, 1)
		self.display_image(self.image, 1)

	# Display image in frame
	def display_image(self, image, window=1):
		qformat = QtGui.QImage.Format_Indexed8
		if len(image.shape) == 3: #
			if image.shape[2] == 4:
				qformat = QtGui.QImage.Format_RGBA8888

			else:
				qformat = QtGui.QImage.Format_RGB888
				#print(image.shape[0], image.shape[1], image.shape[2])
		self.img_2_display = QtGui.QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
		self.img_2_display = QtGui.QImage.rgbSwapped(self.img_2_display)

		if window == 1:
			self.ui.imgLabel.setPixmap(QtGui.QPixmap.fromImage(self.img_2_display))
			self.ui.imgLabel.setScaledContents(False)

	# Save image to set location
	def save_image(self):
		if not os.path.exists("./images"):
			os.mkdir("images")

		self.date_string =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		# Replace semicolons with underscores
		self.date_string = self.date_string.replace(":","_")
		self.write_image_loc = './images/'+self.date_string + '.png'
		cv2.imwrite(self.write_image_loc, self.image)
		self.statusBar().showMessage("Captured Image, saved to: " + self.write_image_loc)


	# Stop camera
	def stop_camera(self):
		self.timer.stop()

	# ======================
	# FUNCTIONS : Setup
	# ======================

	# Populate the available ports
	def populate_ports(self):
	    """
	        :raises EnvironmentError:
	            On unsupported or unknown platforms
	        :returns:
	            A list of the serial ports available on the system
	    """
	    print("Populating ports..")
	    if sys.platform.startswith('win'):
	        ports = ['COM%s' % (i + 1) for i in range(256)]
	    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
	        # this excludes your current terminal "/dev/tty"
	        ports = glob.glob('/dev/tty[A-Za-z]*')
	    elif sys.platform.startswith('darwin'):
	        ports = glob.glob('/dev/tty.*')
	    else:
	        raise EnvironmentError('Unsupported platform')

	    result = []
	    for port in ports:
	        try:
	            s = serial.Serial(port)
	            s.close()
	            result.append(port)
	        except (OSError, serial.SerialException):
	            pass
	    self.ui.port_DROPDOWN.addItems(result)
	    print("Ports have been populated.")

	# Refresh the list of ports
	def refresh_ports(self):
		self.statusBar().showMessage("You clicked REFRESH PORTS")
		self.ui.port_DROPDOWN.clear()
		self.populate_ports()
		self.set_port()

	# Set the port that is selected from the dropdown menu
	def set_port(self):
#		self.port = '/dev/tty.usbmodem11301'
		self.port = self.ui.port_DROPDOWN.currentText()

	# Set the microstepping amount from the dropdown menu
	# TODO: There is definitely a better way of updating different variables
	# after there is a change of some input from the user. need to figure out.
	def set_microstepping(self):
		self.microstepping = int(self.ui.microstepping_DROPDOWN.currentText())
		self.set_p1_units()
		self.set_p1_speed()
		self.set_p1_accel()
		self.set_p1_setup_jog_delta()
		self.set_p1_amount()

		self.set_p2_units()
		self.set_p2_speed()
		self.set_p2_accel()
		self.set_p2_setup_jog_delta()
		self.set_p2_amount()

		self.set_p3_units()
		self.set_p3_speed()
		self.set_p3_accel()
		self.set_p3_setup_jog_delta()
		self.set_p3_amount()
		
		self.set_auto_total_time()

		self.update_displays()
		#print(self.microstepping)

	def set_experiment_notes(self):
		self.experiment_notes = self.ui.experiment_notes.text()

	# Set the name of the log file
	# Can probably delete
	def set_log_file_name(self):
		"""
		Sets the file name for the current test run, enables us to log data to the file.

		Callback setter method from the 'self.ui.logFileNameInput' to set the
		name of the log file. The log file name is of the form
		label_Year-Month-Date hour_min_sec.txt
		"""
		# Create a date string
		self.date_string =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		# Replace semicolons with underscores
		self.date_string = self.date_string.replace(":","_")
		self.log_file_name = self.ui.log_file_name_INPUT.text() + "_" + self.date_string + ".png"

	def save_settings(self):
		# TODO: if you cancel then it gives error, fix this
		# TODO: add comment
		name, _ = QFileDialog.getSaveFileName(self,'Save File', options=QFileDialog.DontUseNativeDialog)

		# Create a date string
		self.date_string =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		# Replace semicolons with underscores
		self.date_string = self.date_string.replace(":","_")

		date_string = self.date_string

		# write all of the settings here
		## Settings for pump 1
		p1_syringe 			= str(self.p1_syringe)
		p1_units 			= str(self.p1_units)
		p1_speed 			= str(self.p1_speed)
		p1_accel 			= str(self.p1_accel)
		p1_setup_jog_delta 	= str(self.p1_setup_jog_delta)

		## Settings for pump 2
		p2_syringe 			= str(self.p2_syringe)
		p2_units 			= str(self.p2_units)
		p2_speed 			= str(self.p2_speed)
		p2_accel 			= str(self.p2_accel)
		p2_setup_jog_delta 	= str(self.p2_setup_jog_delta)

		## Settings for pump 3
		p3_syringe 			= str(self.p3_syringe)
		p3_units 			= str(self.p3_units)
		p3_speed 			= str(self.p3_speed)
		p3_accel 			= str(self.p3_accel)
		p3_setup_jog_delta 	= str(self.p3_setup_jog_delta)

		## Experiment Notes
		experiment_notes = self.experiment_notes

		text = []
		text.append("File name: " + name + ".txt" + "\n") 		# line 0
		text.append("Date time: " + date_string + "\n") 		# line 1

		text.append(":================================ \n") 	# line 2
		text.append("P1 Syrin: " + p1_syringe + "\n") 			# line 3
		text.append("P1 Units: " + p1_units + "\n") 			# line 4
		text.append("P1 Speed: " + p1_speed + "\n") 			# line 5
		text.append("P1 Accel: " + p1_accel + "\n") 			# line 6
		text.append("P1 Jog D: " + p1_setup_jog_delta + "\n") 	# line 7
		text.append(":================================ \n")		# line 8
		text.append("P2 Syrin: " + p2_syringe + "\n") 			# line 9
		text.append("P2 Units: " + p2_units + "\n") 			# line 10
		text.append("P2 Speed: " + p2_speed + "\n") 			# line 11
		text.append("P2 Accel: " + p2_accel + "\n") 			# line 12
		text.append("P2 Jog D: " + p2_setup_jog_delta + "\n") 	# line 13
		text.append(":================================ \n") 	# line 14
		text.append("P3 Syrin: " + p3_syringe + "\n") 			# line 15
		text.append("P3 Units: " + p3_units + "\n") 			# line 16
		text.append("P3 Speed: " + p3_speed + "\n") 			# line 17
		text.append("P3 Accel: " + p3_accel + "\n") 			# line 18
		text.append("P3 Jog D: " + p3_setup_jog_delta + "\n") 	# line 19
		text.append("Exp Note: " + experiment_notes)			# line 20

		if name:
			with open(name + ".txt", 'w') as f:
				f.writelines(text)
				self.statusBar().showMessage("Settings saved in " + name + ".txt")

	def load_settings(self):
		# need to make name an tuple otherwise i had an error and app crashed
		name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog, filter = "Text (*.txt)")

		if name:
			with open(name, 'r') as f:
				text = f.readlines()
				# here is where you load all of your variables
				# reformatting the text
				text = [line.split(':')[-1].strip('\n')[1:] for line in text]
				fname = text[0]
				date_string = text[1]

				p1_syringe 			= text[3]
				p1_units 			= text[4]
				p1_speed 			= text[5]
				p1_accel 			= text[6]
				p1_setup_jog_delta 	= text[7]

				p2_syringe 			= text[9]
				p2_units 			= text[10]
				p2_speed 			= text[11]
				p2_accel 			= text[12]
				p2_setup_jog_delta 	= text[13]

				p3_syringe 			= text[15]
				p3_units 			= text[16]
				p3_speed 			= text[17]
				p3_accel 			= text[18]
				p3_setup_jog_delta 	= text[19]

				experiment_notes 	= text[20]

				#print(fname, date_string, p1_syringe, p1_units, p1_speed, p1_accel, p1_setup_jog_delta)

			# Here we are setting all of the values as given by the settings file
			p1_syringe_index = self.ui.p1_syringe_DROPDOWN.findText(p1_syringe, QtCore.Qt.MatchFixedString)
			self.ui.p1_syringe_DROPDOWN.setCurrentIndex(p1_syringe_index)
			p1_units_index = self.ui.p1_units_DROPDOWN.findText(p1_units, QtCore.Qt.MatchFixedString)
			self.ui.p1_units_DROPDOWN.setCurrentIndex(p1_units_index)
			self.ui.p1_speed_INPUT.setValue(float(p1_speed))
			self.ui.p1_accel_INPUT.setValue(float(p1_accel))

			AllItems = [self.ui.p1_setup_jog_delta_INPUT.itemText(i) for i in range(self.ui.p1_setup_jog_delta_INPUT.count())]

			p1_setup_jog_delta_index = self.ui.p1_setup_jog_delta_INPUT.findText(p1_setup_jog_delta, QtCore.Qt.MatchFixedString)
			self.ui.p1_setup_jog_delta_INPUT.setCurrentIndex(p1_setup_jog_delta_index)


			p2_syringe_index = self.ui.p2_syringe_DROPDOWN.findText(p2_syringe, QtCore.Qt.MatchFixedString)
			self.ui.p2_syringe_DROPDOWN.setCurrentIndex(p2_syringe_index)
			p2_units_index = self.ui.p2_units_DROPDOWN.findText(p2_units, QtCore.Qt.MatchFixedString)
			self.ui.p2_units_DROPDOWN.setCurrentIndex(p2_units_index)
			self.ui.p2_speed_INPUT.setValue(float(p2_speed))
			self.ui.p2_accel_INPUT.setValue(float(p2_accel))

			p2_setup_jog_delta_index = self.ui.p2_setup_jog_delta_INPUT.findText(p2_setup_jog_delta, QtCore.Qt.MatchFixedString)
			self.ui.p2_setup_jog_delta_INPUT.setCurrentIndex(p2_setup_jog_delta_index)

			p3_syringe_index = self.ui.p3_syringe_DROPDOWN.findText(p3_syringe, QtCore.Qt.MatchFixedString)
			self.ui.p3_syringe_DROPDOWN.setCurrentIndex(p3_syringe_index)
			p3_units_index = self.ui.p3_units_DROPDOWN.findText(p3_units, QtCore.Qt.MatchFixedString)
			self.ui.p3_units_DROPDOWN.setCurrentIndex(p3_units_index)
			self.ui.p3_speed_INPUT.setValue(float(p3_speed))
			self.ui.p3_accel_INPUT.setValue(float(p3_accel))

			p3_setup_jog_delta_index = self.ui.p3_setup_jog_delta_INPUT.findText(p3_setup_jog_delta, QtCore.Qt.MatchFixedString)
			self.ui.p3_setup_jog_delta_INPUT.setCurrentIndex(p3_setup_jog_delta_index)

			self.ui.experiment_notes.setText(experiment_notes)

			self.statusBar().showMessage("Settings loaded from: " + text[1])
		else:
			self.statusBar().showMessage("No file selected.")

	# Populate the microstepping amounts for the dropdown menu
	def populate_microstepping(self):
		self.microstepping_values = ['1', '2', '4', '8', '16', '32']
		self.ui.microstepping_DROPDOWN.addItems(self.microstepping_values)
		self.microstepping = 1

	# Populate the list of possible syringes to the dropdown menus
	def populate_syringe_sizes(self):
		self.syringe_options = ["BD 1 mL", "BD 3 mL", "BD 5 mL", "BD 10 mL", "BD 20 mL", "BD 30 mL", "BD 60 mL"]
		self.syringe_volumes = [1, 3, 5, 10, 20, 30, 60]
		self.syringe_areas = [17.34206347, 57.88559215, 112.9089185, 163.539454, 285.022957, 366.0961536, 554.0462538]

		self.ui.p1_syringe_DROPDOWN.addItems(self.syringe_options)
		self.ui.p2_syringe_DROPDOWN.addItems(self.syringe_options)
		self.ui.p3_syringe_DROPDOWN.addItems(self.syringe_options)

	# Set Px syringe
	def set_p1_syringe(self):
		self.p1_syringe = self.ui.p1_syringe_DROPDOWN.currentText()
		self.p1_syringe_area = self.syringe_areas[self.syringe_options.index(self.p1_syringe)]
		self.display_p1_syringe()

		self.set_p1_units()
		self.set_p1_speed()
		self.set_p1_accel()
		self.set_p1_setup_jog_delta()
		self.set_p1_amount()

	def set_p2_syringe(self):
		self.p2_syringe = self.ui.p2_syringe_DROPDOWN.currentText()
		self.p2_syringe_area = self.syringe_areas[self.syringe_options.index(self.p2_syringe)]
		self.display_p2_syringe()

		self.set_p2_units()
		self.set_p2_speed()
		self.set_p2_accel()
		self.set_p2_setup_jog_delta()
		self.set_p2_amount()

	def set_p3_syringe(self):
		self.p3_syringe = self.ui.p3_syringe_DROPDOWN.currentText()
		self.p3_syringe_area = self.syringe_areas[self.syringe_options.index(self.p3_syringe)]
		self.display_p3_syringe()

		self.set_p3_units()
		self.set_p3_speed()
		self.set_p3_accel()
		self.set_p3_setup_jog_delta()
		self.set_p3_amount()

	# Set Px units
	def set_p1_units(self):
		self.p1_units = self.ui.p1_units_DROPDOWN.currentText()

		length = self.p1_units.split("/")[0]
		self.ui.p1_units_LABEL_2.setText(length)

		self.set_p1_speed()
		self.set_p1_accel()
		self.set_p1_setup_jog_delta()
		self.set_p1_amount()

	def set_p2_units(self):
		self.p2_units = self.ui.p2_units_DROPDOWN.currentText()

		length = self.p2_units.split("/")[0]
		self.ui.p2_units_LABEL_2.setText(length)

		self.set_p2_speed()
		self.set_p2_accel()
		self.set_p2_setup_jog_delta()
		self.set_p2_amount()


	def set_p3_units(self):
		self.p3_units = self.ui.p3_units_DROPDOWN.currentText()

		length = self.p3_units.split("/")[0]
		self.ui.p3_units_LABEL_2.setText(length)

		self.set_p3_speed()
		self.set_p3_accel()
		self.set_p3_setup_jog_delta()
		self.set_p3_amount()


	def populate_pump_units(self):
#		self.units = ['mm/s', 'mL/s', 'mL/hr', 'µL/s', 'µL/min', 'µL/hr']
		self.units = ['µL/s', 'µL/min', 'µL/hr', 'mL/s', 'mL/hr','mm/s' ]
		self.ui.p1_units_DROPDOWN.addItems(self.units)
		self.ui.p2_units_DROPDOWN.addItems(self.units)
		self.ui.p3_units_DROPDOWN.addItems(self.units)

	def populate_pump_jog_delta(self):
		self.jog_delta = ['10.0','1.0','0.1','0.01']
		self.ui.p1_setup_jog_delta_INPUT.addItems(self.jog_delta)
		self.ui.p2_setup_jog_delta_INPUT.addItems(self.jog_delta)
		self.ui.p3_setup_jog_delta_INPUT.addItems(self.jog_delta)

	# Set Px speed
	def set_p1_speed(self):
		self.p1_speed = self.ui.p1_speed_INPUT.value()
		self.ui.p1_units_LABEL.setText(str(self.p1_speed) + " " + self.ui.p1_units_DROPDOWN.currentText())
		self.p1_speed_to_send = self.convert_speed(self.p1_speed, self.p1_units, self.p1_syringe_area, self.microstepping)

	def set_p2_speed(self):
		self.p2_speed = self.ui.p2_speed_INPUT.value()
		self.ui.p2_units_LABEL.setText(str(self.p2_speed) + " " + self.ui.p2_units_DROPDOWN.currentText())
		self.p2_speed_to_send = self.convert_speed(self.p2_speed, self.p2_units, self.p2_syringe_area, self.microstepping)

	def set_p3_speed(self):
		self.p3_speed = self.ui.p3_speed_INPUT.value()
		self.ui.p3_units_LABEL.setText(str(self.p3_speed) + " " + self.ui.p3_units_DROPDOWN.currentText())
		self.p3_speed_to_send = self.convert_speed(self.p3_speed, self.p3_units, self.p3_syringe_area, self.microstepping)

	# Set Px accel
	def set_p1_accel(self):
		if self.user_accelerations:
			self.p1_accel = self.ui.p1_accel_INPUT.value()
			self.p1_accel_to_send = self.convert_accel(self.p1_accel, self.p1_units, self.p1_syringe_area, self.microstepping)
		else:
			self.p1_accel_to_send = self.default_accel

	def set_p2_accel(self):
		if self.user_accelerations:
			self.p2_accel = self.ui.p2_accel_INPUT.value()
			self.p2_accel_to_send = self.convert_accel(self.p2_accel, self.p2_units, self.p2_syringe_area, self.microstepping)
		else:
			self.p2_accel_to_send = self.default_accel

	def set_p3_accel(self):
		if self.user_accelerations:
			self.p3_accel = self.ui.p3_accel_INPUT.value()
			self.p3_accel_to_send = self.convert_accel(self.p3_accel, self.p3_units, self.p3_syringe_area, self.microstepping)
		else:
			self.p3_accel_to_send = self.default_accel

	# Set Px jog delta (setup)
	def set_p1_setup_jog_delta(self):
		self.p1_setup_jog_delta = self.ui.p1_setup_jog_delta_INPUT.currentText()
		self.p1_setup_jog_delta = float(self.ui.p1_setup_jog_delta_INPUT.currentText())
		self.p1_setup_jog_delta_to_send = self.convert_displacement(self.p1_setup_jog_delta, self.p1_units, self.p1_syringe_area, self.microstepping)

	def set_p2_setup_jog_delta(self):
		self.p2_setup_jog_delta = float(self.ui.p2_setup_jog_delta_INPUT.currentText())
		self.p2_setup_jog_delta_to_send = self.convert_displacement(self.p2_setup_jog_delta, self.p2_units, self.p2_syringe_area, self.microstepping)

	def set_p3_setup_jog_delta(self):
		self.p3_setup_jog_delta = float(self.ui.p3_setup_jog_delta_INPUT.currentText())
		self.p3_setup_jog_delta_to_send = self.convert_displacement(self.p3_setup_jog_delta, self.p3_units, self.p3_syringe_area, self.microstepping)

	# Send Px settings
	def send_p1_settings(self):
		self.statusBar().showMessage("You clicked SEND P1 SETTINGS")
		self.p1_settings = []
		self.p1_settings.append("<SETTING,SPEED,1," + str(self.p1_speed_to_send) + ",F,0.0,0.0,0.0>")
		self.p1_settings.append("<SETTING,ACCEL,1," + str(self.p1_accel_to_send) + ",F,0.0,0.0,0.0>")
		self.p1_settings.append("<SETTING,DELTA,1," + str(self.p1_setup_jog_delta_to_send) + ",F,0.0,0.0,0.0>")

		print("Sending P1 SETTINGS..")
		thread = Thread(self.runTest, self.p1_settings)
		thread.finished.connect(lambda:self.thread_finished(thread))
		thread.start()
		print("P1 SETTINGS sent.")

	def send_p2_settings(self):
		self.statusBar().showMessage("You clicked SEND P2 SETTINGS")
		self.p2_settings = []
		self.p2_settings.append("<SETTING,SPEED,2," + str(self.p2_speed_to_send) + ",F,0.0,0.0,0.0>")
		self.p2_settings.append("<SETTING,ACCEL,2," + str(self.p2_accel_to_send) + ",F,0.0,0.0,0.0>")
		self.p2_settings.append("<SETTING,DELTA,2," + str(self.p2_setup_jog_delta_to_send) + ",F,0.0,0.0,0.0>")

		print("Sending P2 SETTINGS..")
		thread = Thread(self.runTest, self.p2_settings)
		thread.finished.connect(lambda:self.thread_finished(thread))
		thread.start()
		print("P2 SETTINGS sent.")

	def send_p3_settings(self):
		self.statusBar().showMessage("You clicked SEND P3 SETTINGS")
		self.p3_settings = []
		self.p3_settings.append("<SETTING,SPEED,3," + str(self.p3_speed_to_send) + ",F,0.0,0.0,0.0>")
		self.p3_settings.append("<SETTING,ACCEL,3," + str(self.p3_accel_to_send) + ",F,0.0,0.0,0.0>")
		self.p3_settings.append("<SETTING,DELTA,3," + str(self.p3_setup_jog_delta_to_send) + ",F,0.0,0.0,0.0>")

		print("Sending P3 SETTINGS..")
		thread = Thread(self.runTest, self.p3_settings)
		thread.finished.connect(lambda:self.thread_finished(thread))
		thread.start()
		print("P3 SETTINGS sent.")

	def set_auto_variables(self):
		self.auto_volume = self.ui.auto_volume_INPUT.value()
		self.p_auto_inject = self.ui.auto_pinject_DROPDOWN.currentText()
		self.p_auto_extract = self.ui.auto_pextract_DROPDOWN.currentText()
		self.auto_injection_number = self.ui.auto_inject_number_INPUT.value()
		self.auto_latent_time = self.ui.auto_latent_time_INPUT.value()
		
		self.p_auto_units = self.ui.p1_units_DROPDOWN.currentText()
		
		self.display_auto_units()
		
		inject_syringe = self.ui.p1_syringe_DROPDOWN.currentText()
		self.p_auto_syringe_area = self.syringe_areas[self.syringe_options.index(inject_syringe)]
		
		self.p_auto_speed = self.ui.p1_speed_INPUT.value()
		self.p_auto_accel = self.ui.p1_accel_INPUT.value()
		
		self.auto_find_inject_time()
		
		self.auto_total_time = 0
		self.auto_displayTime = self.auto_total_time
		
		self.auto_counter = 0
		self.auto_time_counter = 0
		self.latent_time_units = self.ui.latent_time_units_DROPDOWN.currentText()
		# Linaer (maybe make this a different function)
		
		self.linear_initial_concentration = self.ui.linear_initial_concentration_INPUT.value()
		self.linear_syringe_concentration = self.ui.linear_syringe_concentration_INPUT.value()
		self.linear_target_concentration = self.ui.linear_target_concentration_INPUT.value()
		#self.linear_latent_time = self.ui.linear_latent_time_INPUT.value()
		
		self.p_linear_units = self.ui.p1_units_DROPDOWN.currentText()
		
		'''self.p_linear_inject = self.ui.linear_pinject_DROPDOWN.currentText()
		self.p_linear_extract = self.ui.linear_pextract_DROPDOWN.currentText()'''
		
		self.p_linear_syringe_area = self.syringe_areas[self.syringe_options.index(inject_syringe)]
		self.linear_container_volume = self.ui.linear_solution_volume_INPUT.value()
		self.linear_m = self.ui.linear_concentration_slope_INPUT.value()
		self.injecting_total_time = 0
		self.linear_total_time = 0
		self.linear_displayTime = self.linear_total_time
		self.linear_duty_ratio = self.ui.linear_duty_ratio_INPUT.value()## Between 0 and 1. # of time spent injecting
		
		self.linear_counter = -1
		self.linear_time_counter = 0
		self.linear_concentration_units_display()


		
		
	# Connect to the Arduino board
	def connect(self):
		#self.port_nano = '/dev/cu.usbserial-A9M11B77'
		#self.port_uno = "/dev/cu.usbmodem1411"
		#self.baudrate = baudrate
		#self.port_uno = '/dev/tty.usbmodem11301'
		self.statusBar().showMessage("You clicked CONNECT TO CONTROLLER")
		try:
			port_declared = self.port in vars()
			try:
				self.serial = serial.Serial()
				self.serial.port = self.port
				self.serial.baudrate = 230400
				self.serial.parity = serial.PARITY_NONE
				self.serial.stopbits = serial.STOPBITS_ONE
				self.serial.bytesize = serial.EIGHTBITS
				self.serial.timeout = 1
				self.serial.open()
				#self.serial.flushInput()

				# This is a thread that always runs and listens to commands from the Arduino
				#self.global_listener_thread = Thread(self.listening)
				#self.global_listener_thread.finished.connect(lambda:self.self.thread_finished(self.global_listener_thread))
				#self.global_listener_thread.start()

				# ~~~~~~~~~~~~~~~~
				# TAB : Setup
				# ~~~~~~~~~~~~~~~~
				self.ui.disconnect_BTN.setEnabled(True)
				self.ui.p1_setup_send_BTN.setEnabled(True)
				self.ui.p2_setup_send_BTN.setEnabled(True)
				self.ui.p3_setup_send_BTN.setEnabled(True)
				self.ui.send_all_BTN.setEnabled(True)

				self.ui.connect_BTN.setEnabled(False)
				time.sleep(3)
				self.statusBar().showMessage("Successfully connected to board.")
				
				self.send_all()
			except:
				self.statusBar().showMessage("Cannot connect to board. Try again..")
				raise CannotConnectException
		except AttributeError:
			self.statusBar().showMessage("Please plug in the board and select a proper port, then press connect.")



	# Disconnect from the Arduino board
	# TODO: figure out how to handle error..
	def disconnect(self):
		self.statusBar().showMessage("You clicked DISCONNECT FROM BOARD")
		print("Disconnecting from board..")
		#self.global_listener_thread.stop()
		time.sleep(3)
		self.serial.close()
		print("Board has been disconnected")

		self.grey_out_components()
		self.ui.connect_BTN.setEnabled(True)
		self.ui.disconnect_BTN.setEnabled(False)

	# Send all settings
	def send_all(self):
		self.statusBar().showMessage("You clicked SEND ALL SETTINGS")

		self.settings = []
		self.settings.append("<SETTING,SPEED,1,"+str(self.p1_speed_to_send)+",F,0.0,0.0,0.0>")
		self.settings.append("<SETTING,ACCEL,1,"+str(self.p1_accel_to_send)+",F,0.0,0.0,0.0>")
		self.settings.append("<SETTING,DELTA,1,"+str(self.p1_setup_jog_delta_to_send)+",F,0.0,0.0,0.0>")

		self.settings.append("<SETTING,SPEED,2,"+str(self.p2_speed_to_send)+",F,0.0,0.0,0.0>")
		self.settings.append("<SETTING,ACCEL,2,"+str(self.p2_accel_to_send)+",F,0.0,0.0,0.0>")
		self.settings.append("<SETTING,DELTA,2,"+str(self.p2_setup_jog_delta_to_send)+",F,0.0,0.0,0.0>")

		self.settings.append("<SETTING,SPEED,3,"+str(self.p3_speed_to_send)+",F,0.0,0.0,0.0>")
		self.settings.append("<SETTING,ACCEL,3,"+str(self.p3_accel_to_send)+",F,0.0,0.0,0.0>")
		self.settings.append("<SETTING,DELTA,3,"+str(self.p3_setup_jog_delta_to_send)+",F,0.0,0.0,0.0>")

		print("Sending all settings..")
		self.runTest(self.settings)
		thread = Thread(self.runTest, self.settings)
		thread.finished.connect(lambda:self.thread_finished(thread))
		thread.start()

		self.ui.p1_setup_send_BTN.setStyleSheet("background-color: none")
		self.ui.p2_setup_send_BTN.setStyleSheet("background-color: none")
		self.ui.p3_setup_send_BTN.setStyleSheet("background-color: none")

		self.ungrey_out_components()

		self.update_displays()
	


	# =======================
	# MISC : Functions I need
	# =======================

	def steps2mm(self, steps, microsteps):
	# 200 steps per rev
	# one rev is 0.8mm dist
		#mm = steps/200/32*0.8
		mm = steps/200/microsteps*0.8
		return mm

	def steps2mL(self, steps, syringe_area):
		mL = self.mm32mL(self.steps2mm(steps,self.microstepping)*syringe_area)
		return mL

	def steps2uL(self, steps, syringe_area):
		uL = self.mm32uL(self.steps2mm(steps,self.microstepping)*syringe_area)
		return uL


	def mm2steps(self, mm, microsteps):
		steps = mm/0.8*200*microsteps
		#steps = mm*200/0.8
#		print(steps)
		return steps

	def mL2steps(self, mL, syringe_area, microsteps):
		# note syringe_area is in mm^2
		steps = self.mm2steps(self.mL2mm3(mL)/syringe_area, microsteps)
		return steps

	def uL2steps(self, uL, syringe_area, microsteps):
		steps = self.mm2steps(self.uL2mm3(uL)/syringe_area, microsteps)
		return steps


	def mL2uL(self, mL):
		return mL*1000.0

	def mL2mm3(self, mL):
		return mL*1000.0


	def uL2mL(self, uL):
		return uL/1000.0

	def uL2mm3(self, uL):
		return uL


	def mm32mL(self, mm3):
		return mm3/1000.0

	def mm32uL(self, mm3):
		return mm3

	def persec2permin(self, value_per_sec):
		value_per_min = value_per_sec*60.0
		return value_per_min

	def persec2perhour(self, value_per_sec):
		value_per_hour = value_per_sec*60.0*60.0
		return value_per_hour


	def permin2perhour(self, value_per_min):
		value_per_hour = value_per_min*60.0
		return value_per_hour

	def permin2persec(self, value_per_min):
		value_per_sec = value_per_min/60.0
		return value_per_sec


	def perhour2permin(self, value_per_hour):
		value_per_min = value_per_hour/60.0
		return value_per_min

	def perhour2persec(self, value_per_hour):
		value_per_sec = value_per_hour/60.0/60.0
		return value_per_sec

	def convert_displacement(self, displacement, units, syringe_area, microsteps):
		length = units.split("/")[0]
		time = units.split("/")[1]
		inp_displacement = displacement
		# convert length first
		if length == "mm":
			displacement = self.mm2steps(displacement, microsteps)
		elif length == "mL":
			displacement = self.mL2steps(displacement, syringe_area, microsteps)
		elif length == "µL":
			displacement = self.uL2steps(displacement, syringe_area, microsteps)

		print('______________________________')
		print("INPUT  DISPLACEMENT: " + str(inp_displacement) + ' ' + length)
		print("OUTPUT DISPLACEMENT: " + str(displacement) + ' steps')
		print('\n############################################################\n')
		return displacement

	def convert_speed(self, inp_speed, units, syringe_area, microsteps):
		length = units.split("/")[0]
		time = units.split("/")[1]


		# convert length first
		if length == "mm":
			speed = self.mm2steps(inp_speed, microsteps)
		elif length == "mL":
			speed = self.mL2steps(inp_speed, syringe_area, microsteps)
		elif length == "µL":
			speed = self.uL2steps(inp_speed, syringe_area, microsteps)


		# convert time next
		if time == "s":
			pass
		elif time == "min":
			speed = self.permin2persec(speed)
		elif time == "hr":
			speed = self.perhour2persec(speed)



		print("INPUT  SPEED: " + str(inp_speed) + ' ' + units)
		print("OUTPUT SPEED: " + str(speed) + ' steps/s')
		return speed

	def convert_accel(self, accel, units, syringe_area, microsteps):
		length = units.split("/")[0]
		time = units.split("/")[1]
		inp_accel = accel
		accel = accel

		# convert length first
		if length == "mm":
			accel = self.mm2steps(accel, microsteps)
		elif length == "mL":
			accel = self.mL2steps(accel, syringe_area, microsteps)
		elif length == "µL":
			accel = self.uL2steps(accel, syringe_area, microsteps)

		# convert time next
		if time == "s":
			pass
		elif time == "min":
			accel = self.permin2persec(self.permin2persec(accel))
		elif time == "hr":
			accel = self.perhour2persec(self.perhour2persec(accel))

		print('______________________________')
		print("INPUT  ACCEL: " + str(inp_accel) + ' ' + units + '/' + time)
		print("OUTPUT ACCEL: " + str(accel) + ' steps/s/s')
		return accel

	def convert_time(self, time):
		if self.latent_time_units == "s":
			pass
		elif self.latent_time_units == "min":
			time = time * 60
		elif self.latent_time_units == "hr":
			time = time * 3600
			
		return time
	
	def convert_volume(self, volume):
		volume_units = self.p_linear_units.split("/")[0]
		if volume_units == "mm":
			pass
		elif volume_units == "mL":
			volume = self.mL2mm3(volume)
		elif volume_units == "µL":
			volume = self.uL2mm3(volume)
		return volume

	'''
		Syringe Volume (mL)	|		Syringe Area (mm^2)
	-----------------------------------------------
		1				|			17.34206347
		3				|			57.88559215
		5				|			112.9089185
		10				|			163.539454
		20				|			285.022957
		30				|			366.0961536
		60				|			554.0462538

	IMPORTANT: These are for BD Plastic syringes ONLY!! Others will vary.
	'''
	def getSteps(self,command):
		steps=np.zeros(3)
		cmdlist=command.split(",")
#		print(cmdlist,cmdlist[7].split('>')[0])
		if cmdlist[0] == '<RUN':
			if "1" in cmdlist[2]:
				steps[0]=2*((cmdlist[4]=='F')-0.5)*float(cmdlist[5]);
			if "2" in cmdlist[2]:
				steps[1]=2*((cmdlist[4]=='F')-0.5)*float(cmdlist[6]);
			if "3" in cmdlist[2]:
				steps[2]=2*((cmdlist[4]=='F')-0.5)*float(cmdlist[7].split('>')[0]);
		return(steps)
				


	#====================================== Reading and Writing to Arduino

	def sendToArduino(self, sendStr):
		self.serial.write(sendStr.encode())
		self.serial.flushInput()


	def recvPositionArduino(self):
		startMarker = self.startMarker
		midMarker = self.midMarker
		endMarker = self.endMarker

		ck = ""
		whole = ""
		x = "z" # any value that is not an end- or startMarker

		# wait for the start character
#		print("Before reading:",x)
		while ord(x) != startMarker:
			while self.serial.in_waiting==0:# Seems needed for very low flow rates
				pass
			x = self.serial.read()
			whole = whole + x.decode()

		# save data until the end marker is found
		while ord(x) != endMarker:
			if ord(x) == midMarker:
				ck = ""
				x = self.serial.read()
				whole = whole + x.decode()

			if ord(x) != startMarker:
				ck = ck + x.decode()
				whole = whole + x.decode()

			x = self.serial.read()

#		return(ck)
		return(whole)

	def recnewPositionArduino(self):
		startMarker = self.startMarker
		midMarker = self.midMarker
		endMarker = self.endMarker

		ck = ""
		x = "z" # any value that is not an end- or startMarker

		# wait for the start character
		while  ord(x) != startMarker:
			x = self.serial.read()

		# save data until the end marker is found
		while ord(x) != endMarker:
#			if ord(x) == midMarker:
##				print(ck)
#				self.ui.p1_absolute_DISP.display(ck)
#				ck = ""
#				x = self.serial.read()

			if ord(x) != startMarker:
		    #print(x)
				ck = ck + x.decode()

			x = self.serial.read()

		return(ck)

	#============================
	def update_volume(self,pump, vol):
		if pump == 1:
			self.ui.p1_absolute_DISP.display(vol)
		if pump == 2:
			self.ui.p2_absolute_DISP.display(vol)
		if pump == 3:
			self.ui.p3_absolute_DISP.display(vol)



	def update_volume2(self,vol):
		self.ui.p2_absolute_DISP.display(vol)
	def update_volume3(self,vol):
		self.ui.p3_absolute_DISP.display(vol)
				
	
	def update_displays(self):
#		print (self.p1_units.split('/'))
#		print("Updating displays to:",calib[1,:])
		calib=np.loadtxt("calibration.txt")

		if self.p2_units.split('/')[0]=="µL":
			self.ui.p2_absolute_DISP.display(self.steps2uL(calib[1,1],self.p2_syringe_area))
		if self.p2_units.split('/')[0]=="mL":
			self.ui.p2_absolute_DISP.display(self.steps2mL(calib[1,1],self.p2_syringe_area))
		if self.p2_units.split('/')[0]=="mm":
			self.ui.p2_absolute_DISP.display(self.steps2mm(calib[1,1],self.microstepping))
		if self.p3_units.split('/')[0]=="µL":
			self.ui.p3_absolute_DISP.display(self.steps2uL(calib[1,2],self.p3_syringe_area))
		if self.p3_units.split('/')[0]=="mL":
			self.ui.p3_absolute_DISP.display(self.steps2mL(calib[1,2],self.p3_syringe_area))
		if self.p3_units.split('/')[0]=="mm":
			self.ui.p3_absolute_DISP.display(self.steps2mm(calib[1,2],self.microstepping))
		if self.p1_units.split('/')[0]=="µL":
			self.ui.p1_absolute_DISP.display(self.steps2uL(calib[1,0],self.p1_syringe_area))
		if self.p1_units.split('/')[0]=="mL":
			self.ui.p1_absolute_DISP.display(self.steps2mL(calib[1,0],self.p1_syringe_area))
		if self.p1_units.split('/')[0]=="mm":
			self.ui.p1_absolute_DISP.display(self.steps2mm(calib[1,0],self.microstepping))

	
	def update_current_vol(self,currentSteps):
#		print (self.p1_units.split('/'))
#		print("Updating displays to:",calib[1,:])
#		calib=np.loadtxt("calibration.txt")
		
		if self.p1_units.split('/')[0]=="µL":
			self.ui.p1_curr_DISP.display(self.steps2uL(currentSteps[0],self.p1_syringe_area))
#			print("updating with:",self.steps2uL(currentSteps[0],self.p1_syringe_area))
		if self.p1_units.split('/')[0]=="mL":
			self.ui.p1_curr_DISP.display(self.steps2mL(currentSteps[0],self.p1_syringe_area))
		if self.p1_units.split('/')[0]=="mm":
			self.ui.p1_curr_DISP.display(self.steps2mm(currentSteps[0],self.microstepping))
		if self.p2_units.split('/')[0]=="µL":
			self.ui.p2_curr_DISP.display(self.steps2uL(currentSteps[1],self.p2_syringe_area))
		if self.p2_units.split('/')[0]=="mL":
			self.ui.p2_curr_DISP.display(self.steps2mL(currentSteps[1],self.p2_syringe_area))
		if self.p2_units.split('/')[0]=="mm":
			self.ui.p2_curr_DISP.display(self.steps2mm(currentSteps[1],self.microstepping))
		if self.p3_units.split('/')[0]=="µL":
			self.ui.p3_curr_DISP.display(self.steps2uL(currentSteps[2],self.p3_syringe_area))
		if self.p3_units.split('/')[0]=="mL":
			self.ui.p3_curr_DISP.display(self.steps2mL(currentSteps[2],self.p3_syringe_area))
		if self.p3_units.split('/')[0]=="mm":
			self.ui.p3_curr_DISP.display(self.steps2mm(currentSteps[2],self.microstepping))

	def update_p2_display(self,value):
		serl.ui.p2_absolute_DISP.display(vlue)

# 	def threadTest1 (self):
# 		
# 		for i in range (10):
# 			self.update_volume(2,i)
# 			print("Thread Test 1",i)
# 			time.sleep(0.2)
# 
# 	def threadTest2 (self):
# 		
# 		for i in range (10):
# 			self.update_volume(3,i)
# 			print("Thread Test 2",i)
# 			time.sleep(0.2)
	def runTest(self, td):
		print("TD", td)
		numLoops = len(td)
		waitingForReply = False
		n = 0
		teststr=[]

		while n < numLoops:
			teststr = td[n]
			print("Sending:",n+1,"of",numLoops,':',teststr)

			if waitingForReply == False:
				self.sendToArduino(teststr)
				print("Sent from PC -- " + teststr)
				waitingForReply = True

			if waitingForReply == True:
				print ("waiting")
				while self.serial.inWaiting() == 0:
#					print ("still waiting")
					pass

				dataRecvd = self.recvPositionArduino()
#				print ("Reply received")
				print("Reply Received -- " + dataRecvd)
				n += 1
# 				
				waitingForReply = False
# 
# 			time.sleep(0.1)

			
			
	def update_target(self,teststr):
		deltasteps=self.getSteps(teststr)
		calib=np.loadtxt("calibration.txt")
		calib[1,:]=calib[1,:]+deltasteps
		np.savetxt("calibration.txt",calib)
#			print("Zero:",calib[0,:])
#			print("Current steps:",calib[1,:])
#			self.ui.p1_absolute_DISP(calib[1,0])
		self.update_displays()
		return calib[1,:]

	def monitorMoves(self,targetSteps):
		stepsTogo=np.zeros(3)
		while self.serial.inWaiting()==0:
			pass			
		dataRecvd = self.recvPositionArduino()
		print(dataRecvd)
		pumpNum=int(dataRecvd.split("|")[1])
		tmp=int(dataRecvd.split("|")[2])
		stepsTogo[pumpNum]=tmp
		while abs(stepsTogo).sum() > 0:
			while self.serial.in_waiting==0:
				pass
			dataRecvd = self.recvPositionArduino()
			print(dataRecvd)
			pumpNum=int(dataRecvd.split("|")[1])
			tmp=int(dataRecvd.split("|")[2])
			stepsTogo[pumpNum]=tmp
#			print(pumpNum,stepsTogo[pumpNum])
			currentSteps=targetSteps-stepsTogo
#			print(stepsTogo)
#			print(currentSteps)
			self.update_current_vol(currentSteps)
			
			

		
#		print("Steps:",deltasteps)
		
	'''def auto_runTest(self, td, injection_number, latent_time):
		print("TD", td)
		numLoops = len(td)
		waitingForReply = False
		n = 0


		for i in range(injection_number):
			print(i)
			while n < numLoops:
				teststr = td[n]

				if waitingForReply == False:
					self.sendToArduino(teststr)
					print("Sent from PC -- " + teststr)
					waitingForReply = True

				if waitingForReply == True:

					while self.serial.inWaiting() == 0:
						pass

					dataRecvd = self.recvPositionArduino()
					print("Reply Received -- " + dataRecvd)
					n += 1
					waitingForReply = False

				time.sleep(0.1)
		time.sleep(latent_time)

		print("Send and receive complete\n\n")'''

	def send_single_command(self, command):
		waiting_for_reply = False
		if waiting_for_reply == False:
			self.sendToArduino(command)
			print("Sent from PC -- STR " + command)
			waiting_for_reply = True
		if waiting_for_reply == True:
			while self.serial.inWaiting() == 0:
				pass
			data_received = self.recvPositionArduino()
#			data_received = "from other func"
			print("Reply Received -- " + data_received)
			waiting_for_reply = False
			print("=============================\n\n")
			print("Sent a single command")


	def listening(self):
		startMarker = self.startMarker
		midMarker = self.midMarker
		endMarker = self.endMarker
		posMarker = ord('?')
		i = 0

		while (True):
			self.serial.flushInput()
			x = "z"
			ck = ""
			isDisplay = "asdf"
			while self.serial.inWaiting() == 0:
				pass
			while  not x or ord(x) != startMarker:
				x = self.serial.read()
				#if ord(x) == posMarker:
				#	return self.get_position()
			while ord(x) != endMarker:
				if ord(x) == midMarker:
					i += 1
#					print(ck)
					#isDisplay = ck
					#if i % 100 == 0:
					#	self.ui.p1_absolute_DISP.display(ck)
					ck = ""
					x = self.serial.read()

				if ord(x) != startMarker:
					ck = ck + x.decode()

				x = self.serial.read()
				# TODO
			#if isDisplay == "START":
			#	print("This is ck: " + ck)
				#motorID = int(ck)
				#self.is_p1_running = True
				#run thread(self.display_position, motorID)

				#toDisp = self.steps2mm(float(ck))
				#print("Pump num " + toDisp + " is now running.")i
				#self.ui.p1_absolute_DISP.display(toDisp)
				#isDisplay = ""

			#self.serial.flushInput()
			#print(self.serial.read(self.serial.inWaiting()).decode('ascii'))
#			print(ck)
#			print("\n")

	# TODO
	# def display_position(self, motorID):
	# 	if motorID == 1:

	# 		seconds = 0
	# 		p1_speed = self.p1_speed_to_send
	# 		p1_dist = 0
	# 		p1_time = p1_dist/p1_speed

	# 		time_start = time.start()
	# 		while self.is_p1_running:
	# 			pass



	def get_position(self):
		ck = ""
		x = self.serial.read()

		while ord(x) != self.endMarker:
			if ord(x) == self.midMarker:
#				print(ck)
				ck = ""
				x = self.serial.read()
			ck = ck + x.decode()
			x = self.serial.read()
#		print(ck)
		return (ck)



	def closeEvent(self, event):
		try:
			#self.global_listener_thread.stop()
			self.serial.close()
			#self.threadpool.end()

		except AttributeError:
			pass
		sys.exit()

# I feel better having one of these
def main():
	# a new app instance
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.setWindowTitle("Poseidon Pumps Controller - Pachter Lab Caltech 2018 - Juers Lab Whitman College 2025")
	window.show()
	# without this, the script exits immediately.
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
