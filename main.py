import json
import os
from tqdm import tqdm


def fix_start(heartrates):
    '''
    Description: If you start your training session in the app before putting on the heartrate sensor
    the recording will have 0 valued leading entries wee need to get rid of

    :param heartrates: List of dicts including recorded heartrate
    :return: number of 0 valued heartrates at start of the session
    '''

    count = 0
    for i, sample in enumerate(heartrates):
        try:
            hr = sample['value']
        except:
            count += 1
            continue
        if hr == 0:
            count += 1
        else: break

    return count


if __name__ == '__main__':

    data_dir = 'data'
    out_dir = 'fixed_data'

    os.makedirs(out_dir, exist_ok=True)

    for file in tqdm(os.listdir(data_dir)):
        #file includes training data

        if file.startswith('training-session'):
            #read data
            data = json.load(open(os.path.join(data_dir, file)))
            #no heart rate recorded
            try:
                #read heart rate data
                heartrates = data['exercises'][0]['samples']['heartRate']
            except:
               continue

            start = fix_start(heartrates)

            heartrates = heartrates[start:]

            fixed_heartrates = []
            mean = []
            flag = False

            #iterate trough heartrates to find 0 valued entries
            for i, sample in enumerate(heartrates):
                #skip first entry


                fixed_sample = {}
                fixed_sample['dateTime'] = sample['dateTime']

                #get recorded heartrate
                try:
                    hr = sample['value']
                # no value recorded (does not happen often)
                except:
                    sample['value'] = fixed_heartrates[i-1]['value']
                    hr = sample['value']

                #incorrect record
                if hr == 0:
                    #get previous (valid) heartrate
                    hr1 = fixed_heartrates[i-1]['value']

                    #find next valid recorded heartrate
                    for x in range(len(heartrates)-i):
                        hr2 = heartrates[i+x]['value']
                        #another missing heartrate
                        if hr2 == 0:
                            #all remaining heartrates are 0
                            #(happens when you take of the heartrate monitor before stopping the training session)
                            if x == len(heartrates)-i-1:
                                flag= True
                                break
                            else: continue

                        #valid hr found
                        #approximate the missing heartrate using mean between two valid entries
                        fixed_hr = (1/2)*(hr1+hr2)
                        fixed_sample['value'] = fixed_hr
                        break
                    if flag:
                        break

                    #save fixed data
                    fixed_heartrates.append(fixed_sample)
                    mean.append(fixed_sample['value'])
                else:
                    #save old (correct) data
                    fixed_heartrates.append(sample)
                    mean.append(sample['value'])


            data['exercises'][0]['samples']['heartRate'] = fixed_heartrates
            data['averageHeartRate'] = sum(mean)/len(mean)

            # save fixed data
            #rename file ('training-session-Year-month-dayThour:minute')
            file_name = 'training-session-' + data['startTime'][:-7]
            with open(os.path.join(out_dir, file_name), 'w') as f:
                json.dump(data, f)

    exit(0)
