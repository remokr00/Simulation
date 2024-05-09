from pylab import *

def get_input(prompt, cast_type=float, min_value=None, max_value=None):
    while True:
        try:
            value = cast_type(input(prompt))
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                raise ValueError
            return value
        except ValueError:
            print(f"Invalid input. Please enter a {cast_type.__name__} value", end="")
            if min_value is not None and max_value is not None:
                print(f" between {min_value} and {max_value}.")
            else:
                print(".")

def initialize_variables():
    global t_euler, t_rk, s_euler, s_rk, i_euler, i_rk, r_euler, r_rk, k, dt, beta, t_final
    t_euler= get_input("Enter initial time (t=0): ", float, 0)
    t_rk = t_euler
    beta = get_input("Enter infection rate (beta): ", float, 0)
    s_euler = get_input("Enter initial susceptible fraction (s): ", float, 0, 1)
    s_rk = s_euler
    i_euler = get_input("Enter initial infected fraction (i): ", float, 0, 1)
    i_rk = i_euler
    r_euler = get_input("Enter initial recovered fraction (r): ", float, 0, 1)
    r_rk = r_euler
    k = get_input("Enter recovery rate (k): ", float, 0)
    dt = get_input("Enter time step (dt): ", float, 0)
    t_final = get_input("Enter t_final: ",int, 0 )

    return True



def initialize_euler():

    global t_euler, beta, s_euler, i_euler, k, dt, result_s_euler, result_i_euler, result_r_euler, result_t_euler


    result_s_euler = [s_euler]
    result_i_euler = [i_euler]
    result_r_euler = [r_euler]
    result_t_euler = [t_euler]

def observe_euler():
    global s_euler, i_euler, r_euler, result_s_euler, result_i_euler, result_r_euler, result_t_euler, t_euler

    result_s_euler.append(s_euler)
    result_i_euler.append(i_euler)
    result_r_euler.append(r_euler)
    result_t_euler.append(t_euler)


def update_euler_method():
    global s_euler, i_euler, k, r_euler, beta, dt, next_s_euler, next_i_euler, next_r_euler, t_euler

    next_s_euler = s_euler - (beta * s_euler * i_euler * dt)
    next_i_euler = i_euler + (beta * s_euler * i_euler * dt) - (k * i_euler * dt)
    next_r_euler = r_euler + (k * i_euler * dt)
    t_euler = t_euler + dt
    s_euler = next_s_euler
    i_euler = next_i_euler
    r_euler = next_r_euler

def initialize_runge_kutta():
    global t_rk, r_rk, beta, s_sk, i_sk, k, dt, result_s_rk, result_i_rk, result_r_rk, result_t_rk

    result_s_rk = [s_rk]
    result_i_rk = [i_rk]
    result_r_rk = [r_rk]
    result_t_rk = [t_rk]

#Runge-Kutta method
def update_runge_kutta():
    global s_rk, i_rk, k, r_rk, beta, dt, next_s_rk, next_i_rk, next_r_rk, t_rk

    function_derivate_s = -beta * s_rk * i_rk
    function_derivate_i = beta * s_rk * i_rk - k * i_rk
    function_derivate_r = k * i_rk

    k1_s = dt * function_derivate_s
    k1_i = dt * function_derivate_i
    k1_r = dt * function_derivate_r

    k2_s = dt * (-beta * (s_rk + k1_s/2) * (i_rk + k1_i/2))
    k2_i = dt * (beta * (s_rk + k1_s/2) * (i_rk + k1_i/2) - k * (i_rk + k1_i/2))
    k2_r = dt * (k * (i_rk + k1_i/2))

    k3_s = dt * (-beta * (s_rk + k2_s/2) * (i_rk + k2_i/2))
    k3_i = dt * (beta * (s_rk + k2_s/2) * (i_rk + k2_i/2) - k * (i_rk + k2_i/2))
    k3_r = dt * (k * (i_rk + k2_i/2))

    k4_s = dt * (-beta * (s_rk + k3_s) * (i_rk + k3_i))
    k4_i = dt * (beta * (s_rk + k3_s) * (i_rk + k3_i) - k * (i_rk + k3_i))
    k4_r = dt * (k * (i_rk + k3_i))

    next_s_rk = s_rk + (k1_s + 2*k2_s + 2*k3_s + k4_s) / 6
    next_i_rk = i_rk + (k1_i + 2*k2_i + 2*k3_i + k4_i) / 6
    next_r_rk = r_rk + (k1_r + 2*k2_r + 2*k3_r + k4_r) / 6

    t_rk = t_rk + dt
    s_rk = next_s_rk
    i_rk = next_i_rk
    r_rk = next_r_rk


def observe_runge_kutta():

    global s_rk, i_rk, r_rk, result_s_rk, result_i_rk, result_r_rk, result_t_rk, t_rk

    result_s_rk.append(s_rk)
    result_i_rk.append(i_rk)
    result_r_rk.append(r_rk)
    result_t_rk.append(t_rk)


t_euler = 0
s_euler = 0
i_euler = 0
r_euler = 0
t_rk = 0
s_rk = 0
i_rk = 0
r_rk = 0
k = 0
dt = 0
beta = 0
t_final = 0

result_s_euler = []
result_i_euler = []
result_r_euler= []
result_t_euler = []
next_s_euler = 0
next_i_euler = 0
next_r_euler = 0

result_s_rk = []
result_i_rk = []
result_r_rk= []
result_t_rk = []
next_s_rk = 0
next_i_rk = 0
next_r_rk = 0

if initialize_variables():

    initialize_euler()


    for _ in range(t_final):  # Adjust the number of iterations as needed
        update_euler_method()
        observe_euler()

    plot(result_t_euler, result_s_euler, 'b-', label='Susceptible')
    plot(result_t_euler, result_i_euler, 'g-', label='Infected')
    plot(result_t_euler, result_r_euler, 'r-', label='Recovered')
    title('Infection simulation: Euler method')
    xlabel('Time')
    ylabel('Fraction of Population')
    legend()
    show()

    initialize_runge_kutta()
    for _ in range(t_final):
        update_runge_kutta()
        observe_runge_kutta()


    plot(result_t_rk, result_s_rk, 'b-', label='Susceptible')
    plot(result_t_rk, result_i_rk, 'g-', label='Infected')
    plot(result_t_rk, result_r_rk, 'r-', label='Recovered')
    title('Infection simulation: Runge-Kutta method')
    xlabel('Time')
    ylabel('Fraction of Population')
    legend()
    show()

    plot(result_t_rk, result_s_rk, 'b-', label='Susceptible')
    plot(result_t_euler, result_s_euler, 'b--', label='Infected')
    plot(result_t_rk, result_i_rk, 'g-', label='Infected')
    plot(result_t_euler, result_i_euler, 'g--', label='Infected')
    plot(result_t_rk, result_r_rk, 'r-', label='Recovered')
    plot(result_t_euler, result_r_euler, 'r--', label='Recovered')
    title('Comparison between Euler and Runge-Kutta methods')
    xlabel('Time')
    ylabel('Fraction of Population')
    legend()
    show()

    plot(result_t_rk, result_s_rk, 'b-', label='Susceptible')
    plot(result_t_euler, result_s_euler, 'b--', label='Infected')
    title('Comparison between Susceptible fractions in Euler and Runge-Kutta methods')
    xlabel('Time')
    ylabel('Fraction of Population')
    legend()
    show()

    plot(result_t_rk, result_i_rk, 'g-', label='Infected')
    plot(result_t_euler, result_i_euler, 'g--', label='Infected')
    title('Comparison between Infected fractions in Euler and Runge-Kutta methods')
    xlabel('Time')
    ylabel('Fraction of Population')
    legend()
    show()

    plot(result_t_rk, result_r_rk, 'r-', label='Recovered')
    plot(result_t_euler, result_r_euler, 'r--', label='Recovered')
    title('Comparison between Recovered fractions in Euler and Runge-Kutta methods')
    xlabel('Time')
    ylabel('Fraction of Population')
    legend()
    show()

else:
    print("Initialization failed due to input error.")











