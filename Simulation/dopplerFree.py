from math import sqrt,pi

fRb = 299792458/(780)  # in GHz


def avg_speed(T):
    return(sqrt((8*8.314*T)/(.085 * pi)))


def fDopp(vAvg):
    return((299792458)/(299792458+vAvg))*fRb

Temps = list(range(293, 343, 4))

def broadening():
    dBroad = []
    for i in Temps:
        Spread = fDopp(-avg_speed(i)) - fDopp(avg_speed(i))
        dBroad.append(Spread)

    return dBroad


print(broadening())
