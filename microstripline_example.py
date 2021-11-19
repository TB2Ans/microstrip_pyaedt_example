"""

Draw a Microstriline example with Ports and run Simulation

--------------------------------------------
This tutorial shows how you can use PyAedt to draw a simple structure in HFSS,
place ports, devise an analysis, mesh, run the simulation and save the results. 

Thorsten Baumheinrich, 2021/11/18

"""
# sphinx_gallery_thumbnail_path = 'Resources/circuit.png'

from pyaedt import Hfss
#from pyaedt import Desktop

###############################################################################
# Launch Desktop and HFSS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This examples will use AEDT 2021.2 in Non-Graphical mode and also runs in graphical mode

desktopVersion = "2021.2"

###############################################################################
# NonGraphical
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Change Boolean to False to open AEDT in graphical mode
#

NonGraphical = True
NewThread = False

###############################################################################
# Launch AEDT and Circuit Design
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Desktop Class initialize Aedt and start it on specified version and specified graphical mode. NewThread Boolean variables defines if
# a user wants to create a new instance of AEDT or try to connect to existing instance of it
#

with Hfss(specified_version="2021.2", non_graphical=False) as hfss:
    hfss["w_line"] = "2.7mm"
    hfss["t_line"] = "0.035mm"
    hfss["w_sub"] = "30mm"
    hfss["l_sub"] = "30mm"
    hfss["t_sub"] = "1.5mm"
    
    hfss.create_new_project("my_pyaedt_microstrip")

###############################################################################
# Build Structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Draw boxes with defined dimensions and assign materials, names    
#
    box1 = hfss.modeler.primitives.create_box(["-w_sub/2",0,"-t_sub"], ["w_sub", "l_sub", "t_sub"], name="substrate", matname="FR4_epoxy")
    box1.color = "Green"
    box2 = hfss.modeler.primitives.create_box(["-w_line/2",0,0], ["w_line", "l_sub", "t_line"], name="line", matname="copper")
    box3 = hfss.modeler.primitives.create_box(["-w_sub/2",0,"-t_sub - t_line"], ["w_sub", "l_sub", "t_line"], name="backside", matname="copper")

###############################################################################
# Place Ports 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# at beginning and end of microstripline    
#    
    hfss.create_lumped_port_between_objects("line", "backside",
                                        hfss.AxisDir.YNeg, 50,
                                        "Port1", True, False)
                                        
    hfss.create_lumped_port_between_objects("line", "backside",
                                        hfss.AxisDir.YPos, 50,
                                        "Port2", True, False)
                                        
                                            
###############################################################################
# Define Analysis 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# create a simulation setup "my_hfss_run"  (no "." in here!), then define linear sweep 
#        
    setup1 = hfss.create_setup(setupname="my_hfss_run")
    linear_count_sweep = hfss.create_linear_count_sweep(setupname="my_hfss_run",
                                                    sweepname="LinearCountSweep",
                                                    unit="GHz", freqstart=0.01,
                                                    freqstop=20, num_of_freq_points=201)

###############################################################################
# Run Analysis 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# run our simulation setup "my_hfss_run" on 4 cores
#      
    hfss.analyze_setup("my_hfss_run", num_cores=4)
 
###############################################################################
# Save project and results  
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# need to define path in here 
#      
    hfss.save_project(project_file="D:\microstrip_pyaedt.aedt", overwrite=True )

###############################################################################
# Close all and Clean up  
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# close both project and desktop to have everything stored and lock file removed
#         
    hfss.close_project()
    hfss.close_desktop()  
#    
    
    
