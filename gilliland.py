import json
import matplotlib.pyplot as plt
import numpy as np

def read_data(jfile):
    with open(jfile,'r') as f:
        return json.load(f)
    
def make_plot(jdict,**kwargs):
    fig,ax=plt.subplots(1,2,figsize=kwargs.get('figsize',(12,6)))
    SMALL_SIZE = 14
    MEDIUM_SIZE = 18
    BIGGER_SIZE = 24

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title    plt.rcParams.update({'font.size': 22})
    lin,log=ax
    lin.set_xlim([0,1])
    lin.set_ylim([0,1])
    lin.set_xticks(np.linspace(0,1,11))
    lin.set_yticks(np.linspace(0,1,11))
    lin.set_xlabel(r'$'+jdict["x"]+r'$')
    lin.set_ylabel(r'$'+jdict["y"]+r'$')
    lin.grid()
    log.set_xscale('log')
    log.set_yscale('log')
    log.set_xlim([0.01,1])
    log.set_ylim([0.01,0.8])
    log.set_xlabel(r'$'+jdict["x"]+r'$')
    log.set_ylabel(r'$'+jdict["y"]+r'$')
    log.grid(True,which='both')
    
    for n,ds in jdict["datasets"].items():
        for en,expt in ds["experiments"].items():
            label=f'{n}'
            if len(ds["experiments"])>1:
                label+=f'-{en}'
            marker_style = dict(marker=expt["matplotlib"]["marker"],    
                                linestyle='', markersize=8,
                                # color='darkgrey',
                                markerfacecolor='black',
                                markerfacecoloralt='black',
                                markeredgecolor='black',
                                alpha=0.5,
                                fillstyle=expt["matplotlib"].get("fillstyle",'full'))
            lin.plot(expt["data"]["x"],expt["data"]["y"],label=label,**marker_style)
            log.plot(expt["data"]["x"],expt["data"]["y"],label=label,**marker_style)
    if 'fits' in kwargs:
        xdomain=np.linspace(0,1,101)
        fits=kwargs['fits']
        for fitname,fit in fits.items():
            func=fit['func']
            y=[]
            for x in xdomain:
                y.append(func(x))
            lin.plot(xdomain,y,fit['shortcode'],label=fit['label'],alpha=0.5)
            log.plot(xdomain,y,fit['shortcode'],label=fit['label'],alpha=0.5)
    lin.legend()
    plt.savefig(kwargs.get('outfile','gilliland.png'),bbox_inches='tight')
    plt.clf()

def Liddle(x):
    if 0<=x<0.01:
        return 1-18.5715*x
    elif 0.01<=x<0.9:
        return 0.545827-0.591422*x+0.002743/x
    elif 0.9<=x<=1:
        return 0.16595-0.16595*x
    else:
        return 0

def DavisP3(x):
    m=0.19
    return (1-0.32*x**m+1.7*x**(2*m))*(1-x**m)

def DavisRational(x):
    m=0.0031
    return (1-x**m)/(1-0.99*x**m)

def Rusche(x):
    return 1-0.37*x-0.63*x**0.16

if __name__=='__main__':
    jd=read_data('gilliland_data.json')
    fits={
        'Liddle':{'func':Liddle,'label':'Liddle(1968)','shortcode':'b--'},
        'Rusche':{'func':Rusche,'label':'Rusche(1999)','shortcode':'b:'},
        'DavisP3':{'func':DavisP3,'label':'Davis(2000)','shortcode':'g-'}
    }
    make_plot(jd,fits=fits,figsize=(18,9))
    # print(Rusche(0.455),DavisP3(0.455))