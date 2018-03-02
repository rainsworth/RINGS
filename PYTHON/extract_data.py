
import numpy as np
import io,json
import pylab

# https://zenodo.org/record/1173127#.WpcPQK2cbSA
infile="DD6001_001_20171220_avg_1407+284.ms"

tb.open(infile)

time = tb.getcol('TIME')
ant1 = tb.getcol('ANTENNA1')
ant2 = tb.getcol('ANTENNA2')
data = tb.getcol('DATA')
flag = tb.getcol('FLAG')
desc = tb.getcol('DATA_DESC_ID')
sigma = tb.getcol('SIGMA')

tb.close()

pols = [0,3]  # RR
dataframe=[]
for i in range(0,time.shape[0]):
    for j in pols:
        dict1={}
        dict1['timestamp'] = time[i]
        dict1['antenna1'] = str(ant1[i])
        dict1['antenna2'] = str(ant2[i])
        dict1['spw'] = str(desc[i])
        dict1['polarization'] = str(j)
        #dict1['real'] = list(0.5*(data[0,0:128,i].real + data[3,0:128,i].real))   # create Stokes I as (RR+LL)/2
        #dict1['imag'] = list(0.5*(data[0,0:128,i].imag + data[3,0:128,i].imag))   # create Stokes I as (RR+LL)/2
        dict1['real'] = list(data[j, 0:128, i].real)
        dict1['imag'] = list(data[j, 0:128, i].imag)
        dict1['sigma'] = sigma[0,i]
        dict1['flags'] = list(flag[0,0:128,i]*1.)

        dataframe.append(dict1)

jsonfile = "emerlin_data.json"
with io.open(jsonfile, 'w', encoding='utf-8') as f: 
    output = json.dumps(dataframe, ensure_ascii=False)
    f.write(unicode(output))

