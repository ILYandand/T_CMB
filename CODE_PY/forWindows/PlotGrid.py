import H2_exc
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import scipy as cp



'''
H2 = {}

fold = '/home/ilya/Documents/SSW_NIR/Master Models/The Last Bachelor Models/z0_met_m02'
prefix = 'gridtest_01'
H2database = 'MW'
NameFileIN = 'script_cloudy_sim_02.in'
COM = 'Cloudy'
metallab = 'Z'

H2[COM] = H2_exc.H2_exc(folder=fold, prefix=prefix,
                        namefileIN=NameFileIN, H2database=H2database,
                        CodOfMOd=COM)

H2[COM].readfolder()
H2[COM].setgrid(pars=['n0', 'uv'], fixed={}, show=False)

NameFileIN = ''
prefix = ''
fold = '/home/ilya/Documents/SSW_NIR/Master Models/av2_0_cmb0_0_z1_0_n_uv'
H2database = 'MW'
COM = 'PDR'
metallab = 'me'
# metallab: -0.2

H2[COM] = H2_exc.H2_exc(folder=fold, prefix=prefix,
                        namefileIN=NameFileIN, H2database=H2database,
                        CodOfMOd=COM)

H2[COM].readfolder()
H2[COM].setgrid(pars=['n0', 'uv'], fixed={}, show=False)
'''



#cmaps = {'boundNHI':'inferno', 'fractionNH2':'cividis', 'T10':'plasma'}
cmaps = {'boundNHI': 'Greens', 'fractionNH2': 'Blues', 'T10': 'hot'}
paramout = list(cmaps.keys())


class inputParam():
    def __init__(self, CodeOfMode='', folder=[''], NameFileIN=[''],
                 prefix=[''], H2database='', metallab='', param=['n0', 'uv'],
                 parout=paramout):
        self.parout = parout
        self.param = param
        self.fold = folder
        self.prefix = prefix
        self.NameFileIN = NameFileIN
        self.metallab = metallab
        self.COM = CodeOfMode
        self.H2database = H2database


class gridH2():
    def __init__(self, INPar=inputParam(), seting=True):
        self.INP = INPar
        self.setH2()
        self.setGlobalGrid()
        if seting:
            self.setGlobalLimits()
            self.setGridDelta()


    def setH2(self):
        INP = self.INP
        COM = INP.COM
        self.H2 = []
        for fold, NMI, pref in zip(INP.fold, INP.NameFileIN, INP.prefix):
            h2 = H2_exc.H2_exc(folder=fold, prefix=pref,
                                namefileIN=NMI, H2database=INP.H2database,
                                CodOfMOd=COM)
            h2.readfolder()
            self.H2.append(h2)

    def setGlobalGrid(self, par=[], parout=[]):
        INP = self.INP
        H2 = self.H2
        self.models = {}
        if len(par) == 0:
            par = INP.param

        if len(parout) == 0:
            parout = INP.parout

        self.GlobalListPar = {p: [] for p in par}
        self.points = []
        self.ParsOut = {p: [] for p in parout}

        for h2 in H2:
            for name, model in h2.models.items():
                point = []
                for p in par:
                    parvalue = np.log10(getattr(model, p))
                    point.append(parvalue)
                    if parvalue not in self.GlobalListPar[p]:
                        self.GlobalListPar[p].append(parvalue)
                if tuple(point) not in self.models.keys():
                    self.points.append(tuple(point))
                    self.models[tuple(point)] = model
                    for pout in parout:
                        self.ParsOut[pout].append(getattr(model, pout))

    def setGlobalLimits(self, par=[], bounds={'': []}):
        self.bounds = {}

        if len(par) == 0:
            par = self.INP.param

        if [] in bounds.values():
            for p in par:
                min = np.min(self.GlobalListPar[p])
                max = np.max(self.GlobalListPar[p])

                self.bounds[p] = [min, max]
        else:
            self.bounds = bounds

    def setGridDelta(self, par=[], delta=None):
        if len(par) == 0:
            par = self.INP.param

        self.delta = {}
        if delta is None:
            for p in par:
                length = float(len(self.GlobalListPar[p]))
                self.delta[p] = (self.bounds[p][1] - self.bounds[p][0]) / (length - 1.0)
        else:
            print('There mustn\'t be delta as argument')
            b = 1/0



def CountOverlapOfLimits(H2=[], bounds={'':[None,None]}):
    for h2 in H2:
        lenn0 = 0
        lenuv = 0

        for i, (Code, h2) in enumerate(H2.items()):
            listn0 = np.array(h2.listpar['n0'])
            listuv = np.array(h2.listpar['uv'])

            listn0 = np.sort(np.log10(listn0))
            listuv = np.sort(np.log10(listuv))

        if i == 0:
            maxn0 = listn0.max()
            minn0 = listn0.min()

            maxuv = listuv.max()
            minuv = listuv.min()

            lenn0 = len(listn0)
            lenuv = len(listuv)
        else:
            if maxn0 > listn0.max():
                maxn0 = listn0.max()
                lenn0 = len(listn0)

            if minn0 < listn0.max():
                minn0 = listn0.min()

            if maxuv > listuv.max():
                maxuv = listuv.max()
                lenuv = len(listuv)

            if minuv < listuv.max():
                minuv = listuv.min()

    if (maxuv < minuv) or (maxn0 < minn0):
        print('Error. The areas have no common intersection')
        b = 1/0

    lengthn0 = lenn0
    lengthuv = lenuv

    deltaxx = (maxn0 - minn0) / ((lengthn0 - 1) * 2.0)
    deltayy = (maxuv - minuv) / ((lengthuv - 1) * 2.0)

'''
deltaxx = (listn0.max() - listn0.min()) / ((lengthn0 - 1) * 2.0)
deltayy = (listuv.max() - listuv.min()) / ((lengthuv - 1) * 2.0)
'''


if 1:
    folder = ['/home/ilya/Documents/SSW_NIR/Master Models/The Last Bachelor Models/z0_met_m02',
              '/home/ilya/Documents/SSW_NIR/Master Models/befor upgraiding/z0_met_m02_withLowUV']
    prefix = ['gridtest_01', 'gridtest_01']
    NameFileIN = ['script_cloudy_sim_02.in', 'script_cloudy_sim_02.in']
elif 1:
    folder = ['/home/ilya/Documents/SSW_NIR/Master Models/befor upgraiding/LastModelsWITHOUThm12(UV_0to2)']
    prefix = ['gridtest_01', 'gridtest_01']
    NameFileIN = ['script_cloudy_sim_02.in', 'script_cloudy_sim_02.in']
else:
    folder = ['/home/ilya/Documents/SSW_NIR/Master Models/after upgraiding/grid_diffuse']
    prefix = ['gridtest_01']
    NameFileIN = ['script_cloudy_sim_02.in']

input1 = inputParam(CodeOfMode='Cloudy', folder=folder, NameFileIN=NameFileIN,
                    prefix=prefix, H2database='MW')

NameFileIN = ['']
prefix = ['']
fold = ['/home/ilya/Documents/SSW_NIR/Master Models/befor upgraiding/av2_0_cmb0_0_z1_0_n_uv']
H2database = 'MW'
COM = 'PDR'
metallab = 'me'

input2 = inputParam(CodeOfMode=COM, folder=fold, prefix=prefix, H2database='MW', NameFileIN=NameFileIN)

H2 = [gridH2(INPar=input1, seting=False), gridH2(INPar=input2, seting=False)]

H2[0].setGlobalLimits(bounds={'n0': [0.0, 4.0], 'uv': [-1.0, 2.0]})
H2[0].setGridDelta(par=['n0', 'uv'])
H2[1].setGlobalLimits(bounds={'n0': [0.0, 4.0], 'uv': [-1.0, 2.0]})
H2[1].setGridDelta(par=['n0', 'uv'])

maxparout = {}
minparout = {}
for param in paramout:
    max0 = np.max(H2[0].ParsOut[param])
    max1 = np.max(H2[1].ParsOut[param])

    min0 = np.min(H2[0].ParsOut[param])
    min1 = np.min(H2[1].ParsOut[param])

    if param == 'boundNHI': # or param == 'fractionNH2':
        max0 = np.log10(max0)
        max1 = np.log10(max1)

        min0 = np.log10(min0)
        min1 = np.log10(min1)

    maxparout[param] = np.max([max0, max1])
    minparout[param] = np.min([min0, min1])

savebool = True

'''{'boundNHI':'inferno', 'fractionNH2':'cividis', 'T10':'plasma'}'''
if __name__ == '__main__':
    for k, param in enumerate(paramout):
        print(param)
        size = 1.0
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12 * size, 11 * size))

        if param == 'boundNHI':
            title = r'$\log NHI$ (cm$^{-2}$), when NH2/NHI > 1%'
        elif param == 'fractionNH2':
            title = 'Fraction (%) NH2 relative to column density of total hydrogen\n' + r' at $\log NHI = 20$'
        elif param == 'T10':
            title = r'Temperature (K) of excitation of the rotation level j=1 of $H_2$' + '\n' + r'at $\log NHI = 20$'

        fig.suptitle(title, fontsize='x-large')
        # fig.subplots_adjust(wspace=0.3)

        #for m, (Code, h2) in enumerate(H2.items()):
        for m, h2 in enumerate(H2):
            models = h2.models
            print(h2.INP.COM)


            ax = axes[m]

            deltaxx = h2.delta['n0'] / 2.0
            deltayy = h2.delta['uv'] / 2.0

            minn0 = h2.bounds['n0'][0]
            maxn0 = h2.bounds['n0'][1]

            minuv = h2.bounds['uv'][0]
            maxuv = h2.bounds['uv'][1]

            ax.set_ylim([minuv-deltayy, maxuv+deltayy])
            ax.set_xlim([minn0-deltaxx, maxn0+deltaxx])

            ax.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)

            Code = h2.INP.COM
            ax.set_title(Code, fontsize='x-large', loc='left')
            ax.set_xlabel(r'$\log n_0$', fontsize='x-large')
            ax.set_ylabel(r'$\log I_\mathrm{UV}$', fontsize='x-large')
            #c = ax.pcolor(X, Y, z, cmap='Oranges', vmin=np.min(z), vmax=np.max(z))
            #cax = fig.add_axes([0.93, 0.27, 0.01, 0.47])
            #fig.colorbar(z, cax=cax, orientation='vertical')]

            x = []
            y = []
            z = []

            n=-1
            #for n, (name, mod) in enumerate(models.items()):
            for point, parout in zip(h2.points, h2.ParsOut[param]):
                n += 1
                v1 = point[0]
                v2 = point[1]
                l = parout
                #col = 'red'
                col = 'black'

                add = ''
                if param == 'boundNHI':
                    l = np.log10(l)
                    textt = '{:.1f}'
                elif param == 'T10':
                    col = 'blue'
                    add = '|'
                    textt = '{:.0f}'
                elif param == 'fractionNH2':
                    l = l
                    textt = '{:.0f}'

                #l = np.log10(float(l))

                print(v1, v2, l)
                if (minn0 <= v1 <= maxn0) and (minuv <= v2 <= maxuv):
                    ax.text(v1, v2, add + textt.format(l) + add, size=12, color=col,
                            horizontalalignment='center', verticalalignment='center',)



                if 0:
                    if l < 0:
                        l = -l
                    if param == 'T10' and l > 200:
                        l = 200
                    elif param == 'boundNHI':
                        if l > 20:
                            l =20
                        elif l < 17:
                            l = 17
                elif 1:
                    if l < 0:
                        l = -l
                    if param == 'T10' and l > 200:
                        l = 200
                    elif param == 'boundNHI':
                        if l > 20:
                            l = 20
                        elif l < 17:
                            l = 16


                x.append(v1)
                y.append(v2)
                z.append(l)


            x, y, z = np.array(x), np.array(y), np.array(z)

            z_rbf = cp.interpolate.Rbf(x, y, z, smooth=0.1) #function='linear'

            xmax = maxn0 #x.max()
            xmin = minn0 #x.min()

            ymax = maxuv #y.max()
            ymin = minuv #y.min()


            deltax = h2.delta['n0']/10.0 #lengthn0 * 10
            deltay = h2.delta['uv']/10.0 #lengthuv * 10

            #deltax = (xmax - xmin) / ((numx - 1) * 2.0)
            #deltay = (ymax - ymin) / ((numy - 1) * 2.0)

            xmax = xmax + deltax * 10.0/2.0
            xmin = xmin - deltax * 10.0/2.0

            ymax = ymax + deltay * 10.0/2.0
            ymin = ymin - deltay * 10.0/2.0


            xx = np.arange(xmin, xmax, deltax)
            yy = np.arange(ymin, ymax, deltay)

            X, Y = np.meshgrid(xx, yy)

            Z = np.zeros_like(X)

            Flagnext = True
            print('Next there are values which are less then -0')
            for i, xi in enumerate(xx):
                for j, yj in enumerate(yy):
                    Z[j, i] = z_rbf(xi, yj)
                    if Z[j, i] < -0 and Flagnext:
                        print(xi, yj, Z[j, i])
                        str = 'no' #input('Do you want to do next?')
                        if str not in ['YES', 'yes', 'Yes', 'yEs',
                                       'yeS', 'YEs', 'yES', 'YeS']:
                            Flagnext = False

            vmin = Z.min()
            vmax = Z.max()

            vmin = minparout[param]
            vmax = maxparout[param]

            '''{'boundNHI':'inferno', 'fractionNH2':'cividis', 'T10':'plasma'}'''
            if 0:
                if param == 'boundNHI':
                    vmax = 20
                    vmin = 17
                elif param == 'fractionNH2':
                    vmax = 100
                    vmin = 0
                elif param == 'T10':
                    vmax = 200
                    vmin = 0
            elif 1:
                if param == 'boundNHI':
                    vmax = 20
                    vmin = 16
                    levels = [16.5, 17.5, 18.5, 19.5]
                    fmt = '%.1f'
                elif param == 'fractionNH2':
                    vmax = 100
                    vmin = 0
                    levels = [10, 30, 60, 90]
                    fmt = '%.0f'
                elif param == 'T10':
                    vmax = 200
                    vmin = 0
                    levels = [50, 100, 150, 190]
                    fmt = '%.0f'

            p = ax.pcolor(X, Y, Z, cmap=cmaps[param], edgecolors='face', vmin=vmin, vmax=vmax)
            cs = ax.contour(X, Y, Z, levels=levels, vmin=vmin, vmax=vmax, colors='black')
            cs.clabel(fmt=fmt)#cmap=mpl.cm.RdBu
            cb = fig.colorbar(p, ax=ax) #orientation='horizontal'

        plt.tight_layout()

        if savebool:
            fig.savefig('Grids_' + param + '_.pdf', bbox_inches='tight')

plt.show()

#ax.text

if 0:
    xx = np.log10(np.array(listn0))
    yy = np.log10(np.array(listuv))

    xx = np.sort(xx)
    yy = np.sort(yy)


    deltax = (xx[1] - xx[0]) / 2.0
    deltay = (yy[1] - yy[0]) / 2.0

    xx = list(xx)
    yy = list(yy)



    xx.append(np.max(xx) + 2 * deltax)
    yy.append(np.max(yy) + 2 * deltay)

    x = np.array(xx) - deltax
    y = np.array(yy) - deltay

    C = np.zeros(shape=(lengthn0, lengthuv), dtype=float, order='F') + 1

    if 0:
        indi = yy.index(v2)
        indj = xx.index(v1)

        if l != 1:
            C[indi, indj] = l #np.log10(l)