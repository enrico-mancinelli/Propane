import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import ccgfilt
# create the ccgfilt object

#df= pd.read_csv("testdata.txt", sep="\s+", header=None)
#xp = df[0]
#yp = df[1]

CO2_df = pd.read_csv("Dataco2.csv", sep= ",")
CO2_df["datetime"] = [datetime.datetime(CO2_df["Year"][i],CO2_df["Month"][i],CO2_df["Day"][i],CO2_df["Hour"][i],CO2_df["Minute"][i]) for i in range(len(CO2_df))]
CO2_df = CO2_df[["datetime","co2"]]
CO2_df = CO2_df.dropna()
CO2_df["index"] = [i for i in range(len(CO2_df))]
CO2_df = CO2_df.set_index('index')
#print(CO2_df.head())
CO2_df['decimal_date']= [CO2_df["datetime"][i].year+ (CO2_df["datetime"][i].dayofyear-1 + CO2_df["datetime"][i].hour/24) /365 for i in range(len(CO2_df))]

xp = CO2_df["decimal_date"]
yp = CO2_df["co2"]

#print(xp[0:10])
filt = ccgfilt.ccgFilter(xp, yp, shortterm=80, longterm = 667, sampleinterval=0, numpolyterms=3, numharmonics=4, timezero=-1, gap=0, debug=False)
#
mm = filt.getMonthlyMeans()
amps = filt.getAmplitudes()
tcup, tcdown = filt.getTrendCrossingDates()

# get x,y data for plotting
x0 = filt.xinterp
y1 = filt.getFunctionValue(x0)
y2 = filt.getPolyValue(x0)
y3 = filt.getSmoothValue(x0)
y4 = filt.getTrendValue(x0)
# Seasonal Cycle
# x and y are original data points
trend = filt.getTrendValue(x0)
detrend = y3 - trend
harmonics = filt.getHarmonicValue(x0)
smooth_cycle = harmonics + filt.smooth - filt.trend
# residuals from the function
resid_from_func = filt.resid
# smoothed residuals
resid_smooth = filt.smooth
# trend of residuals
resid_trend = filt.trend
# residuals about the smoothed line
resid_from_smooth = filt.yp - filt.getSmoothValue(xp)
# equally spaced interpolated data with function removed
x1 = filt.xinterp
y9 = filt.yinterp

plt.plot(xp,yp,"bo",markersize=3,markeredgecolor="k",label="observations")
plt.plot(x0,y1,"red",label="smooth curve")
#plt.plot(x0,y3,"blue",label="smooth plot")
#plt.plot(x0,y4,"orange")
plt.plot(x0,trend,"green",label="trend curve")
plt.xlabel("Year")
plt.ylabel("CO2(ppm)")
#plt.plot(x0,detrend,"red",label="detrend")
plt.legend()
plt.savefig("co2_trend.png", dpi=300)
#plt.show()

# plt.plot(x0,detrend,"red",label="detrend")
# plt.xlabel("Year")
# plt.ylabel("CO2(ppm)")
# plt.legend()
# plt.savefig("co2_detrend.png", dpi=300)
#plt.show()