import math
from datatypes import Universe, Body, OrderedPair


# Simulation Code

def simulate_gravity(initial_universe: Universe, num_gens: int, time: float, trials: int =1) -> list[Universe]:
    """
    Simulate an N-body system for a fixed number of generations.

    Args:
        initial_universe: The starting state of the universe.
        num_gens: Number of simulation steps to advance (>= 0).
        time: Time step (Δt) between generations (> 0).
        trials: Number of simulation steps between recorded snapshots (> 0).

    Returns:
        A list of Universe snapshots of length num_gens + 1.
    """
    start = copy_universe(initial_universe)
    for b in start.bodies:
        b.acceleration = update_acceleration(start, b)
    time_points: list[Universe] = [start]


    current_universe = start
    for i in range(1, num_gens+1):
        current_universe = update_universe(current_universe, time)
        if i % trials == 0 or i == num_gens:
            time_points.append(current_universe)
    return time_points



def update_universe(current_universe: Universe, time: float) -> Universe:
    """
    Advance the universe by a single time step.

    Uses a velocity-Verlet style update: compute new accelerations from the
    current state, then advance velocity and position accordingly.

    Args:
        current_universe: Universe state at the current time.
        time: Time step (Δt) to advance.

    Returns:
        A new Universe instance representing the next state.
    """
    new_universe = copy_universe(current_universe)

    for b in new_universe.bodies:
        b.position = update_position(b, b.acceleration, b.velocity,time)

    for b in new_universe.bodies:
        old_acceleration = b.acceleration
        b.acceleration = update_acceleration(new_universe, b)
        b.velocity = update_velocity(b, old_acceleration, time)
    return new_universe


def momentum(current_universe: Universe) -> OrderedPair:
    """
    Compute the total momentum of the universe.

    Args:
        current_universe (Universe): The universe whose momentum is to be computed.

    Returns:
        OrderedPair: The total momentum of the universe.
    """
    px = 0.0
    py = 0.0
    pz = 0.0
    for b in current_universe.bodies:
        px += b.mass * b.velocity.x
        py += b.mass * b.velocity.y
        pz += b.mass * b.velocity.z
    return OrderedPair(px, py, pz)


def total_energy(current_universe: Universe) -> float:
    """
    Compute the total energy of the universe.

    Args:
        current_universe (Universe): The universe whose energy is to be computed.

    Returns:
        float: The total energy of the universe.
    """
    return kinetic_energy(current_universe) + potential_energy(current_universe)


def kinetic_energy(current_universe: Universe) -> float:
    """
    Compute the total kinetic energy of the universe.

    Args:
        current_universe (Universe): The universe whose energy is to be computed.

    Returns:
        float: The total kinetic energy of the universe.
    """
    KE = 0.0
    for b in current_universe.bodies:
        v_squared = b.velocity.x**2 + b.velocity.y**2 + b.velocity.z**2
        KE += 0.5 * b.mass * v_squared
    return KE


def potential_energy(current_universe: Universe) -> float:
    """
    Compute the total potential energy of the universe.

    Args:
        current_universe (Universe): The universe whose potential energy is to be computed.

    Returns:
        float: The total potential energy of the universe.
    """
    PE = 0.0
    for i, b1 in enumerate(current_universe.bodies):
        for b2 in current_universe.bodies[i+1:]:
            d = distance(b1.position,b2.position)
            if d> 0:
                PE += -current_universe.gravitational_constant * b1.mass * b2.mass / d
    return PE


def update_acceleration(current_universe: Universe, b: Body) -> OrderedPair:
    """
    Compute the body's acceleration from the net gravitational force.

    Uses:
        a = F / m (Newton's second law)

    Args:
        current_universe (Universe): The universe containing all bodies that
            contribute gravitational force.
        b (Body): The body whose acceleration is being computed.

    Returns:
        OrderedPair: A 3D vector (ax, ay, az) representing the updated acceleration.
    """
    # we will do everything componentwise

    net_force = compute_net_force(current_universe,b)
    ax = net_force.x/b.mass
    ay = net_force.y/b.mass
    az = net_force.z/b.mass
    

    return OrderedPair(ax,ay,az)




def update_velocity(b: Body, old_acceleration: OrderedPair, time: float) -> OrderedPair:
    """
    Update velocity using average acceleration over the step.

    Formula:
        v_{t+Δt} = v_t + 0.5 * (a_t + a_{t+Δt}) * Δt

    Args:
        b (Body): The body whose velocity is being updated.
        old_acceleration (OrderedPair): The acceleration at the previous time step.
        time (float): The time step Δt.

    Returns:
        OrderedPair: A new OrderedPair containing the updated velocity (vx, vy).
    """
    vx = b.velocity.x+0.5*(b.acceleration.x+old_acceleration.x)*time
    vy = b.velocity.y+0.5*(b.acceleration.y+old_acceleration.y)*time
    vz = b.velocity.z+0.5*(b.acceleration.z+old_acceleration.z)*time
    

    return OrderedPair(vx,vy,vz)


def update_position(b: Body, old_acc: OrderedPair, old_vel: OrderedPair, time: float) -> OrderedPair:
    """
    Update position using constant-acceleration kinematics.

    Formula:
        p_{t+Δt} = p_t + v_t * Δt + 0.5 * a_t * Δt^2

    Args:
        b (Body): The body whose position is being updated.
        old_acc (OrderedPair): The acceleration at the previous time step.
        old_vel (OrderedPair): The velocity at the previous time step.
        time (float): The time step Δt.

    Returns:
        OrderedPair: A new OrderedPair containing the updated position (px, py).
    """
    px = b.position.x + old_vel.x*time +0.5*old_acc.x*(time**2)
    py = b.position.y + old_vel.y*time +0.5*old_acc.y*(time**2)
    pz = b.position.z + old_vel.z*time +0.5*old_acc.z*(time**2)
    

    return OrderedPair(px,py,pz)


def compute_net_force(current_universe: Universe, b: Body) -> OrderedPair:
    """
    Compute the net gravitational force on a body from all other bodies.

    Args:
        current_universe (Universe): The universe containing all bodies.
        b (Body): The body on which the net gravitational force is computed.

    Returns:
        OrderedPair: A 2D vector (x, y) representing the net gravitational
        force acting on the given body.
    """
    net_force = OrderedPair(0.0,0.0,0.0)
    G = current_universe.gravitational_constant

    for current_body in current_universe.bodies:
        if current_body is not b:
            current_force = compute_force(b, current_body, G)
            net_force.x += current_force.x
            net_force.y += current_force.y
            net_force.z += current_force.z

    return net_force


def compute_force(b1: Body, b2: Body, G: float) -> OrderedPair:
    """
    Compute the gravitational force exerted on one body by another.

    Args:
        b1 (Body): The body on which the force is acting.
        b2 (Body): The body exerting the gravitational force.
        G (float): Gravitational constant.

    Returns:
        OrderedPair: A 3D vector (x, y, z) representing the force on b1.
    """
    d = distance(b1.position,b2.position)
    if d == 0.0:
        return OrderedPair(0.0,0.0,0.0)

    F_magnitude = G*b1.mass*b2.mass/(d**2)

    dx = b2.position.x - b1.position.x
    dy = b2.position.y - b1.position.y
    dz = b2.position.z - b1.position.z

    Fx = F_magnitude *(dx/d)
    Fy = F_magnitude *(dy/d)
    Fz = F_magnitude *(dz/d)

    return OrderedPair(Fx,Fy,Fz)
    



def distance(p1: OrderedPair, p2: OrderedPair) -> float:
    """
    Compute the Euclidean distance between two position vectors.

    Args:
        p1 (OrderedPair): The first position vector.
        p2 (OrderedPair): The second position vector.

    Returns:
        float: The distance between p1 and p2.
    """
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dz = p2.z - p1.z
    d = math.sqrt(dx**2+dy**2+dz**2)

    return d


def copy_universe(current_universe: Universe) -> Universe:
    """
    Deep-copy a Universe, including all of its bodies.

    Args:
        current_universe (Universe): The universe to copy.

    Returns:
        Universe: A new Universe with deep-copied bodies and the same
        width and gravitational constant as the original.
    """
    new_bodies: list[Body] = []
    for b in current_universe.bodies:
        new_bodies.append(copy_body(b))

    u = Universe(new_bodies, current_universe.width, current_universe.gravitational_constant)

    return u


def copy_body(b: Body) -> Body:
    """
    Deep-copy a Body, including position, velocity, and acceleration.

    Args:
        b (Body): The body to copy.

    Returns:
        Body: A new Body with identical attributes and deep-copied
        OrderedPair objects for position, velocity, and acceleration.
    """
    return Body(name=b.name, 
                mass=b.mass, 
                position = OrderedPair(b.position.x, b.position.y,b.position.z), 
                velocity = OrderedPair(b.velocity.x, b.velocity.y, b.velocity.z),
                acceleration = OrderedPair(b.acceleration.x,b.acceleration.y, b.acceleration.z), 
                radius = b.radius,
                density = b.density,
                red=b.red, 
                green=b.green, 
                blue=b.blue)
