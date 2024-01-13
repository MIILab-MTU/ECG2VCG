# -*- coding: utf-8 -*-"
"""
Created on 04/25/2021  4:52 PM


@author: Zhuo
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # <--- This is important for 3d plotting

ecgLead_list = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
color = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:olive']


def plot_12ecgs(demo_arr, fig_dir=None, show_fig=False, show_grid=True):
    """plot ecg figures"""
    t = range(len(demo_arr[1]))

    fig, ax = plt.subplots(6, 2, figsize=(12, 12))

    for i in range(0, 6):
        j = 0
        ax[i, j].plot(t, demo_arr[i, :])
        ax[i, j].set_ylabel(ecgLead_list[i])
        ax[i, j].xaxis.set_ticklabels([])
        ax[i, j].yaxis.set_ticklabels([])
        if show_grid:
            ax[i, j].grid(True)
        #     ax.set_xticks(np.arange(x_min, x_max, 0.2))
        #     ax.set_yticks(np.arange(y_min, y_max, 0.5))
        #
        #     ax.minorticks_on()
        #
        #     ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        #
        #     ax.grid(which='major', linestyle='-', linewidth=0.5 * display_factor, color=color_major)
        #     ax.grid(which='minor', linestyle='-', linewidth=0.5 * display_factor, color=color_minor)

        j = 1
        ax[i, j].plot(t, demo_arr[i + 6, :])
        ax[i, j].set_ylabel(ecgLead_list[i + 6])
        ax[i, j].xaxis.set_ticklabels([])
        ax[i, j].yaxis.set_ticklabels([])
        if show_grid:
            ax[i, j].grid(True)

    # save to file
    if fig_dir is not None:
        plt.savefig(fig_dir, dpi=300, bbox_inches='tight')

    # show
    if show_fig:
        plt.show()
    else:
        plt.close(fig)


def plot_vcg_XYZandVM(demo_arr, fig_dir=None, show_fig=False, show_timeOnX=False):
    """
    Plot vcg figure

    Parameters
    ----------
    demo_arr: array
        vcg array, the size should be (3, ).
    fig_dir: string
        The directory of the saved figure.
    show_fig: bool, optional
        If True, show the plot immediately.
    show_timeOnX: bool, optional
        If True, show the time on the x axis as the unit, else show the sampling index.
    sampling_rate: int, default=500
        ECG sampling rate.
    """
    x = demo_arr[0, :]
    y = demo_arr[1, :]
    z = demo_arr[2, :]
    sampling = np.arange(len(x))
    # ts = np.true_divide(sampling, sampling_rate)
    # ts = sampling/int(sampling_rate)
    ts = sampling / 1000
    vm = np.sqrt(np.power(x, 2) + np.power(y, 2) + np.power(z, 2))
    # origin = np.array([[0], [0]])  # origin point

    # Figure 1 VCG_1 contains X, Y, Z waveform.
    fig1 = plt.figure(figsize=(7, 9), constrained_layout=True)
    gs = fig1.add_gridspec(3, 2)

    # X waveform
    ax1 = fig1.add_subplot(gs[0, :2])
    if show_timeOnX:
        ax1.plot(ts, x)
    else:
        ax1.plot(sampling, x)
    ax1.grid(True)
    ax1.set_ylabel('X')
    ax1.set_xlim(xmin=0, xmax=len(x))

    # Y waveform
    ax2 = fig1.add_subplot(gs[1, :2])
    if show_timeOnX:
        ax2.plot(ts, y)
    else:
        ax2.plot(sampling, y)
    ax2.grid(True)
    ax2.set_ylabel('Y')
    ax2.set_xlim(xmin=0, xmax=len(y))

    # Z waveform
    ax3 = fig1.add_subplot(gs[2, :2])
    ax3.plot(sampling, z)
    ax3.grid(True)
    ax3.set_ylabel('Z')
    ax3.set_xlim(xmin=0, xmax=len(z))

    # save to file
    if fig_dir is not None:
        plt.savefig(fig_dir + 'XYZ.png', dpi=300, bbox_inches='tight')

    # show
    if show_fig:
        plt.show()
    else:
        plt.close()

    # Figure 2 VCG_2 contains vector magnitude (VM) waveform for delineation.
    # fig2 = plt.figure(figsize=(len(sampling) / 100, len(sampling) / 100 / 2))
    # fig2 = plt.figure(figsize=(len(sampling)/100, len(sampling)/2/100), dpi=100, frameon=False)
    fig2 = plt.figure(frameon=False)
    fig2.set_size_inches(len(sampling) / 100, len(sampling) / 2 / 100)
    # ax4 = fig2.add_subplot()
    ax4 = plt.Axes(fig2, [0., 0., 1., 1.])
    ax4.plot(sampling, vm)
    # ax4.grid(True)
    # ax4.set_ylabel('VM')
    ax4.set_xlim(xmin=0, xmax=len(vm))
    # ax4.set_ylim(ymin=np.min(vm), ymax=np.max(vm))
    ax4.set_axis_off()
    fig2.add_axes(ax4)

    # save to file
    if fig_dir is not None:
        plt.savefig(fig_dir + 'VM.png', bbox_inches='tight', pad_inches=0)

    # show
    if show_fig:
        plt.show()
    else:
        plt.close()


def plot_vcg_blue(demo_arr, fig_dir=None, show_fig=False, show_timeOnX=False):
    # Figure 3 VCG_3 contains VCG_XYZ, VCG_VM, and 4 VCG images:
    # XY vcg - Frontal plane
    x = demo_arr[0, :]
    y = demo_arr[1, :]
    z = demo_arr[2, :]
    sampling = np.arange(len(x))
    # ts = np.true_divide(sampling, sampling_rate)
    # ts = sampling/int(sampling_rate)
    ts = sampling / 1000
    vm = np.sqrt(np.power(x, 2) + np.power(y, 2) + np.power(z, 2))
    origin = np.array([[0], [0]])  # origin point

    fig = plt.figure(figsize=(20, 12), constrained_layout=True)
    gs = fig.add_gridspec(4, 6)

    # X waveform
    ax1 = fig.add_subplot(gs[0, :2])
    if show_timeOnX:
        ax1.plot(ts, x)
    else:
        ax1.plot(sampling, x)
    ax1.grid(True)
    ax1.set_ylabel('X')

    # Y waveform
    ax2 = fig.add_subplot(gs[1, :2])
    if show_timeOnX:
        ax2.plot(ts, y)
    else:
        ax2.plot(sampling, y)
    ax2.grid(True)
    ax2.set_ylabel('Y')

    # Z waveform
    ax3 = fig.add_subplot(gs[2, :2])
    ax3.plot(sampling, z)
    ax3.grid(True)
    ax3.set_ylabel('Z')

    # vector magnitude waveform
    ax4 = fig.add_subplot(gs[3, :2])
    ax4.plot(sampling, vm)
    ax4.grid(True)
    ax4.set_ylabel('VM')

    # XY vcg - Frontal plane
    ax5 = fig.add_subplot(gs[:2, 2:4])
    ax5.plot(x, y)
    ax5.set_title('Frontal plane')
    ymin, ymax = ax5.get_ylim()
    xmin, xmax = ax5.get_xlim()
    ax5.axhline(c='k', lw=2)
    ax5.text(xmax - (xmax - xmin) / 20, (ymax - ymin) / 50, 'X', size=20)
    ax5.axvline(c='k', lw=2)
    ax5.text((xmax - xmin) / 70, ymin + (ymax - ymin) / 50, 'Y', size=20)
    ax5.grid(True)
    # ax.set_xticks([])
    # ax.set_yticks([])

    # ZY vcg - Sagittal plane
    ax6 = fig.add_subplot(gs[2:, 2:4])
    ax6.plot(z, y)
    ax6.set_title('Sagittal plane')
    ymin, ymax = ax6.get_ylim()
    xmin, xmax = ax6.get_xlim()
    ax6.axhline(c='k', lw=2)
    ax6.text(xmax - (xmax - xmin) / 20, (ymax - ymin) / 50, 'Z', size=20)
    ax6.axvline(c='k', lw=2)
    ax6.text((xmax - xmin) / 70, ymin + (ymax - ymin) / 50, 'Y', size=20)
    ax6.grid(True)

    # XZ vcg - Transversal plane
    ax7 = fig.add_subplot(gs[:2, 4:])
    ax7.plot(x, z)
    ax7.set_title('Transversal plane')
    ymin, ymax = ax7.get_ylim()
    xmin, xmax = ax7.get_xlim()
    ax7.axhline(c='k', lw=2)
    ax7.text(xmax - (xmax - xmin) / 20, (ymax - ymin) / 50, 'X', size=20)
    ax7.axvline(c='k', lw=2)
    ax7.text((xmax - xmin) / 70, ymin + (ymax - ymin) / 50, 'Z', size=20)
    ax7.grid(True)

    # XYZ vcg - 3D plot
    ax8 = fig.add_subplot(gs[2:, 4:], projection='3d')
    ax8.plot(x, y, z)
    ax8.grid(True)
    ax8.legend()
    #
    # fig3 = plt.figure(figsize=(14, 12))
    # ax5 = fig3.add_subplot(2, 2, 1)
    # ax5.plot(x, y)
    # ax5.set_title('Frontal plane')
    # ymin, ymax = ax5.get_ylim()
    # xmin, xmax = ax5.get_xlim()
    # ax5.axhline(c='k', lw=2)
    # ax5.text(xmax - (xmax - xmin) / 20, (ymax - ymin) / 50, 'X', size=20)
    # ax5.axvline(c='k', lw=2)
    # ax5.text((xmax - xmin) / 70, ymin + (ymax - ymin) / 50, 'Y', size=20)
    # ax5.grid(True)
    # # ax.set_xticks([])
    # # ax.set_yticks([])
    #
    # # ZY vcg - Sagittal plane
    # ax6 = fig3.add_subplot(2, 2, 2)
    # ax6.plot(z, y)
    # ax6.set_title('Sagittal plane')
    # ymin, ymax = ax6.get_ylim()
    # xmin, xmax = ax6.get_xlim()
    # ax6.axhline(c='k', lw=2)
    # ax6.text(xmax - (xmax - xmin) / 20, (ymax - ymin) / 50, 'Z', size=20)
    # ax6.axvline(c='k', lw=2)
    # ax6.text((xmax - xmin) / 70, ymin + (ymax - ymin) / 50, 'Y', size=20)
    # ax6.grid(True)
    #
    # # XZ vcg - Transversal plane
    # ax7 = fig3.add_subplot(2, 2, 3)
    # ax7.plot(x, z)
    # ax7.set_title('Transversal plane')
    # ymin, ymax = ax7.get_ylim()
    # xmin, xmax = ax7.get_xlim()
    # ax7.axhline(c='k', lw=2)
    # ax7.text(xmax - (xmax - xmin) / 20, (ymax - ymin) / 50, 'X', size=20)
    # ax7.axvline(c='k', lw=2)
    # ax7.text((xmax - xmin) / 70, ymin + (ymax - ymin) / 50, 'Z', size=20)
    # ax7.grid(True)
    #
    # # XYZ vcg - 3D plot
    # ax8 = fig3.add_subplot(2, 2, 4, projection='3d')
    # ax8.plot(x, y, z)
    # ax8.grid(True)
    # ax8.legend()

    # save to file
    if fig_dir is not None:
        plt.savefig(fig_dir + 'blue.png', dpi=300)

    # show
    if show_fig:
        plt.show()
    else:
        plt.close()

def paint_color(demo_arr,one,two,three,four,five,fig_dir,show_timeOnX=False):

    x = demo_arr[0, :]
    y = demo_arr[1, :]
    z = demo_arr[2, :]

    vm = np.sqrt(np.power(x, 2) + np.power(y, 2) + np.power(z, 2))

    a1 = vm[0:one+ 1]
    a2 = vm[one:two+ 1]
    a3 = vm[two:three+ 1]
    a4 = vm[three:four+ 1]
    a5 = vm[four:five+ 1]
    a6 = vm[five:-1]

    x1 = x[0:one + 1]
    x2 = x[one:two + 1]
    x3 = x[two:three + 1]
    x4 = x[three:four + 1]
    x5 = x[four:five + 1]
    x6 = x[five:-1]

    y1 = y[0:one + 1]
    y2 = y[one:two + 1]
    y3 = y[two:three + 1]
    y4 = y[three:four + 1]
    y5 = y[four:five + 1]
    y6 = y[five:-1]

    z1 = z[0:one + 1]
    z2 = z[one:two + 1]
    z3 = z[two:three + 1]
    z4 = z[three:four + 1]
    z5 = z[four:five + 1]
    z6 = z[five:-1]

    sampling = np.arange(len(vm))
    fig = plt.figure(frameon=False)
    fig.set_size_inches(len(sampling) / 100, len(sampling) / 2 / 100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])


    ax.plot(sampling[0:one + 1],a1,color='#1f77b4')
    ax.plot(sampling[one:two+ 1], a2, color='darkorange')
    ax.plot(sampling[two:three+ 1], a3, color='green')
    ax.plot(sampling[three:four+ 1], a4, color='red')
    ax.plot(sampling[four:five+ 1], a5, color='yellow')
    ax.plot(sampling[five: -1], a6,color='#1f77b4')

    ax.set_xlim(xmin=0, xmax=len(vm))
    ax.set_axis_off()
    fig.add_axes(ax)

    plt.savefig(fig_dir + 'VCG.png', bbox_inches='tight', pad_inches=0)


    ts = sampling / 1000
    origin = np.array([[0], [0]])  # origin point

    fig1 = plt.figure(figsize=(20, 12), constrained_layout=True)
    gs = fig.add_gridspec(4, 6)

    # X waveform
    ax1 = fig1.add_subplot(gs[0, :2])
    if show_timeOnX:
        ax1.plot(ts, x)
    else:
        ax1.plot(sampling, x)
    ax1.grid(True)
    ax1.set_ylabel('X')

    # Y waveform
    ax2 = fig1.add_subplot(gs[1, :2])
    if show_timeOnX:
        ax2.plot(ts, y)
    else:
        ax2.plot(sampling, y)
    ax2.grid(True)
    ax2.set_ylabel('Y')

    # Z waveform
    ax3 = fig1.add_subplot(gs[2, :2])
    ax3.plot(sampling, z)
    ax3.grid(True)
    ax3.set_ylabel('Z')

    # vector magnitude waveform
    ax4 = fig1.add_subplot(gs[3, :2])
    ax4.plot(sampling[0:one + 1], a1, color='#1f77b4')
    ax4.plot(sampling[one:two + 1], a2, color='darkorange')
    ax4.plot(sampling[two:three + 1], a3, color='green')
    ax4.plot(sampling[three:four + 1], a4, color='red')
    ax4.plot(sampling[four:five + 1], a5, color='yellow')
    ax4.plot(sampling[five: -1], a6, color='#1f77b4')
    ax4.grid(True)
    ax4.set_ylabel('VM')

    # XY vcg - Frontal plane
    ax5 = fig1.add_subplot(gs[:2, 2:4])
    ax5.plot(x2, y2, color='darkorange')
    ax5.plot(x3, y3, color='green')
    ax5.plot(x4, y4, color='red')
    ax5.plot(x5, y5, color='yellow')
    ax5.set_title('Frontal plane')
    ymin, ymax = ax5.get_ylim()
    xmin, xmax = ax5.get_xlim()
    ax5.axhline(c='k', lw=2)
    ax5.text(xmax - (xmax - xmin) / 20, (ymax - ymin) / 50, 'X', size=20)
    ax5.axvline(c='k', lw=2)
    ax5.text((xmax - xmin) / 70, ymin + (ymax - ymin) / 50, 'Y', size=20)
    ax5.grid(True)
    # ax.set_xticks([])
    # ax.set_yticks([])

    # ZY vcg - Sagittal plane
    ax6 = fig1.add_subplot(gs[2:, 2:4])
    ax6.plot(z2, y2, color='darkorange')
    ax6.plot(z3, y3, color='green')
    ax6.plot(z4, y4, color='red')
    ax6.plot(z5, y5, color='yellow')
    ax6.set_title('Sagittal plane')
    ymin, ymax = ax6.get_ylim()
    xmin, xmax = ax6.get_xlim()
    ax6.axhline(c='k', lw=2)
    ax6.text(xmax - (xmax - xmin) / 20, (ymax - ymin) / 50, 'Z', size=20)
    ax6.axvline(c='k', lw=2)
    ax6.text((xmax - xmin) / 70, ymin + (ymax - ymin) / 50, 'Y', size=20)
    ax6.grid(True)

    # XZ vcg - Transversal plane
    ax7 = fig1.add_subplot(gs[:2, 4:])
    ax7.plot(x2, z2, color='darkorange')
    ax7.plot(x3, z3, color='green')
    ax7.plot(x4, z4, color='red')
    ax7.plot(x5, z5, color='yellow')
    ax7.set_title('Transversal plane')
    ymin, ymax = ax7.get_ylim()
    xmin, xmax = ax7.get_xlim()
    ax7.axhline(c='k', lw=2)
    ax7.text(xmax - (xmax - xmin) / 20, (ymax - ymin) / 50, 'X', size=20)
    ax7.axvline(c='k', lw=2)
    ax7.text((xmax - xmin) / 70, ymin + (ymax - ymin) / 50, 'Z', size=20)
    ax7.grid(True)

    # XYZ vcg - 3D plot
    ax8 = fig1.add_subplot(gs[2:, 4:], projection='3d')
    ax8.plot(x2, y2, z2, color='darkorange')
    ax8.plot(x3, y3, z3, color='green')
    ax8.plot(x4, y4, z4, color='red')
    ax8.plot(x5, y5, z5, color='yellow')
    ax8.grid(True)
    ax8.legend()

    plt.savefig(fig_dir + 'VCGBlue.png', bbox_inches='tight', pad_inches=0)
