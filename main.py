
##################################################
## This is Assignment I project of EH2745 Computer Applications in Power Systems
## It has purpose to CIM-XML modelling and parsing, storing data to MySQL Database, and 
## Build Y-Matrix
##################################################
## {2019, MIT License}
##################################################
## Author: Fahrur Rozzi, Ruoyu Xu
## Copyright: Copyright 2019, Assignment 1
## Credits: ["Lars Nordström", "Oscar Utterbäck", "Fahrur Rozzi", "Ruoyu Xu"]
## License: MIT License
## Version: 1.0.1
## Maintainer: Fahrur Rozzi, Ruoyu Xu 
## Email: fahrurrozzi18@gmail.com, seuruoyuxu@gmail.com
## Status: Production
##################################################

# Import Library
import xml.etree.ElementTree as ET
import cmath
import math
import numpy
import mysql.connector

from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import filedialog

# GUI of the application
root = Tk()
root.title("Assignment 1")
content = ttk.Frame(root)
frame = ttk.Frame(content, borderwidth=5, relief="sunken", width=100, height=100)
img = PhotoImage(file='KTH.png')
panel = ttk.Label(content, image=img)
content.grid(column=1, row=0)
frame.grid(column=1, row=0, columnspan=3, rowspan=2)
panel.grid(column=1, row=0, columnspan=3, rowspan=2)

# Insert File
def EQ_file():
    EQ_file = filedialog.askopenfilename()
    global EQ_file_XML, Message_EQ
    EQ_file_XML = EQ_file
    Message_EQ = "Successfully added EQ File"

def SSH_file():
    SSH_file = filedialog.askopenfilename()
    global SSH_file_XML, Message_SSQ
    SSH_file_XML = SSH_file
    Message_SSH = "Successfully added SSH File"

# GUI Layout
Button_EQ = Button(root, text="Import EQ File", command=EQ_file)
Button_EQ.grid(column=1, row=3, sticky='nesw')
Button_SSH = Button(root, text="Import SSH File", command=SSH_file)
Button_SSH.grid(column=1, row=4, sticky='nesw')
Button_Run = Button(root, text="Run", command=root.destroy)
Button_Run.grid(column=1, row=5,sticky='nesw')

root.mainloop()



# For parsing the data EQ and SSH file
tree_EQ = ET.parse(EQ_file_XML)
tree_SSH = ET.parse(SSH_file_XML)
root_EQ = tree_EQ.getroot()
root_SSH = tree_SSH.getroot()

cim = "{http://iec.ch/TC57/2013/CIM-schema-cim16#}"
md = "{http://iec.ch/TC57/61970-552/ModelDescription/1#}"
rdf = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"

# Class definition of CIM Objects
class base_voltage:
  def __init__(self, rdf_ID, nominal_value):
    self.rdf_ID = rdf_ID
    self.nominal_value = nominal_value


class substation:
  def __init__(self, rdf_ID,
  name, region_rdf_ID):
    self.rdf_ID = rdf_ID
    self.name = name
    self.region_rdf_ID = region_rdf_ID


class voltage_level:
  def __init__(self, rdf_ID, name, substation_rdf_ID, base_voltage_rdf_ID):
    self.rdf_ID = rdf_ID
    self.name = name
    self.substation_rdf_ID = substation_rdf_ID
    self.base_voltage_rdf_ID = base_voltage_rdf_ID


class generating_unit:
   def __init__(self, rdf_ID, name, max_P, min_P,  equipment_container_rdf_ID):
    self.rdf_ID = rdf_ID
    self.name = name
    self.max_P = max_P
    self.min_P = min_P
    self.equipment_container_rdf_ID = equipment_container_rdf_ID


class synchronous_machine:
  def __init__(self, rdf_ID, name, rated_S, active_power, reactive_power,
  generator_unit_rdf_ID, reg_control_rdf_ID, equipment_container_rdf_ID,
  base_voltage_rdf_ID):
    self.rdf_ID = rdf_ID
    self.name = name
    self.rated_S = rated_S
    self.active_power = active_power
    self.reactive_power = reactive_power
    self.generator_unit_rdf_ID = generator_unit_rdf_ID
    self.reg_control_rdf_ID = reg_control_rdf_ID
    self.equipment_container_rdf_ID = equipment_container_rdf_ID
    self.base_voltage_rdf_ID = base_voltage_rdf_ID
    self.admittance = 0

class regulating_control:
  def __init__(self, rdf_ID, name, target_value):
    self.rdf_ID = rdf_ID
    self.name = name
    self.target_value = target_value


class power_transformer:
  def __init__(self, rdf_ID, name, equipment_container_rdf_ID):
    self.rdf_ID = rdf_ID
    self.name = name
    self.equipment_container_rdf_ID = equipment_container_rdf_ID

    self.transformer_r = 0
    self.transformer_x = 0
    self.base_voltage_value = 0
    self.admittance_value = 0
    self.b = 0
    self.g = 0


class energy_consumer_load:
  def __init__(self, rdf_ID, name, active_power, reactive_power,
  equipment_container_rdf_ID, base_voltage_rdf_ID):
    self.rdf_ID = rdf_ID
    self.name = name
    self.active_power = active_power
    self.reactive_power = reactive_power
    self.equipment_container_rdf_ID = equipment_container_rdf_ID
    self.base_voltage_rdf_ID = base_voltage_rdf_ID

    self.admittance = 0


class power_transformer_end_transformer_winding:
  def __init__(self, rdf_ID, name, transformer_r, transformer_x,
  transformer_rdf_ID, base_voltage_rdf_ID, b, g):
    self.rdf_ID = rdf_ID
    self.name = name
    self.transformer_r = transformer_r
    self.transformer_x = transformer_x
    self.transformer_rdf_ID = transformer_rdf_ID
    self.base_voltage_rdf_ID = base_voltage_rdf_ID
    self.b = b
    self.g = g


class breaker:
  def __init__(self, rdf_ID, name, state, equipment_container_rdf_ID,
  base_voltage_rdf_ID):
    self.rdf_ID = rdf_ID
    self.name = name
    self.state = state
    self.equipment_container_rdf_ID = equipment_container_rdf_ID
    self.base_voltage_rdf_ID = base_voltage_rdf_ID

    self.admittance = 0


class ratio_tap_changer:
  def __init__(self, rdf_ID, name, step):
    self.rdf_ID = rdf_ID
    self.name = name
    self.step = step

# ==========================
# Class for bus branch model and Y calculation


class AC_line_segment:
  def __init__(self, rdf_ID, name, equipment_container_rdf_ID, ACLineSegment_r,
  ACLineSegment_x, bch, gch, length, base_voltage_rdf_ID):
    self.rdf_ID = rdf_ID
    self.name = name
    self.equipment_container_rdf_ID = equipment_container_rdf_ID
    self.ACLineSegment_r = ACLineSegment_r
    self.ACLineSegment_x = ACLineSegment_x
    self.bch = bch
    self.gch = gch
    self.length = length
    self.base_voltage_rdf_ID = base_voltage_rdf_ID

    self.ACLineSegment_r_value = 0
    self.ACLineSegment_x_value = 0
    self.bch_value = 0
    self.gch_value = 0
    self.length_value = 0
    self.admittance = 0
    self.shunt_admittance = 0
    self.base_voltage_value = 0


class busbar_section:
  def __init__(self, rdf_ID, name, equipment_container_rdf_ID, base_voltage_rdf_ID):
    self.rdf_ID = rdf_ID
    self.name = name
    self.equipment_container_rdf_ID = equipment_container_rdf_ID
    self.base_voltage_rdf_ID = base_voltage_rdf_ID


class linear_shunt_compensator:
  def __init__(self, rdf_ID, name,  b_per_section, g_per_section,
  equipment_container_rdf_ID, base_voltage_rdf_ID, base_voltage_value):
    self.rdf_ID = rdf_ID
    self.name = name
    self.b_per_section = b_per_section
    self.g_per_section = g_per_section
    self.equipment_container_rdf_ID = equipment_container_rdf_ID
    self.base_voltage_rdf_ID = base_voltage_rdf_ID
    self.base_voltage_value = base_voltage_value

    self.admittance = 0


class connectivity_node:
  def __init__(self, rdf_ID, name):
    self.rdf_ID = rdf_ID
    self.name = name
    self.count_terminal = 0


class terminal:
  def __init__(self, rdf_ID, name, CE_rdf_ID, CN_rdf_ID):
    self.rdf_ID = rdf_ID
    self.name = name
    self.CE_rdf_ID = CE_rdf_ID
    self.CN_rdf_ID = CN_rdf_ID
    self.traversal_flag = "Not Yet Pass"


class conducting_equipment:
  def __init__(self, rdf_ID, name):
    self.rdf_ID = rdf_ID
    self.name = name


# ==================================
# Initialization list

# Class List

base_voltage_list = []
substation_list = []
voltage_level_list = []
generating_unit_list = []
synchronous_machine_list = []
regulating_control_list = []
power_transformer_list = []
energy_consumer_load_list = []
power_transformer_end_transformer_winding_list = []
breaker_list = []
ratio_tap_changer_list = []

AC_line_segment_list = []
busbar_section_list = []
linear_shunt_compensator_list = []
connectivity_node_list = []
terminal_list = []
conducting_equipment_list = []


# Find base voltage from XML
# print('\nBase Voltage')
for base_voltage_xml in root_EQ.iter(cim+'BaseVoltage'):
  base_voltage_list.append(base_voltage(base_voltage_xml.get(
      rdf+'ID'), base_voltage_xml.find(cim+'BaseVoltage.nominalVoltage').text))

# Find substation from XML
# print('\nSubstation')
for substation_xml in root_EQ.iter(cim+'Substation'):
  substation_list.append(substation(substation_xml.get(rdf+'ID'), substation_xml.find(
      cim+'IdentifiedObject.name').text, substation_xml.find(cim+'Substation.Region').get(rdf+'resource')))

# Find voltage level from XML
# print('\nVoltage Level')
for voltage_level_xml in root_EQ.iter(cim+'VoltageLevel'):
  voltage_level_list.append(voltage_level(voltage_level_xml.get(rdf+'ID'), voltage_level_xml.find(cim+'IdentifiedObject.name').text,
  voltage_level_xml.find(cim+'VoltageLevel.Substation').get(rdf+'resource'),
  voltage_level_xml.find(cim+'VoltageLevel.BaseVoltage').get(rdf+'resource')))

# Find Generating Unit from XML
# print('\nGenerating Unit')
for generating_unit_xml in root_EQ.iter(cim+'GeneratingUnit'):
  generating_unit_list.append(generating_unit(generating_unit_xml.get(rdf+'ID'), generating_unit_xml.find(cim+'IdentifiedObject.name').text,
  generating_unit_xml.find(cim+'GeneratingUnit.maxOperatingP').text, generating_unit_xml.find(
      cim+'GeneratingUnit.minOperatingP').text,
  generating_unit_xml.find(cim+'Equipment.EquipmentContainer').get(rdf+'resource')))

# Find Synchronous Machine from XML
# print('\nSynchronous Machine')
for synchronous_machine_xml in root_EQ.iter(cim+'SynchronousMachine'):
  synchronous_machine_list.append(synchronous_machine(synchronous_machine_xml.get(rdf+'ID'), synchronous_machine_xml.find(cim+'IdentifiedObject.name').text,
  synchronous_machine_xml.find(cim+'RotatingMachine.ratedS').text, "", "", synchronous_machine_xml.find(
      cim+'RotatingMachine.GeneratingUnit').get(rdf+'resource'),
  synchronous_machine_xml.find(
      cim+'RegulatingCondEq.RegulatingControl').get(rdf+'resource'),
  synchronous_machine_xml.find(cim+'Equipment.EquipmentContainer').get(rdf+'resource'), ""))

count_ssh = 0
for synchronous_machine_xml in root_SSH.iter(cim+'SynchronousMachine'):
  synchronous_machine_list[count_ssh].active_power = synchronous_machine_xml.find(
      cim+'RotatingMachine.p').text
  synchronous_machine_list[count_ssh].reactive_power = synchronous_machine_xml.find(
      cim+'RotatingMachine.q').text
  count_ssh += 1

# Find Regulating Control from XML
# print('\nRegulating Control')
for regulating_control_xml in root_EQ.iter(cim+'RegulatingControl'):
  regulating_control_list.append(regulating_control(regulating_control_xml.get(
      rdf+'ID'), regulating_control_xml.find(cim+'IdentifiedObject.name').text, ""))

count_ssh = 0
for regulating_control_xml in root_SSH.iter(cim+'RegulatingControl'):
  regulating_control_list[count_ssh].target_value = regulating_control_xml.find(
      cim+'RegulatingControl.targetValue').text
  count_ssh += 1

# Find Power Transformer from XML
# print('\nPower Transformer')
for power_transformer_xml in root_EQ.iter(cim+'PowerTransformer'):
  power_transformer_list.append(power_transformer(power_transformer_xml.get(rdf+'ID'), power_transformer_xml.find(cim+'IdentifiedObject.name').text,
  power_transformer_xml.find(cim+'Equipment.EquipmentContainer').get(rdf+'resource')))

# Find Energy Consumer Load from XML
# print('\nEnergy Consumer (Load)')
for energy_consumer_load_xml in root_EQ.iter(cim+'EnergyConsumer'):
  energy_consumer_load_list.append(energy_consumer_load(energy_consumer_load_xml.get(rdf+'ID'), energy_consumer_load_xml.find(cim+'IdentifiedObject.name').text, "", "",
  energy_consumer_load_xml.find(cim+'Equipment.EquipmentContainer').get(rdf+'resource'), ""))

count_ssh = 0
for energy_consumer_load_xml in root_SSH.iter(cim+'EnergyConsumer'):
  energy_consumer_load_list[count_ssh].active_power = energy_consumer_load_xml.find(
      cim+'EnergyConsumer.p').text
  energy_consumer_load_list[count_ssh].reactive_power = energy_consumer_load_xml.find(
      cim+'EnergyConsumer.q').text
  count_ssh += 1
# Base voltage rdf id for enernt.EquipmentContainer").item(0);y consumer (load) not yet!!!

# Find Power Transformer End (nt.EquipmentContainer").item(0);ransformer winding) from XML
# print('\nPower Transformer End (Transformer Winding)')
for power_transformer_end_transformer_winding_xml in root_EQ.iter(cim+'PowerTransformerEnd'):
  power_transformer_end_transformer_winding_list.append(power_transformer_end_transformer_winding(power_transformer_end_transformer_winding_xml.get(rdf+'ID'),
  power_transformer_end_transformer_winding_xml.find(
      cim+'IdentifiedObject.name').text, power_transformer_end_transformer_winding_xml.find(cim+'PowerTransformerEnd.r').text,
  power_transformer_end_transformer_winding_xml.find(
      cim+'PowerTransformerEnd.x').text, power_transformer_end_transformer_winding_xml.find(cim+'PowerTransformerEnd.PowerTransformer').get(rdf+'resource'),
  power_transformer_end_transformer_winding_xml.find(cim+'TransformerEnd.BaseVoltage').get(rdf+'resource'), 
  power_transformer_end_transformer_winding_xml.find(cim+'PowerTransformerEnd.b').text, 
  power_transformer_end_transformer_winding_xml.find(cim+'PowerTransformerEnd.g').text))

# Find breaker from XML
# print('\nBreaker')
for breaker_xml in root_EQ.iter(cim+'Breaker'):
  breaker_list.append(breaker(breaker_xml.get(rdf+'ID'), breaker_xml.find(cim+'IdentifiedObject.name').text,
                      "", breaker_xml.find(cim+'Equipment.EquipmentContainer').get(rdf+'resource'), ""))

count_ssh = 0
for breaker_xml in root_SSH.iter(cim+'Breaker'):
  breaker_list[count_ssh].state = breaker_xml.find(cim+'Switch.open').text
  count_ssh += 1
# Base voltage rdf id for Breaker not yet!!!

# Find ratio tap changer from XML
# print('\nRatio Tap Changer')
for ratio_tap_changer_xml in root_EQ.iter(cim+'RatioTapChanger'):
  ratio_tap_changer_list.append(ratio_tap_changer(ratio_tap_changer_xml.get(
      rdf+'ID'), ratio_tap_changer_xml.find(cim+'IdentifiedObject.name').text, ""))

count_ssh = 0
for ratio_tap_changer_xml in root_SSH.iter(cim+'RatioTapChanger'):
  ratio_tap_changer_list[count_ssh].step = ratio_tap_changer_xml.find(
      cim+'TapChanger.step').text
  count_ssh += 1

# Find connectivity node from XML
# print('\nConnectivity Node')
for connectivity_node_xml in root_EQ.iter(cim+'ConnectivityNode'):
  connectivity_node_list.append(connectivity_node(connectivity_node_xml.get(
      rdf+'ID'), connectivity_node_xml.find(cim+'IdentifiedObject.name').text))

# Find terminal from XML
# print('\nTerminal')
for terminal_xml in root_EQ.iter(cim+'Terminal'):
  terminal_list.append(terminal(terminal_xml.get(rdf+'ID'), terminal_xml.find(cim+'IdentifiedObject.name').text, terminal_xml.find(cim+'Terminal.ConductingEquipment').get(rdf+'resource'),
  terminal_xml.find(cim+'Terminal.ConnectivityNode').get(rdf+'resource')))

# Find AC Line Segment from XML
# print('\nAC Line Segment')
for AC_line_segment_xml in root_EQ.iter(cim+'ACLineSegment'):
  AC_line_segment_list.append(AC_line_segment(AC_line_segment_xml.get(rdf+'ID'), AC_line_segment_xml.find(cim+'IdentifiedObject.name').text, AC_line_segment_xml.find(cim+'Equipment.EquipmentContainer').get(rdf+'resource'),
  AC_line_segment_xml.find(cim+'ACLineSegment.r').text, AC_line_segment_xml.find(cim+'ACLineSegment.x').text, AC_line_segment_xml.find(
      cim+'ACLineSegment.bch').text, AC_line_segment_xml.find(cim+'ACLineSegment.gch').text,
  AC_line_segment_xml.find(cim+'Conductor.length').text, AC_line_segment_xml.find(cim+'ConductingEquipment.BaseVoltage').get(rdf+'resource')))

# Find Busbar Section from XML
# print('\nBusbar Section')
for busbar_section_xml in root_EQ.iter(cim+'BusbarSection'):
  busbar_section_list.append(busbar_section(busbar_section_xml.get(rdf+'ID'), busbar_section_xml.find(
      cim+'IdentifiedObject.name').text, busbar_section_xml.find(cim+'Equipment.EquipmentContainer').get(rdf+'resource'), ""))

# Find Linear Shunt Compensator from XML
# print('\nLinear Shunt Compensator')
for linear_shunt_compensator_xml in root_EQ.iter(cim+'LinearShuntCompensator'):
  linear_shunt_compensator_list.append(linear_shunt_compensator(linear_shunt_compensator_xml.get(rdf+'ID'), linear_shunt_compensator_xml.find(cim+'IdentifiedObject.name').text, linear_shunt_compensator_xml.find(cim+'LinearShuntCompensator.bPerSection').text,
  linear_shunt_compensator_xml.find(cim+'LinearShuntCompensator.gPerSection').text, linear_shunt_compensator_xml.find(cim+'Equipment.EquipmentContainer').get(rdf+'resource'), "", 
  linear_shunt_compensator_xml.find(cim+'ShuntCompensator.nomU').text))

# print('\n')

# Generating Conducting Equipment List

for i in range(len(synchronous_machine_list)):
  conducting_equipment_list.append(conducting_equipment(
   synchronous_machine_list[i].rdf_ID, synchronous_machine_list[i].name))

for i in range(len(power_transformer_list)):
  conducting_equipment_list.append(conducting_equipment(
      power_transformer_list[i].rdf_ID, power_transformer_list[i].name))

for i in range(len(energy_consumer_load_list)):
  conducting_equipment_list.append(conducting_equipment(
      energy_consumer_load_list[i].rdf_ID, energy_consumer_load_list[i].name))

for i in range(len(breaker_list)):
  conducting_equipment_list.append(conducting_equipment(
      breaker_list[i].rdf_ID, breaker_list[i].name))

for i in range(len(AC_line_segment_list)):
  conducting_equipment_list.append(conducting_equipment(
      AC_line_segment_list[i].rdf_ID, AC_line_segment_list[i].name))

for i in range(len(busbar_section_list)):
  conducting_equipment_list.append(conducting_equipment(
      busbar_section_list[i].rdf_ID, busbar_section_list[i].name))

for i in range(len(linear_shunt_compensator_list)):
  conducting_equipment_list.append(conducting_equipment(
      linear_shunt_compensator_list[i].rdf_ID, linear_shunt_compensator_list[i].name))

# Finding base voltage
for i in range(len(synchronous_machine_list)):
  buff_rdf_ID = synchronous_machine_list[i].equipment_container_rdf_ID
  buff_rdf_ID = buff_rdf_ID.replace("#", "")
  for j in range(len(voltage_level_list)):
    if buff_rdf_ID == voltage_level_list[j].rdf_ID:
      buff_base_voltage_ID = voltage_level_list[j].base_voltage_rdf_ID
      buff_base_voltage_ID = buff_base_voltage_ID.replace("#", "")
      for k in range(len(base_voltage_list)):
        if buff_base_voltage_ID == base_voltage_list[k].rdf_ID:
          synchronous_machine_list[i].base_voltage_rdf_ID = "#" + \
              base_voltage_list[k].rdf_ID
# print('\n')

for i in range(len(energy_consumer_load_list)):
  buff_rdf_ID = energy_consumer_load_list[i].equipment_container_rdf_ID
  buff_rdf_ID = buff_rdf_ID.replace("#", "")
  for j in range(len(voltage_level_list)):
    if buff_rdf_ID == voltage_level_list[j].rdf_ID:
      buff_base_voltage_ID = voltage_level_list[j].base_voltage_rdf_ID
      buff_base_voltage_ID = buff_base_voltage_ID.replace("#", "")
      for k in range(len(base_voltage_list)):
        if buff_base_voltage_ID == base_voltage_list[k].rdf_ID:
          energy_consumer_load_list[i].base_voltage_rdf_ID = "#" + \
              base_voltage_list[k].rdf_ID
# print('\n')

for i in range(len(breaker_list)):
  buff_rdf_ID = breaker_list[i].equipment_container_rdf_ID
  buff_rdf_ID = buff_rdf_ID.replace("#", "")
  for j in range(len(voltage_level_list)):
    if buff_rdf_ID == voltage_level_list[j].rdf_ID:
      buff_base_voltage_ID = voltage_level_list[j].base_voltage_rdf_ID
      buff_base_voltage_ID = buff_base_voltage_ID.replace("#", "")
      for k in range(len(base_voltage_list)):
        if buff_base_voltage_ID == base_voltage_list[k].rdf_ID:
          breaker_list[i].base_voltage_rdf_ID = "#"+base_voltage_list[k].rdf_ID




# Get Energy Consumer list
energy_consumer_load_rdf_ID_list=[]
for i in range(len(energy_consumer_load_list)):
    energy_consumer_load_rdf_ID_list.append(energy_consumer_load_list[i].rdf_ID)

# Get Synchronous Machine list
synchronous_machine_rdf_ID_list=[]
for i in range(len(synchronous_machine_list)):
    synchronous_machine_rdf_ID_list.append(synchronous_machine_list[i].rdf_ID)

# Get Linear Shunt Compensator List
linear_shunt_compensator_rdf_ID_list=[]
for i in range(len(linear_shunt_compensator_list)):
  linear_shunt_compensator_rdf_ID_list.append(linear_shunt_compensator_list[i].rdf_ID)

# Get Open Breaker 
breaker_open_rdf_ID_list=[]
for i in range(len(breaker_list)):
  if breaker_list[i].state == "true" :
    breaker_open_rdf_ID_list.append(breaker_list[i].rdf_ID)

# Get Breaker List
breaker_rdf_ID_list = []
for i in range(len(breaker_list)):
  breaker_rdf_ID_list.append(breaker_list[i].rdf_ID)


#============================================
# Alghorithm for network traversal
# Initialization

CN_stack = []
CN_rdf_ID_stack = []
CN_stack_list = []
CN_rdf_ID_stack_list = []

CE_stack = []
CE_stack_list = []
CE_rdf_ID_stack = []
CE_rdf_ID_stack_list = []

all_stack = []
all_stack_list = []
all_rdf_ID_stack = []
all_rdf_ID_stack_list = []

CN_related_to_busbar = {}


# Step 1
# Select the starting node
start_node = terminal_list[0]

# Initialize the current node
previous_node_ID = ""
previous_node_type = ""
current_node = start_node
current_node_ID = current_node.rdf_ID
current_node_type="terminal"
next_node_type = ""

# Step 2
# Function to find the next node
def find_next_node(prev_node_rdf_ID, curr_node_rdf_ID, previous_node_type, current_node_type):
  next_node_rdf_ID = ""
  current_node_name = ""
  next_node_type = ""
# If the current node is CE
# Next node is terminal
  if current_node_type == "conducting equipment":
    for i in range(len(conducting_equipment_list)):
        if curr_node_rdf_ID == conducting_equipment_list[i].rdf_ID:
            for j in range(len(terminal_list)):
                if curr_node_rdf_ID == terminal_list[j].CE_rdf_ID.replace("#", "") and terminal_list[j].traversal_flag == "Not Yet Pass":
                    next_node_type = "terminal"
                    next_node_rdf_ID = terminal_list[j].rdf_ID
                    return next_node_rdf_ID, next_node_type 
    
# If the current node is CN
# Next node is terminal
  if current_node_type == "connectivity node":
    for k in range(len(connectivity_node_list)):
        if curr_node_rdf_ID == connectivity_node_list[k].rdf_ID:
            for j in range(len(terminal_list)):
                if curr_node_rdf_ID == terminal_list[j].CN_rdf_ID.replace("#", "") and terminal_list[j].traversal_flag == "Not Yet Pass":
                    next_node_rdf_ID = terminal_list[j].rdf_ID
                    next_node_type = "terminal"
                    return next_node_rdf_ID, next_node_type

# If the current node is terminal and previous is CE
# Next node is CN and Vice versa
  if current_node_type == "terminal" and previous_node_type == "conducting equipment":  
    for l in range(len(terminal_list)):
        if curr_node_rdf_ID == terminal_list[l].rdf_ID:
            for j in range(len(conducting_equipment_list)):
                if prev_node_rdf_ID == conducting_equipment_list[j].rdf_ID or prev_node_rdf_ID == "":
                    for m in range(len(connectivity_node_list)):
                        if connectivity_node_list[m].rdf_ID == terminal_list[l].CN_rdf_ID.replace("#", ""):
                            next_node_rdf_ID = connectivity_node_list[m].rdf_ID
                            next_node_type = "connectivity node"
                            return next_node_rdf_ID, next_node_type

  if current_node_type == "terminal" and previous_node_type == "connectivity node":
    for n in range(len(terminal_list)):
        if curr_node_rdf_ID == terminal_list[n].rdf_ID:
            for j in range(len(connectivity_node_list)):
                if prev_node_rdf_ID == connectivity_node_list[j].rdf_ID:
                    for m in range(len(conducting_equipment_list)):
                        if conducting_equipment_list[m].rdf_ID == terminal_list[n].CE_rdf_ID.replace("#", ""):
                            next_node_rdf_ID = conducting_equipment_list[m].rdf_ID
                            next_node_type = "conducting equipment"
                            return next_node_rdf_ID, next_node_type


# Get terminal ID attached to busbar and busbar ID
terminal_attached_busbar_list=[]
busbar_section_rdf_id_list=[]
for i in range(len(busbar_section_list)):
  busbar_section_rdf_id_list.append(busbar_section_list[i].rdf_ID)
  for j in range(len(terminal_list)):
    if busbar_section_list[i].rdf_ID == terminal_list[j].CE_rdf_ID.replace("#", ""):
      terminal_attached_busbar_list.append(terminal_list[j])

terminal_attached_busbar_rdf_ID_list = []
for i in range(len(terminal_attached_busbar_list)):
  terminal_attached_busbar_rdf_ID_list.append(terminal_attached_busbar_list[i].rdf_ID)
  

# Step 3
# Find the CN attached to busbar
connectivity_node_attached_to_busbar_rdf_ID_list = []
for i in range(len(terminal_attached_busbar_list)):
    connectivity_node_attached_to_busbar_rdf_ID_list.append(terminal_attached_busbar_list[i].CN_rdf_ID.replace("#",""))

# looping through the CN that attached to busbar
for i in range(len(connectivity_node_attached_to_busbar_rdf_ID_list)):
  CN_related_to_busbar[connectivity_node_attached_to_busbar_rdf_ID_list[i]]=i   
  # Find the terminal connected to CN that attached to busbar
  for j in range(len(terminal_list)):
    previous_node_ID = terminal_attached_busbar_list[i].rdf_ID
    current_node_ID = connectivity_node_attached_to_busbar_rdf_ID_list[i]
    previous_node_type = "terminal"
    current_node_type = "connectivity node"
    if terminal_list[j].CN_rdf_ID.replace("#", "") == current_node_ID and terminal_list[j].traversal_flag == "Not Yet Pass":
      for ii in range(len(terminal_list)):
        if previous_node_ID == terminal_list[ii].rdf_ID:
            terminal_list[ii].traversal_flag = "Pass"
      count_terminal_connected_to_connectivy_node_busbar = 0
      for lll in range(len(terminal_list)):
        if current_node_ID == terminal_list[lll].CN_rdf_ID.replace("#", ""):
          if terminal_list[lll].traversal_flag == "Not Yet Pass":
            count_terminal_connected_to_connectivy_node_busbar += 1
      
      if count_terminal_connected_to_connectivy_node_busbar == 0:
        # print ("No More Terminal")
        print("")
      if count_terminal_connected_to_connectivy_node_busbar != 0 :
        next_node_ID, next_node_type  = find_next_node(previous_node_ID, current_node_ID, previous_node_type, current_node_type)
        all_stack.extend(['start busbar '+ str(i), previous_node_type, current_node_type, next_node_type])
        CN_stack.extend(['start busbar '+ str(i), current_node_type])
        CE_stack.append('start busbar '+ str(i))

        all_rdf_ID_stack.extend([busbar_section_rdf_id_list[i], previous_node_ID, current_node_ID, next_node_ID])
        CN_rdf_ID_stack.extend([busbar_section_rdf_id_list[i], current_node_ID])
        CE_rdf_ID_stack.append(busbar_section_rdf_id_list[i])
    
        while next_node_ID not in connectivity_node_attached_to_busbar_rdf_ID_list:   
          if current_node_type == "terminal":
              if(next_node_type == "connectivity node"):
                  if next_node_ID in terminal_attached_busbar_rdf_ID_list:
                      print('Final Terminal')
                  else:
                      previous_node_ID = current_node_ID
                      previous_node_type = current_node_type
                      current_node_ID = next_node_ID
                      current_node_type = next_node_type
                      CN_stack.append(current_node_type)
                      CN_rdf_ID_stack.append(current_node_ID)
                      for iii in range(len(terminal_list)):
                          if previous_node_ID == terminal_list[iii].rdf_ID:
                              terminal_list[iii].traversal_flag = "Pass"
                      next_node_ID, next_node_type  = find_next_node(previous_node_ID, current_node_ID, previous_node_type, current_node_type)
                      all_stack.append(next_node_type)
                      all_rdf_ID_stack.append(next_node_ID)                

              if(next_node_type == "conducting equipment"):
                  if next_node_ID in terminal_attached_busbar_rdf_ID_list:
                      print('Final Terminal')
                  else:
                      previous_node_ID = current_node_ID
                      previous_node_type = current_node_type
                      current_node_ID = next_node_ID
                      current_node_type = next_node_type
                      if current_node_ID in breaker_rdf_ID_list :
                        CE_stack.extend([current_node_type, "Breaker"])
                      else:
                        CE_stack.append(current_node_type)
                      CE_rdf_ID_stack.append(current_node_ID)
                      for iiii in range(len(terminal_list)):
                          if previous_node_ID == terminal_list[iiii].rdf_ID:
                              terminal_list[iiii].traversal_flag = "Pass"
                      if current_node_ID in energy_consumer_load_rdf_ID_list :
                          # print("Energy Consumer Branch")
                          CE_stack.append("Energy Consumer")
                          break
                      elif current_node_ID in synchronous_machine_rdf_ID_list:
                          # print("Synchronous Machine Branch ")
                          CE_stack.append("Synchronous Machine")                    
                          break
                      elif current_node_ID in linear_shunt_compensator_rdf_ID_list:
                          # print("Linear Compensator Branch")
                          CE_stack.append("Linear Shunt Compensator")
                          break
                      elif current_node_ID in breaker_open_rdf_ID_list:
                          print("Breaker Open Branch")
                          CE_stack.append("Open Breaker")
                          break
                      else:
                          next_node_ID, next_node_type  = find_next_node(previous_node_ID, current_node_ID, previous_node_type, current_node_type)
                      all_stack.append(next_node_type)
                      all_rdf_ID_stack_list.append(next_node_ID)
          if current_node_type == "connectivity node":
              for ij in range(len(terminal_list)):
                  if current_node_ID == terminal_list[ij].CN_rdf_ID.replace("#","") and terminal_list[ij].traversal_flag == "Not Yet Pass":
                      for ijk in range(len(connectivity_node_list)):
                          if current_node_ID == connectivity_node_list[ijk].rdf_ID:
                              connectivity_node_list[ijk].count_terminal += 1

                      previous_node_ID = current_node_ID
                      previous_node_type = current_node_type
                      current_node_ID = next_node_ID
                      current_node_type = next_node_type
                      
                      next_node_ID, next_node_type  = find_next_node(previous_node_ID, current_node_ID, previous_node_type, current_node_type)
                      all_stack.append(next_node_type)
                      all_rdf_ID_stack.append(next_node_ID)


          if current_node_type == "conducting equipment" :
              for ijjk in range(len(terminal_list)):
                  if current_node_ID == terminal_list[ijjk].CE_rdf_ID.replace("#","") and terminal_list[ijjk].traversal_flag == "Not Yet Pass":
                      previous_node_ID = current_node_ID
                      previous_node_type = current_node_type
                      current_node_ID = next_node_ID
                      current_node_type = next_node_type
                      next_node_ID, next_node_type  = find_next_node(previous_node_ID, current_node_ID, previous_node_type, current_node_type)
                      all_stack.append(next_node_type)
                      all_rdf_ID_stack.append(next_node_ID)
                      if next_node_ID in connectivity_node_attached_to_busbar_rdf_ID_list:
                        for l in range(len(connectivity_node_attached_to_busbar_rdf_ID_list)):
                          if next_node_ID == connectivity_node_attached_to_busbar_rdf_ID_list[l]:
                            all_stack.append("End Busbar "+ str(l))
                            CE_stack.append("End Busbar "+ str(l))
                            CN_stack.append("End Busbar "+ str(l))
                            all_rdf_ID_stack.append(busbar_section_rdf_id_list[l])
                            CE_rdf_ID_stack.append(busbar_section_rdf_id_list[l])
                            CN_rdf_ID_stack.append(busbar_section_rdf_id_list[l])
                        for iiijjjkkk in range(len(terminal_list)):
                          if current_node_ID == terminal_list[iiijjjkkk].rdf_ID:
                              terminal_list[iiijjjkkk].traversal_flag = "Pass"

      all_stack_list.append(all_stack)
      CN_stack_list.append(CN_stack)
      CE_stack_list.append(CE_stack)

      all_rdf_ID_stack_list.append(all_rdf_ID_stack)
      CN_rdf_ID_stack_list.append(CN_rdf_ID_stack)
      CE_rdf_ID_stack_list.append(CE_rdf_ID_stack)

      CN_stack = []
      all_stack = [] 
      CE_stack = []
      all_rdf_ID_stack = []
      CN_rdf_ID_stack = []
      CE_rdf_ID_stack = []


# Check the remaining terminal 
for i in range(len(terminal_list)):
  if terminal_list[i].traversal_flag == "Not Yet Pass":
    print("There is still terminal remaining")


# Calculate the Admittance for every conducting equipment
S_base = 1000

# Initialize Y Matrix
Y_bus_matrix = numpy.zeros((len(connectivity_node_attached_to_busbar_rdf_ID_list), len(connectivity_node_attached_to_busbar_rdf_ID_list)),dtype=numpy.complex_)

# Power Transformer admittance
for i in range(len(power_transformer_list)):
  for ii in range(len(power_transformer_end_transformer_winding_list)):
    if power_transformer_end_transformer_winding_list[ii].transformer_rdf_ID.replace("#","") == power_transformer_list[i].rdf_ID:
      if float(power_transformer_end_transformer_winding_list[ii].transformer_r) == 0 and float(power_transformer_end_transformer_winding_list[ii].transformer_x) == 0 : 
        print("")
      else:
        power_transformer_list[i].transformer_r += float(power_transformer_end_transformer_winding_list[ii].transformer_r)
        power_transformer_list[i].transformer_x += float(power_transformer_end_transformer_winding_list[ii].transformer_x)
        power_transformer_list[i].b += float(power_transformer_end_transformer_winding_list[ii].b)
        power_transformer_list[i].g += float(power_transformer_end_transformer_winding_list[ii].g)
        for iij in range(len(base_voltage_list)):
          if power_transformer_end_transformer_winding_list[ii].base_voltage_rdf_ID.replace("#","") == base_voltage_list[iij].rdf_ID:
            power_transformer_list[i].base_voltage_value = float(base_voltage_list[iij].nominal_value)

for i in range(len(power_transformer_list)):
  power_transformer_complex = complex(power_transformer_list[i].transformer_r, power_transformer_list[i].transformer_x)
  # power_transformer_complex_2 = complex(power_transformer_list[i].g, power_transformer_list[i].b)
  power_transformer_complex_2 = 0
  power_transformer_list[i].admittance_value = ((1/power_transformer_complex)-power_transformer_complex_2)*pow(power_transformer_list[i].base_voltage_value, 2)/S_base


# AC Line Segment Admittance
for i in range(len(AC_line_segment_list)):
  for ii in range(len(base_voltage_list)):
    if AC_line_segment_list[i].base_voltage_rdf_ID.replace("#","") == base_voltage_list[ii].rdf_ID:
      AC_line_segment_list[i].base_voltage_value = float(base_voltage_list[ii].nominal_value)
  AC_line_segment_list[i].ACLineSegment_r_value = float(AC_line_segment_list[i].ACLineSegment_r)
  AC_line_segment_list[i].ACLineSegment_x_value = float(AC_line_segment_list[i].ACLineSegment_x)
  AC_line_segment_list[i].bch_value = float(AC_line_segment_list[i].bch)
  AC_line_segment_list[i].gch_value = float(AC_line_segment_list[i].gch)
  AC_line_segment_list[i].length_value = float(AC_line_segment_list[i].length)

  AC_line_complex = complex(AC_line_segment_list[i].ACLineSegment_r_value, AC_line_segment_list[i].ACLineSegment_x_value)
  AC_line_segment_list[i].admittance = (1/AC_line_segment_list[i].length_value) * (1/AC_line_complex)*pow(AC_line_segment_list[i].base_voltage_value, 2)/S_base
  
  
  AC_line_shunt_complex = complex(AC_line_segment_list[i].gch_value, AC_line_segment_list[i].bch_value)
  AC_line_segment_list[i].shunt_admittance = (AC_line_segment_list[i].length_value/2)*(AC_line_shunt_complex)*pow(AC_line_segment_list[i].base_voltage_value, 2)/S_base


# Update Matrix
for i in range(len(all_rdf_ID_stack_list)):
  for iiiiijjj in range(len(all_rdf_ID_stack_list[i])):
    if all_rdf_ID_stack_list[i][iiiiijjj] in breaker_open_rdf_ID_list:
      all_rdf_ID_stack_list[i]=[]
  for ii in range(len(power_transformer_list)):
    if power_transformer_list[ii].rdf_ID in all_rdf_ID_stack_list[i]:
      print("From Busbar "+str(CN_related_to_busbar[all_rdf_ID_stack_list[i][2]]))
      print("To busbar "+str(CN_related_to_busbar[all_rdf_ID_stack_list[i][-2]]))
      buff_Y_matrix_row = CN_related_to_busbar[all_rdf_ID_stack_list[i][2]]
      buff_Y_matrix_column = CN_related_to_busbar[all_rdf_ID_stack_list[i][-2]]
      # print("Matrix row", buff_Y_matrix_row)
      # print("Matrix column", buff_Y_matrix_column)

      # Non Diagonal
      Y_bus_matrix[buff_Y_matrix_row][buff_Y_matrix_column] = -power_transformer_list[ii].admittance_value
      Y_bus_matrix[buff_Y_matrix_column][buff_Y_matrix_row] = -power_transformer_list[ii].admittance_value

      # Diagonal
      Y_bus_matrix[buff_Y_matrix_column][buff_Y_matrix_column] += power_transformer_list[ii].admittance_value
      Y_bus_matrix[buff_Y_matrix_row][buff_Y_matrix_row] += power_transformer_list[ii].admittance_value
  
  for ij in range(len(AC_line_segment_list)):
    if AC_line_segment_list[ij].rdf_ID in all_rdf_ID_stack_list[i]:
      print("From Busbar "+str(CN_related_to_busbar[all_rdf_ID_stack_list[i][2]]))
      print("To busbar "+str(CN_related_to_busbar[all_rdf_ID_stack_list[i][-2]]))
      buff_Y_matrix_row = CN_related_to_busbar[all_rdf_ID_stack_list[i][2]]
      buff_Y_matrix_column = CN_related_to_busbar[all_rdf_ID_stack_list[i][-2]]
      # print("Matrix row", buff_Y_matrix_row)
      # print("Matrix column", buff_Y_matrix_column)
      Y_bus_matrix[buff_Y_matrix_row][buff_Y_matrix_column] += -AC_line_segment_list[ij].admittance
      Y_bus_matrix[buff_Y_matrix_column][buff_Y_matrix_row] += -AC_line_segment_list[ij].admittance

      Y_bus_matrix[buff_Y_matrix_column][buff_Y_matrix_column] += (AC_line_segment_list[ij].admittance + AC_line_segment_list[ij].shunt_admittance)
      Y_bus_matrix[buff_Y_matrix_row][buff_Y_matrix_row] += (AC_line_segment_list[ij].admittance + AC_line_segment_list[ij].shunt_admittance)


for i in range(len(Y_bus_matrix)):
  print(Y_bus_matrix[i])
  print('\n')




#============================================
# Insert Data to Database

# Connect to mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

database_list = []

for databases in mycursor:
    for database in databases:
        database_list.append(database)

# Check if cim object database exist
if "cim_object_database" in database_list:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="CIM_object_database")
    mycursor = mydb.cursor()
else:
    mycursor.execute("CREATE DATABASE cim_object_database")
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="CIM_object_database")
    mycursor = mydb.cursor()



# Table for Base Voltage Data
sql = "DROP TABLE IF EXISTS BaseVoltage";
mycursor.execute(sql)
sql = "CREATE TABLE IF NOT EXISTS BaseVoltage (ID VARCHAR(37) NOT NULL, Value_kV Double , PRIMARY KEY (ID))"
mycursor.execute(sql)

# Insert Base Voltage data to database
sql = "DELETE FROM BaseVoltage"
mycursor.execute(sql)
for i in range(len(base_voltage_list)):
  sql = "INSERT INTO BaseVoltage (ID, Value_kV) VALUES (%s, %s)"
  val = (base_voltage_list[i].rdf_ID, float(base_voltage_list[i].nominal_value))
  mycursor.execute(sql, val)
  mydb.commit()
						
# Table for Substation Data 
sql = "DROP TABLE IF EXISTS Substation"
mycursor.execute(sql)
sql = "CREATE TABLE IF NOT EXISTS Substation (ID VARCHAR(37) NOT NULL, Name VARCHAR(37), Region_rdfID VARCHAR(37), PRIMARY KEY(ID))"
mycursor.execute(sql)   

# Insert Substation data to database
sql = "DELETE FROM Substation"
mycursor.execute(sql)
for i in range(len(substation_list)):
  sql = "INSERT INTO Substation (ID, Name, Region_rdfID) VALUES (%s, %s, %s)"
  val = (substation_list[i].rdf_ID, substation_list[i].name, substation_list[i].region_rdf_ID)
  mycursor.execute(sql, val)
  mydb.commit()
						
# Table for Voltage Level Data
sql = "DROP TABLE IF EXISTS VoltageLevel"
mycursor.execute(sql)
sql = "CREATE TABLE IF NOT EXISTS VoltageLevel (ID VARCHAR(37) NOT NULL, Value_kV Double , Substation_rdfID VARCHAR(37),BaseVoltage_rdfID VARCHAR(37), PRIMARY KEY (ID))"
mycursor.execute(sql)

# Insert Voltage Level data to database
sql = "DELETE FROM VoltageLevel"
mycursor.execute(sql)
for i in range(len(voltage_level_list)):
  sql = "INSERT INTO VoltageLevel (ID, Value_kV, Substation_rdfID, BaseVoltage_rdfID) VALUES (%s, %s, %s, %s)"
  val = (voltage_level_list[i].rdf_ID, voltage_level_list[i].name, voltage_level_list[i].substation_rdf_ID.replace("#",""), voltage_level_list[i].base_voltage_rdf_ID.replace("#",""))
  mycursor.execute(sql, val)
  mydb.commit()
						
# Table for Generating Unit Data
sql = "DROP TABLE IF EXISTS GeneratingUnit"
mycursor.execute(sql)
sql = "CREATE TABLE IF NOT EXISTS GeneratingUnit (ID VARCHAR(37) NOT NULL, Name VARCHAR(37), MaxP DOUBLE, MinP DOUBLE, EquipmentContainer_rdfID VARCHAR(37), PRIMARY KEY (ID))"
mycursor.execute(sql)

# Insert Generating Unit data to database
sql = "DELETE FROM GeneratingUnit"
mycursor.execute(sql)
for i in range(len(generating_unit_list)):
  sql = "INSERT INTO GeneratingUnit (ID, Name, MaxP, MinP, EquipmentContainer_rdfID) VALUES (%s, %s, %s, %s, %s)"
  val = (generating_unit_list[i].rdf_ID, generating_unit_list[i].name, generating_unit_list[i].max_P, 
  generating_unit_list[i].min_P , generating_unit_list[i].equipment_container_rdf_ID.replace("#",""))
  mycursor.execute(sql, val)
  mydb.commit()
									
# Table for Synchronous Machine Data 
sql = "DROP TABLE IF EXISTS SynchronousMachine"
mycursor.execute(sql)
sql = """CREATE TABLE IF NOT EXISTS SynchronousMachine (ID VARCHAR(37) NOT NULL, Name VARCHAR(40), RatedS DOUBLE, P DOUBLE, Q DOUBLE,
GenUnit_rdfID VARCHAR(37), RegControl_rdfID VARCHAR(37), EquipmentContainer_rdfID VARCHAR(37), baseVoltage_rdfID VARCHAR(37), PRIMARY KEY (ID)) """
mycursor.execute(sql)

# Insert Synchronous Machine Data to database
sql = "DELETE FROM SynchronousMachine"
mycursor.execute(sql)
for i in range(len(synchronous_machine_list)):
  sql = "INSERT INTO SynchronousMachine (ID , Name, RatedS , P , Q , GenUnit_rdfID , RegControl_rdfID , EquipmentContainer_rdfID, baseVoltage_rdfID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
  val = (synchronous_machine_list[i].rdf_ID, synchronous_machine_list[i].name, synchronous_machine_list[i].rated_S, 
  synchronous_machine_list[i].active_power,
  synchronous_machine_list[i].reactive_power, synchronous_machine_list[i].generator_unit_rdf_ID.replace("#",""),
  synchronous_machine_list[i].reg_control_rdf_ID.replace("#",""),
  synchronous_machine_list[i].equipment_container_rdf_ID.replace("#",""),
  synchronous_machine_list[i].base_voltage_rdf_ID.replace("#",""))
  mycursor.execute(sql, val)
  mydb.commit()

# Table for Regulating Control Data 
sql = "DROP TABLE IF EXISTS RegulatingControl"
mycursor.execute(sql)
sql = "CREATE TABLE IF NOT EXISTS RegulatingControl (ID VARCHAR(37) NOT NULL, Name VARCHAR(37), TargetValue DOUBLE, PRIMARY KEY (ID))"
mycursor.execute(sql)

# Insert Regulating Control data to database
sql = "DELETE FROM RegulatingControl"
mycursor.execute(sql)
for i in range(len(regulating_control_list)):
  sql = "INSERT INTO RegulatingControl (ID, Name, TargetValue) VALUES (%s, %s, %s)"
  val = (regulating_control_list[i].rdf_ID, regulating_control_list[i].name, regulating_control_list[i].target_value)
  mycursor.execute(sql, val)
  mydb.commit()
									
# Table for Power Transformer
sql = "DROP TABLE IF EXISTS PowerTransformer"
mycursor.execute(sql)
sql = "CREATE TABLE IF NOT EXISTS PowerTransformer (ID VARCHAR(37) NOT NULL, Name VARCHAR(37),EquipmentContainer_rdfID VARCHAR(37), PRIMARY KEY (ID))"
mycursor.execute(sql)

# Insert Power Transformer Data to database
sql = "DELETE FROM PowerTransformer"
mycursor.execute(sql)
for i in range(len(power_transformer_list)):
  sql = "INSERT INTO PowerTransformer (ID , Name, EquipmentContainer_rdfID) VALUES (%s, %s, %s)"
  val = (power_transformer_list[i].rdf_ID, power_transformer_list[i].name,
  power_transformer_list[i].equipment_container_rdf_ID.replace("#",""))
  mycursor.execute(sql, val)
  mydb.commit()
						
# Table for Energy Consumer
sql = "DROP TABLE IF EXISTS EnergyConsumer"
mycursor.execute(sql)
sql = "CREATE TABLE IF NOT EXISTS EnergyConsumer(ID VARCHAR(37) NOT NULL, Name VARCHAR(37), P DOUBLE, Q DOUBLE, EquipmentContainer_rdfID VARCHAR(37), BaseVoltage_rdfID VARCHAR(37),  PRIMARY KEY (ID))";		
mycursor.execute(sql)

# Insert Energy Consumer Data to database
sql = "DELETE FROM EnergyConsumer"
mycursor.execute(sql)
for i in range(len(energy_consumer_load_list)):
  sql = "INSERT INTO EnergyConsumer (ID, Name, P, Q, EquipmentContainer_rdfID, baseVoltage_rdfID) VALUES (%s, %s, %s, %s, %s, %s)"
  val = (energy_consumer_load_list[i].rdf_ID, energy_consumer_load_list[i].name, energy_consumer_load_list[i].active_power, 
  energy_consumer_load_list[i].reactive_power,
  energy_consumer_load_list[i].equipment_container_rdf_ID.replace("#",""),
  energy_consumer_load_list[i].base_voltage_rdf_ID.replace("#",""))
  mycursor.execute(sql, val)
  mydb.commit()
						
# Table for Power Transformer End
sql = "DROP TABLE IF EXISTS TransformerWinding"
mycursor.execute(sql)
sql = """CREATE TABLE IF NOT EXISTS TransformerWinding (ID VARCHAR(40) NOT NULL, Name VARCHAR(40), TransformerR DOUBLE,
        TransformerX DOUBLE, Transformer_rdfID VARCHAR(37), BaseVoltage_rdfID VARCHAR(37),PRIMARY KEY (ID))"""
mycursor.execute(sql)

# Insert Power Transformer End to database
sql = "DELETE FROM TransformerWinding"
mycursor.execute(sql)
for i in range(len(power_transformer_end_transformer_winding_list)):
  sql = "INSERT INTO TransformerWinding (ID , Name, TransformerR , TransformerX , Transformer_rdfID , baseVoltage_rdfID) VALUES (%s, %s, %s, %s, %s, %s)"
  val = (power_transformer_end_transformer_winding_list[i].rdf_ID, power_transformer_end_transformer_winding_list[i].name, 
  power_transformer_end_transformer_winding_list[i].transformer_r, 
  power_transformer_end_transformer_winding_list[i].transformer_x,
  power_transformer_end_transformer_winding_list[i].transformer_rdf_ID.replace("#",""),
  power_transformer_end_transformer_winding_list[i].base_voltage_rdf_ID.replace("#",""))
  mycursor.execute(sql, val)
  mydb.commit()
						
# Table for Circuit Breaker
sql = "DROP TABLE IF EXISTS CircuitBreaker"
mycursor.execute(sql)
sql = "CREATE TABLE IF NOT EXISTS CircuitBreaker (ID VARCHAR(37) NOT NULL, Name VARCHAR(37), State VARCHAR(37), EquipmentContainer_rdfID VARCHAR(37), BaseVoltage_rdfID VARCHAR(37),PRIMARY KEY (ID))"
mycursor.execute(sql)

# Insert Circuit Breaker data to database
sql = "DELETE FROM CircuitBreaker"
mycursor.execute(sql)
for i in range(len(breaker_list)):
  sql = "INSERT INTO CircuitBreaker (ID , Name, State , EquipmentContainer_rdfID) VALUES (%s, %s, %s, %s)"
  val = (breaker_list[i].rdf_ID, breaker_list[i].name, 
  breaker_list[i].state, 
  breaker_list[i].equipment_container_rdf_ID.replace("#",""))
  mycursor.execute(sql, val)
  mydb.commit()

# Table for Tap Changer
sql = "DROP TABLE IF EXISTS RatioTapChanger"
mycursor.execute(sql)
sql = "CREATE TABLE IF NOT EXISTS RatioTapChanger (ID VARCHAR(37) NOT NULL, Name VARCHAR(37), Step DOUBLE, PRIMARY KEY (ID))"				
mycursor.execute(sql)

# Insert Tap Changer data to database
sql = "DELETE FROM RatioTapChanger"
mycursor.execute(sql)
for i in range(len(ratio_tap_changer_list)):
  sql = "INSERT INTO RatioTapChanger (ID , Name, Step) VALUES (%s, %s, %s)"
  val = (ratio_tap_changer_list[i].rdf_ID, ratio_tap_changer_list[i].name, 
  ratio_tap_changer_list[i].step)
  mycursor.execute(sql, val)
  mydb.commit()


# GUI for displaying Y-Bus Matrix
root = Tk()
root.title("Y-Bus Matrix")
height = len(Y_bus_matrix)
width = len(Y_bus_matrix)



Label(root, text="Y-BUS MATRIX").grid(row=0, column=math.floor(width/2))
Label(root, text="").grid(row=1, column=math.floor(width/2))

for i in range(height): #Rows
    for j in range(width): #Columns
        b = Label(root, text=str(Y_bus_matrix[i][j]).replace("(","").replace(")",""))
        b.grid(row=i+2, column=j, pady=5 ,padx=10, sticky="n")

Label(root, text="").grid(row=height+3, column=math.floor(width/2))
Button(root, text="Quit", command=root.destroy).grid(row=height+4, column=math.floor(width/2))


mainloop()