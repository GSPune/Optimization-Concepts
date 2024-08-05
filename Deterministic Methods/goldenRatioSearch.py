#Globals
rho = 0.38196
tol = pow(10,-3)

def func(x):
    return x**3 - 3*(x**2) + 7

def goldenRatioSearch():
    a = int(input('Enter value of a:'))
    b = int(input('Enter value of b:'))
    t = 1 - rho
    c = a + rho*(b-a); d = a + t*(b-a)
    fA = func(a); fB = func(b); fC= func(c); fD = func(d)
    while(abs(a-b) > tol):
        if(fC < fD):
            # a = a
            b = d; fB = fD
            d = c; fD = fC
            c = a + rho*(b-a)
            fC = func(c)
        else:
            a = c;fA = fC
            c = d;fC = fD
            d = a + t*(b-a)
            fD = func(d)

    x_star = (a+b)/2
    print(f"The minima of the function is {round(func(x_star),3)} at x = {round(x_star,3)}")

goldenRatioSearch()
# print(tol)