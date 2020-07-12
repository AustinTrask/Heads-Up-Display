# Heads-Up-Display
CAD models, parts lists, and CircuitPython script for a dashboard-mounted automobile HUD.


I decided to put this project aside as of July 2020 because the lid deformed inward due to the high summer heat and the weight of the lens on it. I fear that any engineered solution would not be enough. I printed the parts on a Prusa Mini in Prusament PETG.

-----------------------------------------------------------------------------------------------------------------

Purchased Part List:

Adafruit Feather M4 Express

Adafruit Ultimate GPS Featherwing

Adafruit LSM303DLHC Compass + Accelerometer

Adafruit 128x32 OLED Featherwing

Half-sized breadboard

Mirrors Darice Craft Mini Square, 3 inches, 5 Pieces from Amazon, ASIN B004HGODQU

SupremeTech 12 x 12 x 0.04 Inch Acrylic See-Through Mirror, 30% Transparent from Amazon, ASIN B017ONH3EG

Double Convex Lens, 100mm Focal Length, 3" (75mm) Diameter - Spherical, Optically Worked Glass Lens - Ground Edges, Polished - Great for Physics Classrooms - Eisco Labs from Amazon, ASIN B076QKKCXJ

-----------------------------------------------------------------------------------------------------------------

General Information:

If I update the Solidworks files, I will try to update the corresponding .STL files as well.

The acrylic is cut to 2.8"x3" for the viewing piece.

The screws I used to secure the display and the lens parts are simply machine screws and nuts I had. I don't know the true size. Adjust the parts as necesary.

The part titled "HUD_Dash_Mount_v1" is modeled to fit my 2012 Toyota Highlander at my prefered viewing angle. I recommend editing the sketches that define the bounds of the loft as well as the spline that the loft follows to best fit your car and head position.

The .py file is a CircuitPython script that uses the RMC data from the GPS to get the speed. If you think I'm a dumbass for not using the OBD-II port, you're probably right. Too bad. Do it your way. My way still remained accurate to within 2 MPH of the car's speedometer but with a lacking refresh rate.