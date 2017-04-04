import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib.colors import ListedColormap
from datetime import datetime
import os
import sys
import tkinter as tk
from tkinter import filedialog

# %% Select STK access reports
# root = tk.Tk()
# root.withdraw()
# file_path = filedialog.askopenfilenames(initialdir="C:\\Users\eagles\Desktop",
#                                         title="Select Access Reports")

cwd = os.getcwd()
file_dir = cwd+"/"+"examplePasses/"

save_dir = cwd+"/"+"availabilityPlots/"

ref_facility = ['DaytonaBeach', 'Daytona Beach, FL'] # [tag, name]

# list of facilities being compated to "ref_facility"
facilities =   [['Prescott', 'Prescott, Az'],
                ['Washington', 'Seattle, WA'],
                ['Fairbanks', 'Fairbanks, AK'],
                ['Boulder', 'Boulder, CO']]

# Date range 
start_date = '2016, 10, 13'
stop_date  = '2017, 10, 13'
date_range = pd.date_range(start_date, stop_date)

# %% Extract access time and duration; get total obs time and number of 
#    acceptable obs, length is above a threshold

# Parms
secs_in_day = 24*60*60 # seconds in one 24 hour day
percentile = 99
min_duration = 1*60  # seconds; minimum access duration to be considered 
                     #          as useful pass
show_plots = True
rejection_list = ['Access', '']
extensions = ['.csv', '.CSV']

# Work on each CSV file
facility_pass = []
names= []
obs_numb = []
revisit_time = []
longest_passes = []

# get availability for reference facility
ref_facility_availability = []
file_path_ref = sorted(os.listdir(os.path.join(file_dir, ref_facility[0])))
file_path_ref = [n for n in file_path_ref if os.path.splitext(n)[1]
                         in extensions]
file_path_ref = sorted(file_path_ref)
for file_name_ref in file_path_ref:
    # load ref csv
    df_ref = pd.read_csv(os.path.join(file_dir, ref_facility[0], file_name_ref), 
                                                   delimiter=',')
    # Remove spaces and duplicate headers
    df_ref = df_ref.loc[~df_ref['Access'].isin(rejection_list)]
    
    # Convert strngs to floating point and datetime
    df_ref['Access'] = pd.to_numeric(df_ref['Access'])
    df_ref['Start Time (UTCG)'] = pd.to_datetime(df_ref['Start Time (UTCG)'])
    df_ref['Stop Time (UTCG)'] = pd.to_datetime(df_ref['Stop Time (UTCG)'])
    df_ref['Duration (sec)'] = pd.to_numeric(df_ref['Duration (sec)'])
    
    # Make start time the index
    df_ref = df_ref.set_index('Start Time (UTCG)')
    df_ref = df_ref.sort()

    # filte based off time minimum
    df_ref = df_ref.loc[df_ref['Duration (sec)'] > min_duration]

    # determine availability
    sat_availability = []
    for date in date_range:
        numb_pass = 0
        for ref in df_ref.index:
            if date.date() == ref.date():
                if numb_pass < 2:
                    numb_pass = numb_pass + 1
        sat_availability.append(numb_pass)

    ref_facility_availability.append(sat_availability)
print("Completed processing reference site data.")

for facility in facilities:
    if not os.path.exists(os.path.join(file_dir, ref_facility[0])):
        print('\nNo data for '+ref_facility[1]+' available. Cannot Continue.')
    else:
        if not os.path.exists(os.path.join(file_dir, facility[0])):
            print('\nNo data for '+facility[1]+' available. Skipping.')
        else:
            acceptable_passes = []
            obs = []
            rev_time = []
            longer_passes = []
            availability = []
            # load list of files in facility directory
            file_path = sorted(os.listdir(os.path.join(file_dir, facility[0])))
            if not file_path:
                print('No files selected.')
                quit()
            else:
                file_path = [n for n in file_path if os.path.splitext(n)[1]
                         in extensions]
                file_path = sorted(file_path)
																
            for file_name in file_path: # per satellite
                # get filename for later
                # name_fac = file_name_ref.split('/')[-1].split('.')[0]
                # names_fac.append(name)
            
                # load CSV file
                df = pd.read_csv(os.path.join(file_dir, facility[0], file_name), 
                                                                delimiter=',')
                
                # Remove spaces and duplicate headers
                df = df.loc[~df['Access'].isin(rejection_list)]
                
                # Convert strngs to floating point and datetime
                df['Access'] = pd.to_numeric(df['Access'])
                df['Start Time (UTCG)'] = pd.to_datetime(df['Start Time (UTCG)'])
                df['Stop Time (UTCG)'] = pd.to_datetime(df['Stop Time (UTCG)'])
                df['Duration (sec)'] = pd.to_numeric(df['Duration (sec)'])
                
                # Make start time the index
                df = df.set_index('Start Time (UTCG)')
                df = df.sort()

                df = df.loc[df['Duration (sec)'] > min_duration]

                # Determine if a pass is observable by facility
                #   0: neither
                #   1: DAB
                #   2: Precott
                #   3: Both
                date_matches = []
                for date in date_range:
                    numb_pass = 0
                    for d in df.index:
                        if date.date() == d.date():
                            if numb_pass < 2:
                                numb_pass = numb_pass + 1
                    date_matches.append(numb_pass)

                availability.append(date_matches)

            if show_plots:
                #   1: DAB
                #   2: Precott
                #   3: Both
                interp = 'nearest'
                plots = 3   # reference facility + comparison + total availability 
                                            #   between the it and a each facility in the "facility" list
                plot_numb = 1
                x_lims = mdates.date2num([date_range[0], date_range[-1]])
                y_lims = [0, 69]
                # plot_tics = [[240,260,20], [280,420,20], [805,855,10], [1050,1300,50]]
                fig = plt.figure(figsize=[16,11])
                ax = fig.add_subplot(111)
                ax.spines['top'].set_color('none')
                ax.spines['bottom'].set_color('none')
                ax.spines['left'].set_color('none')
                ax.spines['right'].set_color('none')
                ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
                plt.suptitle('Satellite Availability', fontsize=25)
            
                ax1 = plt.subplot(plots,1,plot_numb)
                plot_numb = plot_numb + 1
                cmap = ListedColormap(['white', 'gray', 'black'], 'indexed')
                plt.title(ref_facility[1], loc='right')
                im = ax1.imshow(ref_facility_availability, cmap=cmap, interpolation=interp,
                                    extent=[x_lims[0], x_lims[1], y_lims[0], y_lims[1]], aspect='auto')
                cbar = plt.colorbar(im, ticks=[0.325, 1, 1.675])
                cbar.ax.set_yticklabels(['No passes', '1 pass', '2 or more passes'])
                ax1.xaxis_date()
                date_format = mdates.DateFormatter('%m/%d')
                ax1.xaxis.set_major_formatter(date_format)
                plt.xlabel('Date (month/day)')
                plt.ylabel('Satellite')

                # Plot availability for 1 year per satellite as heat map
                ax2 = plt.subplot(plots,1,plot_numb)
                plot_numb = plot_numb + 1
#                #   0: neither
#                #   1: DAB
#                #   2: Precott
#                #   3: Both
                cmap = ListedColormap(['white', 'gray', 'black'], 'indexed')
                plt.title(facility[1], loc='right')
                im2 = ax2.imshow(availability, cmap=cmap, interpolation=interp, 
                        extent=[x_lims[0], x_lims[1], y_lims[0], y_lims[1]], aspect='auto')
                # cbar = plt.colorbar(im2, ticks=[0.3, 1, 1.7])
                cbar = plt.colorbar(im2, ticks=[0.325, 1, 1.675])
                cbar.ax.set_yticklabels(['No passes', '1 pass', '2 or more passes'])
                ax2.xaxis_date()
                ax2.xaxis.set_major_formatter(date_format)
                plt.xlabel('Date (month/day)')
                plt.ylabel('Satellite')

            print("Completed processing "+facility[0]+".")

            # do comparison between reference and selected facilities
            # [availability, ref_facility_availability]
            total_site_availabiity = []
            for ref, site in zip(ref_facility_availability, availability):
                sat_availability = []
                for ref_sat, site_sat in zip(ref, site):
                    if ref_sat is 0 and site_sat is 0:
                        sat_availability.append(0)
                    if ref_sat > 0 and site_sat is 0:
                        sat_availability.append(1)
                    if ref_sat is 0 and site_sat > 0:
                        sat_availability.append(2)
                    if ref_sat > 0 and site_sat > 0:
                        sat_availability.append(3)
                total_site_availabiity.append(sat_availability)
                        
            if show_plots:
                # plot comparison plot
                ax3 = plt.subplot(plots,1,plot_numb)
                plot_numb = plot_numb + 1
                plt.title('Total Availability', loc='right')
                im3 = ax3.imshow(total_site_availabiity, cmap=cmap, interpolation=interp, 
                        extent=[x_lims[0], x_lims[1], y_lims[0], y_lims[1]], aspect='auto')
                cbar = plt.colorbar(im3, ticks=[0.5, 1.5, 2.5])
                cbar.ax.set_yticklabels(['Not available', 'Available from one site', 'Available from both sites'])
                ax3.xaxis_date()
                ax3.xaxis.set_major_formatter(date_format)
                plt.xlabel('Date (month/day)')
                plt.ylabel('Satellite')
            
                # finish parameters
                pad_length = 0
                # ax.xaxis_date()
                # ax.xaxis.set_major_formatter(date_format) ##### Move this to each plot
                # fig.autofmt_xdate(rotation=45)  
                ax.set_xlabel('Date', labelpad=pad_length)
                ax.set_ylabel('Satellite Number', labelpad=pad_length)
                fig.subplots_adjust(wspace=0.4, hspace=0.5)
                plt.savefig(save_dir+'sat_availability_'+facility[0]+'.pdf', format = 'pdf')
                print("Plotted "+facility[0]+".")
                # plt.show()
                    