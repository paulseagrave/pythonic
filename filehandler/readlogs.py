import json
import os
import datetime
import matplotlib.pyplot as plt
import numpy as numpy
from scipy.interpolate import UnivariateSpline

def file_parse(name):
    '''
    Parse common event
    '''
    all_responses_per_minute ={}

    print('Starting: {}'.format(datetime.datetime.now()))

    with open(filename, 'r') as filehandle:

        for line in filehandle:
            data = json.loads(line)
            request_time = datetime.datetime.fromtimestamp(
                int(data['ts_unix_ms'])/1000
            ).strftime('%Y-%m-%d %H:%M')
            # request_time = int(data['ts_unix_ms'])/1000

            if request_time not in all_responses_per_minute:
                all_responses_per_minute[request_time] = [int(data['attr']['api_response_time'])]
            else:
                all_responses_per_minute[request_time].append(
                    int(data['attr']['api_response_time'])
                )
        filehandle.close()

    return all_responses_per_minute

def calculate_average(values):
    return sum(values)/len(values)

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs({}) to be bigger than window size({}).".format(x.size, window_len))


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s=numpy.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=numpy.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=numpy.convolve(w/w.sum(),s,mode='valid')
    return y

if __name__ == '__main__':
    fname = 'common_event.log.complete'
    current_folder = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filename = os.path.join(current_folder, fname)
    all_responses = file_parse(filename)
    print('File processed: {}'.format(datetime.datetime.now()))
    time_frames = []
    averages = []
    for time_frame in sorted(all_responses):
        time_frames.append(datetime.datetime.strptime(time_frame, '%Y-%m-%d %H:%M'))
        #time_frames.append(time_frame)
        averages.append(calculate_average(all_responses[time_frame]))

    x = numpy.array(time_frames)
    y = numpy.array(averages)

    print('numpy done: {}'.format(datetime.datetime.now()))

    ys = smooth(y)
    print('Smoothy: {}'.format(datetime.datetime.now()))

    ys = ys[:len(x)]
    plt.plot(x, ys)
    plt.show()
