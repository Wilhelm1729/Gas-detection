from numpy import sqrt, sin, cos, pi
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.integrate import quad
from math import sin, pi

def U_in(equation, s):
    variables = {'s': s}
    return eval(equation, {}, variables)

def lock_in_amplifier_integrand(s, t, T, f_ref, phi, equation):
    return (1/T) * sin(2 * pi * f_ref * s + phi) * U_in(equation, s)  # Returns U_out

t = 10
T = 4
phi = 0
f_ref = 1
equation = "s"

# Corrected order of arguments in quad function and args
U_out = quad(lock_in_amplifier_integrand, t-T, t, args=(t, T, f_ref, phi, equation))
print(U_out)