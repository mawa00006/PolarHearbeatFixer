import numpy as np
import matplotlib.pyplot as plt
import json
import os
import argparse
from tqdm import tqdm

def get_HRmax():
    '''
    Read maximum heart rate from activity file
    '''
    files = os.listdir('data')
    for file in files:
        if file.startswith('activity'):
            data = json.load(open(os.path.join('data', file)))
            try:
                HRmax = data['physicalInformation']['maximumHeartRate']
            except:
                HRmax = input('No HRmax found, please enter manually:')
            break

    return int(HRmax)

def calculate_resolution_mean(lst, k):
    result = []
    n = len(lst)
    i = 0
    k = int(k)
    while i < n:
        sub_lst = lst[i:i+k]
        mean = sum(sub_lst) / len(sub_lst)
        result.append(mean)
        i += k
    return result

def plot_training(HRmax, heartrates, session_name, resolution):

    out_dir = os.path.join('plots', session_name+'_res_'+str(resolution)+'s')

    hr_intervals = [int(HRmax*x) for x in [1, 0.9, 0.8, 0.7, 0.6, 0.5]]

    heartrates = calculate_resolution_mean(heartrates, resolution)
    mean_heartrate = np.nanmean(heartrates)
    hr_intervals.append(mean_heartrate)
    fig, ax = plt.subplots()

    ax.margins(0)

    plt.ylim((hr_intervals[-1]-40, HRmax))

    ax.set_yticks(hr_intervals)
    ax.axhspan(hr_intervals[1],hr_intervals[0], facecolor='tomato', alpha =1)
    ax.axhspan(hr_intervals[2], hr_intervals[1], facecolor='gold', alpha=1)
    ax.axhspan(hr_intervals[3], hr_intervals[2], facecolor='yellowgreen', alpha=1)
    ax.axhspan(hr_intervals[4], hr_intervals[3], facecolor='lightblue', alpha=1)
    ax.axhspan(hr_intervals[5], hr_intervals[4], facecolor='silver', alpha=1)

    plt.axhline(y=mean_heartrate)
    plt.title(session_name)
    plt.ylabel('S/min')
    plt.xlabel(f'Training duration, Resolution: {resolution}s')

    plt.plot(heartrates, color='red')
    plt.savefig(out_dir)
    plt.close()




parser = argparse.ArgumentParser()
parser.add_argument('-a', '--all', action='store_true', help='If given plots for all training sessions are calculated')
parser.add_argument('-d', '--date', type=str, default=None, help='Date of the training session. Format: Year-month-day (Example: 2023-10-19)')
parser.add_argument('-t', '--time', type=str, default=None, help='Time of the training session. Format: hour:minute (Example: 15:31)')
parser.add_argument('-r', '--resolution', type=int, default=60, help='Temporal resolution of the plot in seconds')

args = vars(parser.parse_args())
HRmax = get_HRmax()
resolution = int(args['resolution'])

os.makedirs('plots', exist_ok=True)


if args['all']:
    session_names = os.listdir('fixed_data')

else:
    date = args['date']
    time = args['date']

    all_sessions = os.listdir('fixed_data')
    if date == None or time == None:
        raise Exception('Please specify date and time')

    session_names = [f'training-session-{date}T{time}']

    if session_names[0] not in all_sessions:
        raise Exception(f'Training session does not exist, please check date and time again. date:{date}, time:{time}')

for session_name in tqdm(session_names):
    with open(os.path.join('fixed_data',session_name)) as f:

            data = json.load(f)
            heartrate_dicts =data['exercises'][0]['samples']['heartRate']

            heartrates = [int(sample['value']) for sample in heartrate_dicts]

            plot_training(HRmax, heartrates, session_name, resolution)


