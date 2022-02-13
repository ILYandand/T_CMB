import H2_exc
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import scipy as cp
import ReadANDWrite as rw

path1 = '/home/ilya/Documents/SSW_NIR/Master Models/after upgraidng/'
#'/home/ilya/Documents/SSW_NIR/Master Models/'
wayes = ['The Last Bachelor Models/z0_met_m02/',
         'NoQheatAndTurnON/',
         'OrthoParaTurnON/']
        #'NoQheat/'
NameFiles = ['gridtest_01.species_col']

energy = np.array([0.5, 118.5, 354.35, 705.54, 1168.78, 1740.21])

if __name__ == '__main__':
    size = 1.0
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10 * size, 9 * size))

    for way in wayes:
        if way == 'NoQheat/':
            NameFiles = ['grid000000000_gridtest_01.species_col',
                         'grid000000001_gridtest_01.species_col']
        elif way == 'The Last Bachelor Models/z0_met_m02/':
            NameFiles = ['grid000000070_gridtest_01.species_col']
            ind = 0
        else:
            NameFiles = ['gridtest_01.species_col']
            ind = 1


        for k, NamF in enumerate(NameFiles):
            Name = path1 + way + NamF

            DATA = rw.READING(Name=Name)

            for i, string in enumerate(DATA):
                liststr = string.split()
                if i == ind:
                    floatstr = [np.log10(float(str)) for str in liststr]

            y = []
            for i, val in enumerate(floatstr[2:8]):
                if i % 2 == 0:
                    yi = val/(2 * i + 1)
                else:
                    yi = val/(2.0 * i + 1.0) / 3.0
                y.append(val)

            if len(NameFiles) == 1:
                ax = axes
            else:
                ax = axes[k]


            ax.plot(energy, y, label=way)

    ax.legend()
    ax.set_title('Population of rotational levels of H2 \n in model' +
                 r' with $\log n_0 = 3.5$ and $\log I_{UV} = 2.5$', fontsize='x-large')
    ax.set_xlabel(r'$E_J$ cm$^{-1}$', fontsize='x-large')
    ax.set_ylabel(r'$NH_{2J}$ $/$ $g_J$ cm$^{-2}$', fontsize='x-large')

    plt.tight_layout()
    plt.show()

    fig.savefig('Population1.pdf', bbox_inches='tight')

