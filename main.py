"""
Generate and TX samples using a set of waveforms, and waveform characteristics
"""

import argparse
import numpy as np
import uhd
from uhd import types 

WAVEFORMS = {
    "sine": lambda n, tone_offset, rate: np.exp(n * 2j * np.pi * tone_offset / rate),
    "square": lambda n, tone_offset, rate: np.sign(WAVEFORMS["sine"](n, tone_offset, rate)),
    "const": lambda n, tone_offset, rate: 1 + 1j,
    "ramp": lambda n, tone_offset, rate:
            2*(n*(tone_offset/rate) - np.floor(float(0.5 + n*(tone_offset/rate))))
}

def parse_argsRX():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--args", default="", type=str)
    parser.add_argument("-o", "--output-file", default="receive.dat",type=str)#, required=True)
    parser.add_argument("-f", "--freq", default=1e6, type=float)#, required=True)
    parser.add_argument("-r", "--rate", default=1e6, type=float)
    parser.add_argument("-d", "--duration", default=5.0, type=float)
    parser.add_argument("-c", "--channels", default=0, nargs="+", type=int)
    parser.add_argument("-g", "--gain", type=int, default=10)
    parser.add_argument("-n", "--numpy", default=False, action="store_true",
                        help="Save output file in NumPy format (default: No)")
    return parser.parse_args()
    
def parse_argsTX():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--args", default="", type=str)
    parser.add_argument(
        "-w", "--waveform", default="sine", choices=WAVEFORMS.keys(), type=str)
    parser.add_argument("-f", "--freq", default=1e6, type=float)#, required=True)
    parser.add_argument("-r", "--rate", default=1e6, type=float)
    parser.add_argument("-d", "--duration", default=5.0, type=float)
    parser.add_argument("-c", "--channels", default=0, nargs="+", type=int)
    parser.add_argument("-g", "--gain", type=int, default=10)
    parser.add_argument("--wave-freq", default=1e4, type=float)
    parser.add_argument("--wave-ampl", default=0.3, type=float)
    return parser.parse_args()


def TX():
    """TX samples based on input arguments"""
    file = open('tone3.csv')
    rawdata = np.loadtxt(file, delimiter = ",")
    args = parse_argsTX()
    usrp = uhd.usrp.MultiUSRP(args.args)
    txtime = usrp.get_time_now() 
    print("TESTSTADTADFZSDFASDFASDF")
    print(str(txtime.get_real_secs()))
    if not isinstance(args.channels, list):
        args.channels = [args.channels]
    data = np.array(
        list(map(lambda n: args.wave_ampl * WAVEFORMS[args.waveform](n, args.wave_freq, args.rate),
                 np.arange(
                     int(10 * np.floor(args.rate / args.wave_freq)),
                     dtype=np.complex64))),
        dtype=np.complex64)  # One period
    print("Transmitting")
    usrp.send_waveform(rawdata, args.duration, args.freq, args.rate,
                       args.channels, args.gain, start_time = txtime + types.TimeSpec(10.0))
    np.save()
    print("Done")
    time = usrp.get_time_now()
    print(str(time.get_real_secs()))

def RX():
    """RX samples and write to file"""
    args = parse_argsRX()
    usrp = uhd.usrp.MultiUSRP(args.args)
    num_samps = int(np.ceil(args.duration*args.rate))
    if not isinstance(args.channels, list):
        args.channels = [args.channels]
    samps = usrp.recv_num_samps(num_samps, args.freq, args.rate, args.channels, args.gain)
    with open(args.output_file, 'wb') as out_file:
        if args.numpy:
            np.save(out_file, samps, allow_pickle=False, fix_imports=False)
        else:
            samps.tofile(out_file)

def main():
    TX()
    RX()
    
if __name__ == "__main__":
    main()