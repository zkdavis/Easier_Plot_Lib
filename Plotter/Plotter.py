
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import numpy as np
import itertools
import matplotlib as mpl



class figret:
    def __init__(self, fig, ax, pyplt, plots):
        self.fig = fig
        self.ax = ax
        self.pyplt = pyplt
        self.plots = plots
        self.xscale="log"
        self.ylabel="Y-axis"
        self.xlabel="X-axis"
        self.yscale="log"
        self.loc_R=None
        self.loc_C=None
        self.dss=[]
        self.plot_color_bar=False
        self.cbarray=None
        self.cblabel="None"

class data_set_without_data(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class dataset:
    def __init__(self):
        self.plottype = "plot"
        self.scattertype = "scatter"
        self.plot_type = self.scattertype
        self.x = None
        self.y = None
        self.x_error=None
        self.y_error=None
        self.label = None
        self.color = None
        self.marker = None
        self.marker_size = None
        self.data_type = None
        self.x_data_type = None
        # usually a tuple of two. (a,b) where a goes with marker and b goes with color
        self.parameters = None
        self.colorparametername = None
        self.markerparametername = None

    def getSlope(self):
        if(self.x is not None and self.y is not None):
            slope=[]
            for i in range(len(self.x)-1):
                slope.append(np.log10(self.y[i+1]/self.y[i])/np.log10(self.x[i+1]/self.x[i]))
            if(len(slope)>1):
                slope.append(slope[-1])
            return slope

        else:
            raise data_set_without_data("Dataset","No data found in dataset")

    def createLine(self,pos:float,max:float,min:float,axis:str,isLog:bool=False):
        if(axis=="x"):
            #creates a line with a constant x position
            if(isLog):
                self.y = np.logspace(np.log10(min),np.log10(max),100)
            else:
                self.y = np.linspace(min,max,100)
            self.x = np.full_like(self.y,pos)

        elif(axis=='y'):
            #creates a line with constant y position
            if (isLog):
                self.x = np.logspace(np.log10(min), np.log10(max), 100)
            else:
                self.x = np.linspace(min, max, 100)
            self.y = np.full_like(self.x, pos)

        else:
            print("Incorrect or no axis value given")
        self.marker = "--"



class Plotter:
    def __init__(self):


        self.markers = itertools.cycle((',', '+', '.', 'o', '*'))
        self.linesstyles = itertools.cycle(('--', '-.', '-', ':'))
        self.colors = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'tab:purple', 'tab:gray', 'tab:orange'])



    def Plot(self, datasets: [dataset], title="Plot",
             xlabel=r"X-axis", ylable=r"Y-axis", xscale="log", yscale="log", figsize=15, maxy=None, miny=None,
             maxx=None, minx=None, fig=None, ax=None, pyplt=None,build_legend=True):
        if (pyplt == None):
            pyplt = plt
        if (fig == None or ax == None):
            if (ax == None):
                build_legend = False
            fig, ax = plt.subplots(figsize=(figsize, figsize))
        ax.set_xscale(xscale)
        ax.set_yscale(yscale)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylable)
        ax.set_title(title)
        try:
            if (miny != None or maxy != None):
                ax.set_ylim(miny, maxy)
            if (minx != None or maxx != None):
                ax.set_xlim(minx, maxx)
        except:
            print("couldn't set limits")
        plots = []
        for ds in datasets:
            pl = None
            backup_error=np.full(len(ds.x),0)
            xer = backup_error
            yer = backup_error
            if(ds.x_error is not None):
                xer = ds.x_error
            if(ds.y_error is not None):
                yer = ds.y_error
            if ds.color != None and ds.marker != None and ds.label != None and ds.marker_size != None:
                if ds.plot_type == ds.plottype:
                    pl = ax.plot(ds.x, ds.y, c=ds.color, linestyle=ds.marker, label=ds.label, linewidth=ds.marker_size)
                else:
                    pl = ax.errorbar(ds.x, ds.y, yerr=yer, xerr=xer, c=ds.color, fmt=ds.marker, label=ds.label, ms=ds.marker_size)
            if ds.color == None and ds.marker != None and ds.label != None and ds.marker_size != None:
                if ds.plot_type == ds.plottype:
                    pl = ax.plot(ds.x, ds.y, linestyle=ds.marker, label=ds.label, linewidth=ds.marker_size)
                else:
                    pl = ax.errorbar(ds.x, ds.y, yerr=yer, xerr=xer, fmt=ds.marker, label=ds.label, ms=ds.marker_size)
            if ds.color != None and ds.marker != None and ds.label != None and ds.marker_size==None:
                if ds.plot_type == ds.plottype:
                    pl = ax.plot(ds.x, ds.y, c=ds.color, linestyle=ds.marker, label=ds.label)
                else:
                    pl = ax.errorbar(ds.x, ds.y, yerr=yer, xerr=xer, c=ds.color, fmt=ds.marker, label=ds.label)

            if ds.color == None and ds.marker != None and ds.label != None and ds.marker_size == None:
                if ds.plot_type == ds.plottype:
                    pl = ax.plot(ds.x, ds.y, linestyle=ds.marker, label=ds.label)
                else:
                    pl = ax.errorbar(ds.x, ds.y, yerr=yer, xerr=xer, fmt=ds.marker, label=ds.label)
            if ds.color != None and ds.marker == None and ds.label != None and ds.marker_size != None:
                if ds.plot_type == ds.plottype:
                    pl = ax.plot(ds.x, ds.y, c=ds.color, label=ds.label, linewidth=ds.marker_size)
                else:
                    pl = ax.errorbar(ds.x, ds.y, yerr=yer, xerr=xer, c=ds.color, label=ds.label, ms=ds.marker_size)
            if ds.color != None and ds.marker == None and ds.label == None and ds.marker_size != None:
                if ds.plot_type == ds.plottype:
                    pl = ax.plot(ds.x, ds.y, c=ds.color, label=ds.label, ms=ds.marker_size)
                else:
                    pl = ax.errorbar(ds.x, ds.y, yerr=yer, xerr=xer, c=ds.color, label=ds.label, ms=ds.marker_size)
            if ds.color != None and ds.marker == None and ds.label != None and ds.marker_size == None:
                if ds.plot_type == ds.plottype:
                    pl = ax.plot(ds.x, ds.y, c=ds.color, label=ds.label)
                else:
                    pl = ax.errorbar(ds.x, ds.y, yerr=yer, xerr=xer, c=ds.color, label=ds.label)
            if ds.color != None and ds.marker != None and ds.label == None:
                if ds.plot_type == ds.plottype:
                    pl = ax.plot(ds.x, ds.y, c=ds.color, linestyle=ds.marker)
                else:
                    pl = ax.errorbar(ds.x, ds.y, yerr=yer, xerr=xer, c=ds.color, fmt=ds.marker)
            if ds.color == None and ds.marker == None and ds.label != None:
                if ds.plot_type == ds.plottype:
                    pl = ax.plot(ds.x, ds.y, label=ds.label)
                else:
                    pl = ax.errorbar(ds.x, ds.y, yerr=yer, xerr=xer, label=ds.label)
            if ds.color == None and ds.marker != None and ds.label == None:
                if ds.plot_type == ds.plottype:
                    pl = ax.plot(ds.x, ds.y, linestyle=ds.marker)
                else:
                    pl = ax.errorbar(ds.x, ds.y, yerr=yer, xerr=xer, fmt=ds.marker)
            if ds.color != None and ds.marker == None and ds.label == None and ds.marker_size == None:
                if ds.plot_type == ds.plottype:
                    pl = ax.plot(ds.x, ds.y, c=ds.color)
                else:
                    pl = ax.errorbar(ds.x, ds.y, yerr=yer, xerr=xer, c=ds.color)
            if ds.color == None and ds.marker == None and ds.label == None:
                if ds.plot_type == ds.plottype:
                    pl = ax.plot(ds.x, ds.y)
                else:
                    pl = ax.errorbar(ds.x, ds.y, yerr=yer, xerr=xer)
            plots.append(pl)
        if(build_legend):
            handles, labels = ax.get_legend_handles_labels()
            # if len(datasets) > 8:
            #     patches = []
            #     handles = []
            #     labels = []
            #     colorparameterssecond = []
            #     markerparametersfirst = []
            #     markers = []
            #     colors = []
            #     scatter_color=[]
            #     scatter_markers=[]
            #     for ds in datasets:
            #         # if (ds.parameters[0] not in markerparametersfirst):
            #         #     markerparametersfirst.append(ds.parameters[0])
            #         # if (ds.parameters[1] not in colorparameterssecond):
            #         #     colorparameterssecond.append(ds.parameters[1])
            #         if (ds.color not in colors):
            #             if(ds.plot_type==self.plot_type):
            #                 colors.append(ds.color)
            #             else:
            #                 scatter_color.append(ds.color)
            #         if (ds.marker not in markers):
            #             if(ds.plot_type==self.plot_type):
            #                 markers.append(ds.marker)
            #             else:
            #                 scatter_markers.append(ds.marker)
            #     for i in range(len(colors)):
            #         templine = plt.scatter([], [], marker=markers[0], c=colors[i])
            #         handles.append(templine)
            #     handles = tuple(handles)
            #     handles2 = []
            #     for i in range(len(markers)):
            #         templine = plt.scatter([], [], marker=markers[i], c=colors[0])
            #         handles2.append(templine)
            #     handles2 = tuple(handles2)
            #     handlelength = None
            #     if (len(colors) > len(markers)):
            #         handlelength = len(colors)
            #     else:
            #         handlelength = len(markers)
            #     colorlabel = ds.colorparametername
            #     if (colorlabel == None):
            #         colorlabel = ":"
            #     markerlabel = ds.markerparametername
            #     if (markerlabel == None):
            #         markerlabel = ":"
            #     else:
            #         markerlabel = markerlabel + ":"
            #     for c in colorparameterssecond:
            #         colorlabel = colorlabel + ", " + str(c)
            #     for c in markerparametersfirst:
            #         markerlabel = markerlabel + ", " + str(c)
            #     markerlabel = markerlabel.replace(',', "", 1)
            #     colorlabel = colorlabel.replace(',', "", 1)
            #     ax.legend([handles, handles2], [colorlabel, markerlabel], handlelength=handlelength + 3, loc="best",
            #               handler_map={tuple: HandlerTuple(ndivide=None)})
            #
            # else:
            ax.legend(handles, labels, loc="best", prop={'size': 10})
        fr=figret(fig, ax, pyplt, plots)
        fr.dss=datasets
        return fr

    def multiple_plots(self,figrets:[figret],num_of_row:int,num_of_col:int,title="Plot",
             xlabel=r"X-axis", ylable=r"Y-axis", figsize=15,pyplt=None) -> figret:
        if (pyplt == None):
            pyplt = plt
        fig, axs = plt.subplots(nrows=num_of_row,ncols=num_of_col,figsize=(figsize, figsize))
        for fr in figrets:
            if(fr.loc_R is not None and fr.loc_C is not None):
                r,c = fr.loc_R,fr.loc_C
                if(fr.plot_color_bar):
                    norm = colors.LogNorm(vmin=min(fr.cbarray), vmax=max(fr.cbarray))
                    cmap = cm.ScalarMappable(norm=norm, cmap=cm.rainbow)
                    cmap.set_array([])
                    cs=[]
                    for i in range(len(fr.dss)):
                        c = cmap.to_rgba(fr.cbarray[i])
                        cs.append(c)
                        fr.dss[i].color=c
                    cmap2 = mpl.colors.ListedColormap(cs)
                    self.Plot(fr.dss, ax=axs[r][c], fig=fig, build_legend=False)
                    cb = fig.colorbar(cmap2,ax=axs[r][c])
                    cb.set_label(fr.cblabel)

                else:
                    self.Plot(fr.dss,ax=axs[r][c],fig=fig,build_legend=False)
                handles, labels = axs[r][c].get_legend_handles_labels()
                axs[r][c].legend(handles, labels, loc="best", prop={'size': 10})
            else:
                it=None
                r, c = fr.loc_R, fr.loc_C
                if(r is None):
                    it=c
                if(c is None):
                    it = r
                if (fr.plot_color_bar):
                    norm = colors.LogNorm(vmin=min(fr.cbarray), vmax=max(fr.cbarray))
                    cmap = cm.ScalarMappable(norm=norm, cmap=cm.rainbow)
                    cmap.set_array([])
                    cs = []
                    for i in range(len(fr.dss)):
                        c = cmap.to_rgba(fr.cbarray[i])
                        cs.append(c)
                        fr.dss[i].color = c

                    cmapt = colors.ListedColormap(cs)
                    norm = colors.Normalize(vmin=min(fr.cbarray),vmax=max(fr.cbarray))
                    cmap2 = cm.ScalarMappable(norm=norm, cmap=cmapt)
                    cmap2.set_array([])
                    figr = self.Plot(fr.dss, ax=axs[it], fig=fig, build_legend=False,xscale=fr.xscale,yscale=fr.yscale,title="",ylable=fr.ylabel,xlabel=fr.xlabel)
                    cb = figr.pyplt.colorbar(cmap2,ax=axs[it],ticks=fr.cbarray,spacing="proportional")
                    cb.set_label(fr.cblabel)

                else:
                    figr = self.Plot(fr.dss, ax=axs[it], fig=fig, build_legend=False,xscale=fr.xscale,yscale=fr.yscale,title="",ylable=fr.ylabel,xlabel=fr.xlabel)
                handles, labels = axs[it].get_legend_handles_labels()
                axs[it].legend(handles, labels, loc="best", prop={'size': 10})
        fr = figret(fig,axs,pyplt,None)
        return fr
