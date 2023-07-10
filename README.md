# PolarHeartbeatFixer

I use a Polar OH1 optical heart rate sensor to monitor my heart rate during training. Sometimes it moves/turns around and does not record data for a few seconds resulting in a messy graphical representation. 

![Alt text](https://github.com/mawa00006/PolarHearbeatFixer/blob/main/images/PolarHeartbeat.jpg?raw=true)

By fixing the data we can get cleaner graphics

![Alt text](https://github.com/mawa00006/PolarHearbeatFixer/blob/main/plots/training-session-2023-06-02T18:34_res_60s.png?raw=true)

## Downloading the data

You can download all of your training data from Polar by following this guide:

`https://support.polar.com/en/how-to-download-all-your-data-from-polar-flow`
This might take a while...

After downloading the data put all files into to `data` folder.


## Fixing the data

To fix the data run

`python main.py`

The missing heart rate values are approximated by calculating the mean of the last recorded heart rate before the missing value and the next recorded heart rate after the missing value. This approximation might not be perfect for large gaps with a huge difference in the last and next heart rate value but for our case it is sufficient.

## Visualizing the data

To visualize all training sessions run

`python visualize.py -a`

If you only want to visualize the data for a specific training session use

`python visualize.py --date year-month-day --time hour:minute`

You can also change the temporal resolution of the graphic in seconds using resolution `-resolution`. 



