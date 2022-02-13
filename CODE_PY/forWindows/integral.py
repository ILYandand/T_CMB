import numpy as np

def integral (x=None, f=None, xstop=0, f0 = 0):
    '''
    if type(x) == np.ndarray:
        x = list(x)
    if type(f) == np.ndarray:
        f = list(f)
    '''
    	
    if x is not None and f is not None:
        if len(x) == len(f) and len(x) > 1:
            if type(x) != list:
                x = list(x)
            if type(f) != list:
                f = list(f)
                
                
            F = 0
            for xx in x:
                if xx <= xstop:
                    i = x.index(xx)
                    if i > 0:
                        df = (f[i]+f[i-1])*(x[i]-x[i-1])/2
                    else:
                        df = (f[0]+f0)*x[0]/2
                    F = F + df
            return F
        else:
            if len(x) != len(f):
                print('ERROR: len(x) not equal len(f)!')
                return 1/0
            return 0
    else:
        print('ERROR: There are no x or f in argument!')
        return 1/0


if __name__ == '__main__':
    x = np.array([1, 2, 3])
    F = [integral(x=x, f=[2, 5, 6], xstop=xx) for xx in x]
    print(F)
