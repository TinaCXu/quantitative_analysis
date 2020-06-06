import time
import datetime
import math
import numpy as np
import scipy.optimize as so 
import pandas as pd


input_data = pd.read_excel('简单YTM-input.xlsx', sheet_name='Sheet1')
# print(input_data)
# print(input_data['值'][0])
# print(type(input_data['值'][0]))
# print(input_data['值'][0].timestamp())
# print(type(input_data['值'][0].timestamp()))
# print(input_data['值'][0].strftime("%Y"))
# print(type(input_data['值'][0].strftime("%Y")))

# input
d_s = input_data['值'][0]
d_m = input_data['值'][1]
r_c = input_data['值'][2]
pr = input_data['值'][3]
date_frequency = input_data['值'][4]
cln = input_data['值'][5]

def parseTime(t):
    # 将所有日期统一成时间戳形式
    # t_str = t.split('/')
    # t_timestamp = (int(t_str[0]),int(t_str[1]),int(t_str[2]),0,0,0,0,0,0)
    t_timestamp = t.timestamp()
    # 获得对应的年月日
    t_y = int(t.strftime("%Y"))
    t_m = int(t.strftime("%m"))
    t_d = int(t.strftime("%d"))
    t_str = t.strftime("%Y/%m/%d")
    return t_str, t_timestamp, t_y, t_m, t_d

def getTs(y, m, d):
    t_timestamp = (y, m, d, 0, 0, 0, 0, 0, 0)
    t_timestamp = time.mktime(t_timestamp)
    return t_timestamp

def getDatetime(timestamp):
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    return dt

# def getTstr(timestamp):
#     t_array = time.localtime(timestamp)
#     t_str = time.strftime("%Y/%m/%d", t_array)
#     return t_str

def getNods(y1, m1, d1, y2, m2, d2):
    # from: y1, m1, d1
    # to: y2, m2, d2
    if y1 == 31:
        y1 = 30
    if y2 == 31:
        y2 = 30
    nods = (d2 - d1) + (m2 - m1)*30 + (y2 - y1)*360
    return nods

# 转换并定义时间相关变量
d_s_str, d_s_timestamp, d_s_y, d_s_m, d_s_d = parseTime(d_s)
print(d_s_str, d_s_timestamp, d_s_y, d_s_m, d_s_d)
d_m_str, d_m_timestamp, d_m_y, d_m_m, d_m_d = parseTime(d_m)
print(d_m_str, d_m_timestamp, d_m_y, d_m_m, d_m_d)

# CF output表
# number of periods per year
if date_frequency == 'annual':
    m = 1
    month_laps = 12
if date_frequency == 'semi-annual':
    m = 2
    month_laps = 6
if date_frequency == 'quarterly':
    m = 4
    month_laps = 3
if date_frequency == 'monthly':
    m = 12
    month_laps = 1
print(m)

# CF date
current_m = d_m_m
current_y = d_m_y
current_d = d_m_d
CF_dates = [] 
while getTs(current_y, current_m, current_d) > d_s_timestamp:
    CF_dates.append([current_y, current_m, current_d])
    current_m -= month_laps
    if current_m <= 0:
        current_m = 12 + current_m
        current_y = current_y - 1
print(CF_dates)
# number of remaining cash flows
num_remaining_CF = len(CF_dates)
print(num_remaining_CF)


# CF output dict
# interest
int_per_period = pr*r_c/m 

CF_output_dict = {}
for i in range(1,num_remaining_CF+1):
    CF_output_dict[i] = [getDatetime(getTs(CF_dates[num_remaining_CF-i][0],CF_dates[num_remaining_CF-i][1],CF_dates[num_remaining_CF-i][2])), int_per_period, 0, int_per_period]
# redefine the last CF period
CF_output_dict[num_remaining_CF] = [d_m, int_per_period, 100, 100+int_per_period]
print(CF_output_dict)

# Output dialoge
# clean_bond_price
cbp = pr*cln/100
print(cbp)
#previous cash flow date
prev_m = CF_dates[num_remaining_CF-1][1] - month_laps
prev_y = CF_dates[num_remaining_CF-1][0]
prev_d = CF_dates[num_remaining_CF-1][2]
if prev_m <= 0:
    prev_m = 12 + prev_m
    prev_y = prev_y - 1
prev_cfd_ts = getTs(prev_y, prev_m, prev_d)
prev_cfd = getDatetime(prev_cfd_ts)
print(prev_cfd_ts)
#number of days of accrued interest
nods_of_accr_int = getNods(prev_y, prev_m, prev_d, d_s_y, d_s_m, d_s_d)
print(prev_y, prev_m, prev_d, d_s_y, d_s_m, d_s_d)
print(nods_of_accr_int)
#accrued interest
accr_int =nods_of_accr_int/360*r_c*pr
print(accr_int)
#dirty bond price(includes accrued) 
dbp	= cbp + accr_int
print(dbp)
# duration
# modified duration
#next cash flow date
next_cfd = CF_output_dict[1][0]
# next_cfd = getTstr(next_cfd)
print(next_cfd)
print(type(next_cfd))
# number of days from value date to maturity
delta = d_m - d_s
nods_from_vd_to_matur = delta.days
print(nods_from_vd_to_matur)
# years to maturity
years_to_maturity = getNods(d_s_y, d_s_m, d_s_d, d_m_y, d_m_m, d_m_d)/360
print(years_to_maturity)
#number of days from value date to next cash flow
delta = next_cfd - d_s
nods_from_vd_to_nextcf = delta.days
print(nods_from_vd_to_nextcf)

# time = m*t + i - 1
# m = number of periods per year
# t = time in years from settlement date to next cash flow date
next_cfd_str, next_cfd_timestamp, next_cfd_y, next_cfd_m, next_cfd_d = parseTime(next_cfd)
t = getNods(d_s_y, d_s_m, d_s_d, next_cfd_y, next_cfd_m, next_cfd_d)/360
print(t)

# prepare time & CF list for YTM calculation
CF_time = []
CF_cash = []
for i in range(1, num_remaining_CF+1):
    CF_time.append(m*t + i - 1)
for i in range(1, num_remaining_CF+1):
    CF_cash.append(CF_output_dict[i][3])
print(CF_time)
print(CF_cash)

#YTM
def ytm():
    def f(x):
        eq = '+'.join(
                [
                    str(m*x[0]**(-n)) 
                    for m,n in zip(CF_cash,CF_time)]
            )+'-'+str(dbp)
        print(eq)
        return np.array(eval(eq))
    init_guess = np.array([1.03])   # 初始猜一个
    # root = so.root(f, init_guess) # 
    fsolve = so.fsolve(f, init_guess)
    ytm = (max(fsolve) - 1)*m
    return ytm
YTM = ytm()
print(YTM)

#total discounted CF (should equal to dirty bond price)
def discountCF(CF, i):
    disc_CF = CF / ((1 + YTM/m)**(m*t + i - 1))
    return disc_CF
total_disc_CF = 0
for i in range(1, num_remaining_CF+1):
    disc_CF = discountCF(CF_output_dict[i][3], i)
    total_disc_CF += disc_CF
print(total_disc_CF)

#derivative
def derivative(CF, i):
    deri = (-(m*t+i-1))/(m*(1+YTM/m)**(m*t+i))*CF
    return deri
total_deri = 0
for i in range(1, num_remaining_CF+1):
    deri = derivative(CF_output_dict[i][3], i)
    total_deri += deri
print(total_deri)

#second derivative
def sec_derivative(CF, i):
    sec_deri = (m*t+i-1)*(m*t+i)/(m**2*(1+YTM/m)**(m*t+i+1))*CF
    return sec_deri
total_sec_deri = 0
for i in range(1, num_remaining_CF+1):
    sec_deri = sec_derivative(CF_output_dict[i][3], i)
    total_sec_deri += sec_deri
print(total_sec_deri)

#modified duration
modi_dura =total_deri * -1 / dbp
print(modi_dura)

#modified convexity
modi_conv = total_sec_deri / dbp
print(modi_conv)

#duration
dura = modi_dura*(1+YTM/m)
print(dura)

# basis point value
bpv = dbp *(-modi_dura*0.0001+0.5*modi_conv*(0.0001)**2)
print(bpv)

#yield value change per 1bp increase in price 
yv_change_per1bp_inc_in_price =1/total_deri*0.01*pr/100
print(yv_change_per1bp_inc_in_price)

name = ['yield to maturity', 'clean bond price', 'accured interest', 'dirty bond price (includes accrued)',
'duration', 'modified duration', 'modified convexity', 'basis point value', 'yield value change per 1bp increase in price',
'next cash flow date', 'previous cash flow date', 'number of days from value date to maturity', 'years to maturity',
'number of days from value date to next cash flow', 'number of days of accrued interest', 'number of remaining cash flows']

output_data = [ YTM, cbp, accr_int, dbp, dura, modi_dura, modi_conv, bpv, yv_change_per1bp_inc_in_price, 
next_cfd, prev_cfd, nods_from_vd_to_matur, years_to_maturity, nods_from_vd_to_nextcf, nods_of_accr_int, num_remaining_CF]

# output_data = [ ['yield to maturity', YTM], ['clean bond price', cbp], ['accured interest', accr_int], 
# ['dirty bond price (includes accrued)', dbp], ['duration', dura], ['modified duration', modi_dura], 
# ['modified convexity', modi_conv], ['basis point value', bpv], ['yield value change per 1bp increase in price', yv_change_per1bp_inc_in_price],
# ['next cash flow date', next_cfd], ['previous cash flow date', prev_cfd_ts], ['number of days from value date to maturity', nods_from_vd_to_matur], 
# ['years to maturity', years_to_maturity], ['number of days from value date to next cash flow', nods_from_vd_to_nextcf],
# ['number of days of accrued interest', nods_of_accr_int], ['number of remaining cash flows', num_remaining_CF]]

console = pd.DataFrame({'object': name, 'value': output_data})
print(console)
console.to_csv(r'C:\Users\xucha\Documents\找工作\嘉竹\simpleYTM-output.csv', index = False, encoding='utf_8_sig')

# CF
CF_output = list(CF_output_dict.values())
name2 = ['cash flow date', 'interest', 'principal', 'total CF']
console2 = pd.DataFrame(columns= name2, data= CF_output)
console2.index += 1 
print(console2)
console2.to_csv(r'C:\Users\xucha\Documents\找工作\嘉竹\simpleYTM-output.csv', encoding='utf_8_sig', index_label='No.', mode='a')
