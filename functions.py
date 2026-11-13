from datatypes import OrderedPair, Boid, Sky
import math
import sys 
from typing import List

# Paste the functions you wrote for HW4 problems 1-10 here.
# distance() and copy_sky() are provided below; do not paste them again.

def distance(p0: OrderedPair, p1: OrderedPair) -> float:
    """
    Compute the Euclidean distance between two points in 2D space.
    Input:
        p0 (OrderedPair): The first point, with x and y coordinates.
        p1 (OrderedPair): The second point, with x and y coordinates.
    Output:
        float: The Euclidean distance between p0 and p1.
    """
    dx = p0.x - p1.x
    dy = p0.y - p1.y
    return math.sqrt(dx * dx + dy * dy)

def copy_sky(current_sky: Sky) -> Sky:
    """
    Create a deep copy of a Sky object, duplicating all its parameters and boids.
    Input:
        current_sky (Sky): The Sky instance to be copied, containing boids and 
                           simulation parameters (e.g., width, max speed, proximity).
    Output:
        Sky: A new Sky object with identical properties and boid data as the input, 
             but stored in separate memory so changes to one do not affect the other.
    """
    new_sky = Sky()
    new_sky.width = current_sky.width
    new_sky.max_boid_speed = current_sky.max_boid_speed
    new_sky.proximity = current_sky.proximity
    new_sky.separation_factor = current_sky.separation_factor
    new_sky.alignment_factor = current_sky.alignment_factor
    new_sky.cohesion_factor = current_sky.cohesion_factor

    new_boids = []
    for b in current_sky.boids:
        pos_copy = OrderedPair(b.position.x, b.position.y)
        vel_copy = OrderedPair(b.velocity.x, b.velocity.y)
        acc_copy = OrderedPair(b.acceleration.x, b.acceleration.y)
        new_boids.append(Boid(pos_copy, vel_copy, acc_copy))

    new_sky.boids = new_boids
    return new_sky


# ---- Problem 1: sum_vectors() -- from your latest passing submission ----

def sum_vectors(vectors: List[OrderedPair]) -> OrderedPair:
    """
    Sum multiple vectors.

    Args:
        vectors: A list of OrderedPair vectors.
    Returns:
        An OrderedPair representing the sum of all vectors in the list.
    """
    sumx = 0
    sumy=0
    for i in vectors:
        sumx+=i.x
        sumy+=i.y
    return OrderedPair(sumx,sumy)


# ---- Problem 2: limit_speed() -- from your latest passing submission ----

# write your limit_speed() function here along with any subroutines that you need.
def limit_speed(vel : OrderedPair, max_speed: float) -> OrderedPair:
    """
    Limit the speed of a boid.

    Args:
        max_speed: The maximum allowed speed.
        vel: An OrderedPair representing the velocity vector.
    Returns:
        An OrderedPair representing the velocity after limiting its
        magnitude to max_speed, if necessary.
    """
    vx = vel.x
    vy = vel.y
    magv = math.sqrt(vx**2 +vy**2)
    return OrderedPair(vx/magv*max_speed,vy/magv*max_speed)


# ---- Problem 3: net_acceleration_due_to_cohesion() -- from your latest passing submission ----

# write your net_acceleration_due_to_cohesion() function here along with any subroutines that you need.
def net_acceleration_due_to_cohesion(current_sky: Sky, i: int) -> OrderedPair:
    """
    Compute the net acceleration due to cohesion for a boid.

    Args:
        current_sky: A Sky object containing boids, proximity, and cohesionFactor.
        i: Index of the boid of interest in current_sky.boids.
    Returns:
        An OrderedPair representing the acceleration component due to
        cohesive forces acting on the boid at index i.
    """
    net_acc = OrderedPair(0.0,0.0)
    b1 = current_sky.boids[i]
    count = 0
    

    for s in range(len(current_sky.boids)):
        b2 = current_sky.boids[s]
        distance = math.sqrt((b2.position.x-b1.position.x)**2 +(b2.position.y-b1.position.y)**2)
        if i ==s:
            pass
        elif 0<distance and distance <= current_sky.proximity:
            net_acc.x += current_sky.cohesion_factor *(b2.position.x-b1.position.x)/distance
            net_acc.y += current_sky.cohesion_factor *(b2.position.y-b1.position.y)/distance
            count+=1
    if count > 0:
        net_acc.x /=count
        net_acc.y /= count

    return net_acc


# ---- Problem 4: net_acceleration_due_to_alignment() -- from your latest passing submission ----

# write your net_acceleration_due_to_alignment() function here along with any subroutines that you need.
def net_acceleration_due_to_alignment(current_sky: Sky, i: int) -> OrderedPair:
    """
    Compute the net acceleration due to alignment for a boid.

    Args:
        current_sky: A Sky object containing boids, proximity, and alignmentFactor.
        i: Index of the boid of interest in current_sky.boids.
    Returns:
        An OrderedPair representing the acceleration component due to
        alignment forces acting on the boid at index i.
    """
    net_acc = OrderedPair(0.0,0.0)
    b1 = current_sky.boids[i]
    count = 0
    

    for s in range(len(current_sky.boids)):
        b2 = current_sky.boids[s]
        distance = math.sqrt((b2.position.x-b1.position.x)**2 +(b2.position.y-b1.position.y)**2)
        if i ==s:
            pass
        elif 0<distance and distance <= current_sky.proximity:
            net_acc.x += current_sky.alignment_factor *(b2.velocity.x)/distance
            net_acc.y += current_sky.alignment_factor *(b2.velocity.y)/distance
            count+=1
    if count > 0:
        net_acc.x /=count
        net_acc.y /= count

    return net_acc


# ---- Problem 5: net_acceleration_due_to_separation() -- from your latest passing submission ----

# write your net_acceleration_due_to_separation() function here along with any subroutines that you need.
def net_acceleration_due_to_separation(current_sky: Sky, i: int) -> OrderedPair:
    """
    Compute the net acceleration due to separation for a boid.

    Args:
        current_sky: A Sky object containing boids, proximity, and separationFactor.
        i: Index of the boid of interest in current_sky.boids.
    Returns:
        An OrderedPair representing the acceleration component due to
        separation forces acting on the boid at index i.
    """
    net_acc = OrderedPair(0.0,0.0)
    b1 = current_sky.boids[i]
    count = 0
    

    for s in range(len(current_sky.boids)):
        b2 = current_sky.boids[s]
        distance = math.sqrt((b2.position.x-b1.position.x)**2 +(b2.position.y-b1.position.y)**2)
        if i ==s:
            pass
        elif 0<distance and distance <= current_sky.proximity:
            net_acc.x += current_sky.separation_factor *(b1.position.x-b2.position.x)/(distance**2)
            net_acc.y += current_sky.separation_factor *(b1.position.y-b2.position.y)/(distance**2)
            count+=1
    if count > 0:
        net_acc.x /=count
        net_acc.y /= count

    return net_acc


# ---- Problem 6: update_acceleration() -- from your latest passing submission ----

#implement update_acceleration and note use of subroutines
def update_acceleration(current_sky: Sky, i: int) -> OrderedPair:
    """
    Update the acceleration of a boid in the next generation.

    Args:
        current_sky: A Sky object containing boids and behavioral parameters.
        i: Index of the boid of interest in current_sky.boids.
    Returns:
        An OrderedPair representing the updated acceleration of the boid
        at index i for the next generation.
    """
    NADTS = net_acceleration_due_to_separation(current_sky,i)
    NADTA = net_acceleration_due_to_alignment(current_sky, i)
    NADTC = net_acceleration_due_to_cohesion(current_sky,i)

    vectors = [NADTS,NADTA,NADTC]
    return sum_vectors(vectors)


# ---- Problem 7: update_velocity() -- from your latest passing submission ----

# write your update_velocity() function here along with any subroutines that you need.
def update_velocity(b: Boid, old_acceleration: OrderedPair, max_boid_speed: float, time_step: float) -> OrderedPair:
    """
    Update the velocity of a boid.

    Args:
        b: A Boid object.
        old_acceleration: An OrderedPair representing the previous acceleration.
        time_step: The time step over which to update the velocity.
        max_boid_speed: The maximum allowed speed of the boid.
    Returns:
        An OrderedPair representing the updated velocity of the boid after
        time_step seconds.
    """
    new_velocity = OrderedPair(0.0,0.0)

    new_velocity.x = 0.5*(old_acceleration.x+b.acceleration.x)*time_step + b.velocity.x
    new_velocity.y = 0.5*(old_acceleration.y+b.acceleration.y)*time_step + b.velocity.y

    new_velocity = limit_speed(new_velocity,max_boid_speed)

    return new_velocity


# ---- Problem 8: update_position() -- from your latest passing submission ----

# write your update_position() function here along with any subroutines that you need.
def update_position(
    b : Boid,
    old_acceleration : OrderedPair,
    old_velocity : OrderedPair,
    sky_width: float,
    time_step: float
) -> OrderedPair:
    """
    Update the position of a boid.

    Args:
        b: A Boid object.
        old_acceleration: An OrderedPair representing the previous acceleration.
        old_velocity: An OrderedPair representing the previous velocity.
        sky_width: The width of the sky (used for wrap-around behavior).
        time_step: The time step over which to update the position.
    Returns:
        An OrderedPair representing the updated position of the boid after
        time_step seconds, with wrap-around at the sky boundaries.
    """
    new_pos = OrderedPair(0.0,0.0)

    new_pos.x = 0.5*old_acceleration.x*time_step**2 + old_velocity.x*time_step + b.position.x
    new_pos.y = 0.5*old_acceleration.y*time_step**2 + old_velocity.y*time_step + b.position.y

    while new_pos.x > sky_width:
        new_pos.x -= sky_width
    while new_pos.y > sky_width:
        new_pos.y -= sky_width
    while new_pos.x < 0:
        new_pos.x+=sky_width
    while new_pos.y < 0:
        new_pos.y+=sky_width
    
    return new_pos


# ---- Problem 9: update_sky() -- from your latest passing submission ----

# implement update_sky
def update_sky(current_sky: Sky, time_step: float) -> Sky:
    """
    Update a sky of boids by one time step.

    Args:
        current_sky: A Sky object containing boids and simulation parameters.
        time_step: The time step for the update.
    Returns:
        The updated Sky after one time step.
    """
    new_sky = copy_sky(current_sky)
    
    for b in range(len(current_sky.boids)):
        old_boid = current_sky.boids[b]
        new_boid = new_sky.boids[b]

        new_boid.acceleration = update_acceleration(current_sky,b)
        new_boid.velocity = update_velocity(new_boid, old_boid.acceleration, current_sky.max_boid_speed, time_step)
        new_boid.position = update_position(new_boid, old_boid.acceleration, old_boid.velocity, current_sky.width, time_step)

    return new_sky


# ---- Problem 10: simulate_boids() -- from your latest passing submission ----

# write your simulate_boids() function here along with any subroutines that you need.
# NOTE: The autograder will only investigate the last sky in the list of skies that you return.
# If you want to see the intermediate skies, then you will need to print them to stdout.
def simulate_boids(initial_sky: Sky, num_gens: int, time_step: float) -> List[Sky]:
    """
    Simulate a boids system over multiple generations.

    Args:
        initial_sky: A Sky object representing the initial state.
        time_step: The time step for each simulation iteration.
        num_gens: Number of generations to simulate.
    Returns:
        A list of Sky states after simulating num_gens iterations,
        starting with initial_sky.
    """
    skies = [0.0]*(num_gens+1)
    skies[0] = initial_sky
    for i in range(1,len(skies)):
        current_sky = skies[i-1]
        skies[i] = update_sky(current_sky,time_step)

    return skies
