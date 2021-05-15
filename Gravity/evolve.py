import math

def evolve(s, v, s_S, dt):
    # F = ma
    # G * Mm/r^2 = ma
    # a = G * M/r^2     (Centripital acceleration)
    
    x = s_S[0] - s[0]
    y =  s_S[1] - s[1] 
    
    r = (x**2 + y**2)**0.5
    theta = math.atan2(y,x)

    G = 6.67408 * 10**(-11)     # [m^3 kg^-1 s^-2]
    M = 1.989 * 10**30          # [kg]
    a = G * M / (r**2)  # [m]

    vf = [ v[0] + a*math.cos(theta)*dt, v[1] + a*math.sin(theta)*dt ]
    sf = [ s[0] + vf[0]*dt, s[1] + vf[1]*dt ]
    
    return [sf, vf]

#print(evolve([10,10], [1,1], [0,0], 0.5))
