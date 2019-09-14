import math
import matplotlib.pyplot as plt

"""
Analytical Solution (no damping)
"""

def spring_pos(x_o, k, m, t):
    return x_o * (math.cos(math.sqrt(k//m)*t))

k = 3.00000
m = 0.50000
x_o = -2.00000

data = []
ts = []
t = 0.00000
while t <= 50.00000:
    ts.append(t)
    data.append(spring_pos(x_o, k, m, t))
    t += 0.025000

plt.plot(ts, data)
plt.ylabel('x(t)')
plt.xlabel('t')
plt.show()


"""
Numerical Solution (Euler Method) (no damping)

equations of motion:
dx/dt = v
dv/dt = −k⁄m x − b⁄m v

where x is position, v is velocity, k is stiffness, b is damping, m is mass, t is time

if k = 3.0, m = 0.5, b = 0.0 then:
dx/dt = v
dv/dt = −6 x

difference equations:
x[n+1] = x[n] + Δt*v[n]
v[n+1] = v[n] + Δt*(−6x[n])
"""

x_data = [-2.00000]
v_data = [0.00000]
t_data = [0.00000]
dt = 0.025000

while t_data[-1] <= 50.00000:
    x_next = x_data[-1] + (dt * v_data[-1])

    # should this be x_data[-1] instead of x_next?
    # using x_next gives results that look closer to the analytical solution
    v_next = v_data[-1] + (dt * (-6 * x_next))

    x_data.append(x_next)
    v_data.append(v_next)
    t_data.append(t_data[-1] + dt)

plt.plot(t_data, x_data)
plt.ylabel('x(t)')
plt.xlabel('t')
plt.show()
