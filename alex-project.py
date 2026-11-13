# All values are in MKS! Eg. densities are kg/m^3, times are all in seconds etc etc

# If false, then all vpython lines are never called
DoingVisuals=True

from enum import Enum
import math
from vpython import *

ObjectType = Enum('ObjectType', [('RIGID_BODY', 0), ('GAS_GIANT', 1), ('SUN', 2)])

# Unit conversions, moreso for more readable code and units
KM = 1000
AU = 150000000 * KM
G = 6.67e-11
MINUTE = 60

class SolarObject:
    type = None
    position = vec(0, 0, 0)
    momentum = vec(0, 0, 0)
    radius = 0
    density = 0
    net_force = vec(0, 0, 0)
    
    def __init__(self, new_type, new_pos, new_vel, new_rad, new_density, new_color):
        self.type = new_type
        self.position = new_pos
        self.momentum = new_vel * new_density * 4/3 * pi * new_rad**3
        self.radius = new_rad
        self.density = new_density

        if DoingVisuals:
            self.vpython_display = sphere(pos=self.position,radius=max(self.radius*8, 1e9),color=new_color, make_trail=True, retain=50*20)
    
    def mass(self):
        "Returns the mass of this object, derived from radius and density"
        return self.density * 4/3 * pi * self.radius**3
        
    
    def gravity_on(self, other_object):
        "Returns the force of gravity, vector, that `self` applies on `other_object`"
        return -G * self.mass() * other_object.mass() / mag2(self.position - other_object.position) * norm(self.position - other_object.position)
    
    def should_merge_with(self, other_object):
        "Return boolean as to whether this object is close enough to other_object such that tidal forces would tear one apart. Calculation is per the Roche Limit."
        # All calculations are done under the assumption that object is the more massive object.
        # The check is done both ways in the main loops anyway, and doing it the wrong way only gives a smaller, more restricitive answer.

        distance = mag(self.position - other_object.position)

        # Numerical constant from the Roche equation, depends on the composition of the two bodies
        roche_constant = 2.44 if self.type == ObjectType.SUN or other_object.type == ObjectType.SUN or self.type != other_object.type else 1.44

        return distance < max(self.radius, other_object.radius) * roche_constant * math.cbrt(self.density / other_object.density)
        
if DoingVisuals:
    scene2 = canvas(title='Orbits', caption='Animated Display', center=vector(0,0,0), background=color.black, width=1200, height=1000)

Sun = SolarObject(ObjectType.SUN, vec(0, 0, 0), vec(10000, 0, 0), 695500 * KM, 1408, color.yellow)
txt = label(pos=vec(0, -1e8 * KM, 0), text="")

ListOfSolarObjects = [
    Sun,
    SolarObject(ObjectType.SUN, vec(50000000 * KM, 200000000 * KM, 0), vec(-10000, 0, 0), 695500 * KM, 1408, color.yellow),
    SolarObject(ObjectType.RIGID_BODY, vec(AU, 0, 0), vec(0, 0, 0), 6390 * KM, 5513, color.green) # Earth
    # Original earth initial velocity: vec(0, 29830, 0)
]

current_time = 0
dt = 15 * MINUTE

def simulate_single_frame():
    "Process and update all objects in `ListOfSolarObjects` according to physics laws"
    global current_time

    # Calculate gravity and apply movement
    for object in ListOfSolarObjects:
        object.net_force = vec(0, 0, 0)
        for other_object in ListOfSolarObjects:
            if object == other_object: continue
            object.net_force += object.gravity_on(other_object)
        
        object.momentum += object.net_force * dt
        object.position += object.momentum / object.mass() * dt

        print(object.type, object.position)
    print()

    # Detect collisions and deal with such
    for object in ListOfSolarObjects:
        for other_object in ListOfSolarObjects:
            if object == other_object: continue
            if object.should_merge_with(other_object): # Merge the objects, with the final properties being the weighted averages of the originals
                og_object_mass = object.mass()

                object.position = (1/(object.mass() + other_object.mass())) * (object.mass()*object.position + other_object.mass()*other_object.position)
                object.density = (1/(object.mass() + other_object.mass())) * (object.mass()*object.density + other_object.mass()*other_object.density)
                object.radius = math.cbrt((3/(4*pi))/((1/og_object_mass) * object.density))

                object.momentum += other_object.momentum

                if other_object.type == ObjectType.SUN:
                    object.type = ObjectType.SUN
                elif other_object.type == ObjectType.GAS_GIANT and object.type == ObjectType.RIGID_BODY:
                    object.type = ObjectType.RIGID_BODY
                
                other_object.vpython_display.visible = False # So, there's actually no way to delete a vpython object. Man.
                other_object.vpython_display.make_trail = False
                other_object.vpython_display.retain = 0
                other_object.vpython_display.position = vec(0, 0, 0)
                other_object.position = vec(0, 0, 0)
                ListOfSolarObjects.remove(other_object)
    
    current_time += dt

# Main loop
while True:
    rate(1200)
    for i in range(1):
        simulate_single_frame()

    txt.text = f"{floor(current_time / 86400)} days"

    if DoingVisuals:
        for object in ListOfSolarObjects:
            if object.vpython_display.visible:
                object.vpython_display.pos = object.position