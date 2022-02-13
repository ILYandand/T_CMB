import H2_exc
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import scipy as cp
import ReadANDWrite as rw



def calculate_coldens():
    return

if __name__ == '__main__':
    param = {'H': 1, 'H+': 3, 'H2': 2, 'C': 11, 'C+': 12, 'CO': -1}



    path1 = '/home/ilya/Documents/SSW_NIR/Master Models/after upgraidng/'
        #'/home/ilya/Documents/SSW_NIR/Master Models/SeveralDifModels/'
        #'/home/ilya/Documents/SSW_NIR/Master Models/after upgraidng/'
        #'/home/ilya/Documents/SSW_NIR/Master Models/StopColDens_23/'

    wayes = ['SingleKnot_CRR_m16/', 'diffusecloude_CRR_m18/']
    suptitle = {'SingleKnot_CRR_m16/':'CRR = 2E-16, logH=2, LogIuv=0', 'diffusecloude_CRR_m18/':'CRR = 2E-18, logH=2, LogIuv=0'}
    '''
    wayes = ['CosmicRaysBackgr_1/',
             'CosmicRaysBackgr_def/',
             'CosmicRaysBackgr_m1/',
             'CosRayBack_def_exting_col23/',
             'CosRayBack_def_nH_4/',
             'CosRayRate_m17/']
    '''

    '''
    legends = {'SingleKnot_CRR_m16/': 'Without changes',
               'SingKnot_CRR_m16_grNOheating/': 'grain no heating',
               'SingKnot_CRR_m16_NOgrQheat/': 'NO Qheat',
               'SingKnot_CRR_m16_NOqheatNOgr/': 'Two commands',
               'SingKnot_CRR_m16_met_00/': 'metal=0',
               'SingKnot_CRR_m16_met_00withNOqhNOgr/': 'met=0 and two commands'}
    '''
    '''
        'SingKnot_CRR_m16_grNOheating/',
        'SingKnot_CRR_m16_NOqheatNOgr/', 
        'SingKnot_CRR_m16_met_00/', 
        'SingKnot_CRR_m16_met_00withNOqhNOgr/'
        'SingKnot_CRR_m16_NOgrQheat/'
        'SingKnot_CRR_m16_grNOheating/'
    '''
    NameFile1 = 'gridtest_01.ovr_last'
    NameFile2 = 'gridtest_01_species_dens.dat'
    NameFile3 = 'gridtest_01_heat.dat'
    NameFile4 = 'gridtest_01_cool.dat'
    size = 1.0


    for k, way in enumerate(wayes):

        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15 * size, 5 * size))
        sp = {p: [] for p in param.keys()}

        if way[0] == '_':
            continue

        Name = path1 + way + NameFile2



        DATA = rw.READING(Name=Name)

        x = []
        #y = []
        print(k)
        for i, string in enumerate(DATA):
            liststr = string.split()

            if i != 0:
                floatstr = [float(str) for str in liststr]
                x.append(floatstr[0])
                #y.append(floatstr[1])
                for p, ind in param.items():
                    sp[p].append(np.log10(floatstr[ind]))


        NH = np.array([np.trapz(sp['H'][:i], x[:i]) + sp['H'][0] * x[0] for i in range(len(x))])

        Name = path1 + way + NameFile1

        DATA = rw.READING(Name=Name)

        x = []
        T = []
        av = []
        Htot = []
        eden = []

        for i, string in enumerate(DATA):
            liststr = string.split()

            if i != 0:
                floatstr = [float(str) for str in liststr]
                T.append((floatstr[1]))
                eden.append((floatstr[4]))
                x.append(floatstr[0])
                av.append((floatstr[-1])) #np.log10


        if 0:
            x = av
            xlab = r'Av'
        else:
            x = np.log10(NH)
            xlab = r'$\log NHI$ cm$^{-2}$'



        if 0:
            Name = path1 + way + NameFile3

            DATA = rw.READING(Name=Name)

            T = []
            Htot = []
            Ctot = []
            heat = []
            addlabsp = ''
            listOFindBound = []
            labelsOFcont = []

            for i, string in enumerate(DATA):
                liststr = string.split()

                if i != 0:
                    floatstr = [float(stri) for stri in liststr[:4]]

                    if liststr[5] in ['1', 'H']:
                        labsp = liststr[4] + ' ' + liststr[5]
                        indfrac = 6
                    else:
                        labsp = liststr[4]
                        indfrac = 5

                    if i == 1:
                        labelsOFcont.append(labsp)
                        indfirst = i - 1
                        addlabsp = labsp
                    elif i == (len(DATA) - 1):
                        indend = i
                        listOFindBound.append([indfirst, indend])
                    elif addlabsp != labsp:
                        labelsOFcont.append(labsp)
                        indend = i - 1
                        listOFindBound.append([indfirst, indend])
                        indfirst = i
                        addlabsp = labsp



                    floatnum = float(liststr[indfrac])

                    T.append(floatstr[1])
                    heat.append(np.log10(floatnum * floatstr[2]))
                    Htot.append(np.log10(floatstr[2]))
                    Ctot.append(np.log10(floatstr[3]))



            Htot = np.array(Htot)



            for bound, label in zip(listOFindBound, labelsOFcont):
                axes[0][1].plot(x[bound[0]:bound[1]], heat[bound[0]:bound[1]], label=label)
            axes[0][1].plot(x, Htot, label='Htot', color='red')

            Name = path1 + way + NameFile4

            DATA = rw.READING(Name=Name)

            Htot = []
            Ctot = []
            cool = []
            addlabsp = ''
            listOFindBound = []
            labelsOFcont = []

            for i, string in enumerate(DATA):
                liststr = string.split()

                if i != 0:
                    floatstr = [float(stri) for stri in liststr[:4]]

                    if liststr[5] in ['1', 'H', '2']:
                        labsp = liststr[4] + ' ' + liststr[5]
                        indfrac = 7
                    else:
                        labsp = liststr[4]
                        indfrac = 6

                    if i == 1:
                        labelsOFcont.append(labsp)
                        indfirst = i - 1
                        addlabsp = labsp
                    elif i == (len(DATA) - 1):
                        indend = i
                        listOFindBound.append([indfirst, indend])
                    elif addlabsp != labsp:
                        labelsOFcont.append(labsp)
                        indend = i - 1
                        listOFindBound.append([indfirst, indend])
                        indfirst = i
                        addlabsp = labsp

                    floatnum = float(liststr[indfrac])

                    cool.append(np.log10(floatnum * floatstr[3]))
                    Htot.append(np.log10(floatstr[2]))
                    Ctot.append(np.log10(floatstr[3]))

            for bound, label in zip(listOFindBound, labelsOFcont):
                axes[0][2].plot(x[bound[0]:bound[1]], heat[bound[0]:bound[1]], label=label)

            axes[0][2].plot(x, Ctot, label='Ctot', color='blue')

        axes[0].plot(x, T, color='red')
        axes[0].set_ylabel(r'$T$ K', fontsize='x-large', color='red')
        axes[0].set_xlabel(xlab, fontsize='x-large')
        axes[0].set_yscale("log")
        #axes[0].set_xlim([-1, 11])

        if 0:
            axadd = axes[0].twinx()
            axadd.plot(x, eden, color='blue')
            axadd.set_ylabel(r'$\log n_e$ cm$^{-3}$', fontsize='x-large', color='blue')
            axadd.set_yscale("log")
        #axadd.set_xlim([-1, 11])
        #axes[0][1].set_ylabel(r'$Ctot$ erg cm$^{-3}$ s$^{-1}$', fontsize='x-large', color='red')
        #axes[0][1].set_ylabel(r'$Ctot$ erg cm$^{-3}$ s$^{-1}$', fontsize='x-large', color='red')
        #axadd = axes[0][1].twinx()
        #axadd.plot(x, Ctot, color='blue')
        #axadd.set_ylabel(r'$Ctot$ erg cm$^{-3}$ s$^{-1}$', fontsize='x-large', color='blue')

        i = 1
        for p, ind in param.items():
            if p == 'C':
                i = 2
            axes[i].plot(x, sp[p], label=p)




        labels = [r'$T$ K',
                  #r'$\log$ Heat,  erg cm$^{-3}$ s$^{-1}$',
                  #r'$\log$ Cool,  erg cm$^{-3}$ s$^{-1}$',
                  r'$\log n$ cm$^{-3}$',
                  r'$\log n$ cm$^{-3}$']
                  #r'Hello']
        r'$Ctot$ erg cm$^{-3}$ s$^{-1}$'
        title = ['Dependence of temperature on NH',
                 #'fraction 1 of heating on NH',
                 #'fraction 2 of cooling on NH',
                 'H',
                 'C']
                 #'']

        for i in range(1, 3):
            if i < 3:
                ax = axes[i]
            else:
                ax = axes[1]
            ax.legend()
            ax.set_xlabel(xlab, fontsize='x-large')
            ax.set_title(title[i], fontsize='x-large')
            ax.set_ylabel(labels[i], fontsize='x-large')
            #же большпя?тоже ax.set_xlim([-1, 11])
        fig.suptitle(suptitle[way], fontsize=14)
        plt.tight_layout()

        savebool = True
        if savebool:
            fig.savefig(path1 + 'Profiles_' + way[:-1] + '_.pdf', bbox_inches='tight')



    plt.show()



