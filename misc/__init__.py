import sys

def roll_lon(da_, lonname='lon'):
    "roll the input DataArray of global coverage data along the longitude dimention by 180 degree, e.g. from 0~360 to -180~180"
    da = da_.roll({lonname: da_[lonname].size//2}, roll_coords=True) #roll array
    if da[lonname].max() > 180:
        #0~360 to -180~180
        lon_new = da[lonname].where(da[lonname]<180, other=da[lonname]-360) #
    else:
        #-180-180 to 0-360
        lon_new = da[lonname].where(da[lonname]>=0, other=da[lonname]+360) #
    da = da.assign_coords({lonname: lon_new.values})

    return da
        
def get_kws_from_argv(key, default=None):
    """get kws from sys.argv, e.g. daname=precip or --danme=precip """
    kws = [s for s in sys.argv if s.startswith(f'{key}=') or s.startswith(f'--{key}=')]
    if kws:
        value = kws[-1].split('=')[-1]
        print(f'{key}={value}')
    else:
        print(f'{key}={default}')
        value = default
    return value

# Function to calculate Roman values
# from: https://www.geeksforgeeks.org/python-program-to-convert-integer-to-roman/
def intToRoman(num):
    # Storing roman values of digits from 0-9
    # when placed at different places
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D",
         "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L",
         "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V",
         "VI", "VII", "VIII", "IX"]

    # Converting to roman
    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]

    ans = (thousands + hundreds +
           tens + ones)
    return ans
