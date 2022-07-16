"""
Author: Nazmi Eren Varilci
The main goal is making calculations for my previous material science lab by using pandas, matplotlib and numpy
libraries to learn basics of data manipulation. Then by using the main idea here, I will automate the process with some dynamic approach.
However, the usage here would be static, and will contain some very spesific variable names, calculations, list manipulations etc.

Data is given by Middle East Technical University for the course content of CE241 - Material Science on 29 November 2021. 
"""



import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

# Dimensions of Cylindirical Concrete Sample in mm
diameter = 100
gage_height = 130
area = math.pi * (diameter/2)**2


def find_loading_start(data_list : list):
    after_unloading = True # Also for first condition
    loading_start_list = []
    for i in range(len(data_list) - 1):
        if abs(data_list[i]) < abs(data_list[i+1]) and after_unloading == True:
            loading_start_list.append([i, data_list[i]])
            after_unloading = False
        elif abs(data_list[i]) > abs(data_list[i+1]):
            after_unloading = True
    return loading_start_list

def find_unloading_start(data_list : list):
    
    after_loading = True # Also for first condition
    unloading_start_list = []
    for i in range(len(data_list) - 1):
        if abs(data_list[i]) > abs(data_list[i+1]) and after_loading == True:
            unloading_start_list.append([i, data_list[i]])
            after_loading = False
        elif abs(data_list[i]) < abs(data_list[i+1]):
            after_loading = True
    return unloading_start_list


#df = pd.read_excel("Lab1_group1.xlsx")
# print(df)

# Dropping unwawnted rows
"""
df.drop([], axis = 0, inplace=True)
print(df)"""

# Better Approach More Dynamic I suppose

df = pd.read_excel("Lab1_group1.xlsx", skiprows=3) 
# df = pd.read_excel('your_excel_file.xls', header=3, skipfooter=4) # To say not take first 3 and last 4 row since they contain some 
# prior information about data who collect them etc.  

"""Sometimes we need to drop first 2-3 rows like at this example 
The problem here is how do we now may be the first row is our intended 
header row so do we need to check every excel file before 
making a decision. Yes I can make a variable for skiprows with some button text entries 
etc. but I may need a preview of excel file right after implenting the file. 
"""
# print(df) #-> Obtained intended dataframe
"""
          Time   Axial Force Ext. LVDT #1 Ext. LVDT #2 Axial COD
0            s             N           mm           mm        mm
1     1.078613  -2901.632834    -0.002412    -0.000142  0.000442
2      2.07959  -5911.431926     -0.00425    -0.000829  0.000906
3     3.080566  -8928.003084    -0.005611    -0.002075  0.001322
4     4.081543 -11925.812899    -0.006664    -0.003655    0.0017
..         ...           ...          ...          ...       ...
295  295.36572 -14280.519253    -0.008637    -0.006693  0.002865
296   296.3667 -11283.345073    -0.007773    -0.004682  0.002398
297  297.36768  -8275.287521    -0.006836    -0.002554  0.001939
298  298.36865  -5279.379105    -0.005751    -0.000545  0.001517
299  299.36963  -2284.262981    -0.004046     0.000828   0.00109
"""

column_names = df.columns.tolist() # Columns to List
#print(column_names) 
"""
['Time', 'Axial Force', 'Ext. LVDT #1', 'Ext. LVDT #2', 'Axial COD']
"""

data_list = []
unit_list = []
for i in column_names:
    temp_list = df[i].values.tolist()
    unit_list.append(temp_list[0])
    temp_list = temp_list[1:]
    """
    Every first value at each list is unit like s means second for Time N for Axial Force etc.  
    """

    data_list.append(temp_list)
"""
print(data_list[0][0:5])
print(unit_list[0]) to check correctness with limited data"""

indexes = len(data_list[0])
# print(indexes) -> 299 Entity Okey

calculated_values = []
for i in range(indexes):  # Tried 3 for correctness
    temp_list = []
    """
    For every entity find stress
    average deformation
    axial strain
    """
    stress = data_list[column_names.index('Axial Force')][i] / area
    average_deformation = (data_list[column_names.index('Ext. LVDT #1')][i] + data_list[column_names.index('Ext. LVDT #2')][i])/2
    axial_strain = average_deformation/gage_height
    cod_def = data_list[column_names.index('Axial COD')][i]*0.44/1
    temp_list.append(stress)
    temp_list.append(average_deformation)
    temp_list.append(axial_strain)
    temp_list.append(cod_def)
    calculated_values.append(temp_list)
    """
    Learn Numpy and use it because it is more memory and time effective
    """
# print(calculated_values)
"""
[[[-18.721671328328664, -0.0562666104254311, -0.00043282008019562384]], 
 [[-18.340553770445446, -0.055370711709642834, -0.0004259285516126372]], 
 [[-17.959252682721296, -0.05448759279659079, -0.00041913532920454454]]]
"""
calculated_values = np.array(calculated_values).T.tolist()
# print(calculated_values)
# print(calculated_values)
"""
[[[-18.721671328328664, -18.340553770445446, -17.959252682721296]], 
[[-0.0562666104254311, -0.055370711709642834, -0.05448759279659079]], 
[[-0.00043282008019562384, -0.0004259285516126372, -0.00041913532920454454]]]
"""

# Appending necessary column names to the column list
column_names.append("stress")
column_names.append("average_deformation")
column_names.append("axial_strain")
column_names.append("longtitudinal_def")
# print(column_names)
"""
['Time', 'Axial Force', 'Ext. LVDT #1', 'Ext. LVDT #2', 'Axial COD', 'stress', 'average_deformation', 'axial_strain', 'longtitudinal_def']
I have calculated stress, average_deformation and axial_strain up until now
"""

for i in calculated_values:
    data_list.append(i)

"""pdf = pd.DataFrame(np.array(data_list).T, columns=column_names)

data_list 
[[299 entity],  -> time
 [299 entity],  -> Force
  .             -> LVDT1, LVDT2, axial cod, stress, average deformation, axial strain 
  .
  .
  Total 8 rows] so shape is (8,299) but we need other way around at this time at the begining of the script
  while we taking individual data at each column we change the dimensions in a sense

print(pdf)

           Time   Axial Force  Ext. LVDT #1  Ext. LVDT #2  Axial COD    stress  average_deformation  axial_strain
0      1.078613  -2901.632834     -0.002412     -0.000142   0.000442 -0.369447            -0.001277     -0.000010
1      2.079590  -5911.431926     -0.004250     -0.000829   0.000906 -0.752667            -0.002540     -0.000020
2      3.080566  -8928.003084     -0.005611     -0.002075   0.001322 -1.136749            -0.003843     -0.000030
3      4.081543 -11925.812899     -0.006664     -0.003655   0.001700 -1.518442            -0.005159     -0.000040
4      5.082520 -14942.406479     -0.007444     -0.005500   0.002165 -1.902526            -0.006472     -0.000050
..          ...           ...           ...           ...        ...       ...                  ...           ...
294  295.365720 -14280.519253     -0.008637     -0.006693   0.002865 -1.818252            -0.007665     -0.000059
295  296.366700 -11283.345073     -0.007773     -0.004682   0.002398 -1.436640            -0.006228     -0.000048
296  297.367680  -8275.287521     -0.006836     -0.002554   0.001939 -1.053642            -0.004695     -0.000036
297  298.368650  -5279.379105     -0.005751     -0.000545   0.001517 -0.672191            -0.003148     -0.000024
298  299.369630  -2284.262981     -0.004046      0.000828   0.001090 -0.290841            -0.001609     -0.000012

Everything is Ok
"""

stresses = data_list[column_names.index("stress")]
axial_strain = data_list[column_names.index("axial_strain")]
transverse_strain = data_list[column_names.index('Axial COD')]


loading_list = find_loading_start(data_list[column_names.index('Axial Force')])
unloading_list = find_unloading_start(data_list[column_names.index('Axial Force')])
"""
[[0, -2901.6328341000003], [99, -252.59981746999998], [199, -568.4486808]] Start Loading Phase
[[49, -150059.15925], [149, -149707.00745], [249, -149404.78553]] Start Unloading Phase
"""

print(len(stresses[loading_list[1][0]: unloading_list[1][0] - 1]))
print(len(axial_strain[loading_list[1][0]: unloading_list[1][0] - 1]))

fig, axs = plt.subplots(2,2, figsize=(13,8))

fig.suptitle("CE241 LAB1")
axs[0,0].plot(axial_strain[loading_list[1][0]: unloading_list[1][0] - 1], stresses[loading_list[1][0]: unloading_list[1][0] - 1])
axs[0,0].set_title("Second Loading")
axs[0,0].set_xlabel("Axial Strain(-)")
axs[0,0].set_ylabel("Stress(MPa)")
axs[0,1].plot(axial_strain[loading_list[2][0]: unloading_list[2][0] - 1], stresses[loading_list[2][0]: unloading_list[2][0] - 1])
axs[0,1].set_title("Third Loading")
axs[0,1].set_xlabel("Axial Strain(-)")
axs[0,1].set_ylabel("Stress(MPa)")
axs[1,0].plot(axial_strain[loading_list[1][0]: unloading_list[1][0] - 1], transverse_strain[loading_list[1][0]: unloading_list[1][0] - 1])
axs[1,0].set_title("Transverse vs axial second")
axs[1,0].set_xlabel("Axial Strain(-)")
axs[1,0].set_ylabel("Transverse Strain(-)")
axs[1,1].plot(axial_strain[loading_list[2][0]: unloading_list[2][0] - 1], transverse_strain[loading_list[2][0]: unloading_list[2][0] - 1])
axs[1,1].set_title("Transverse vs axial third")
axs[1,1].set_xlabel("Axial Strain(-)")
axs[1,1].set_ylabel("Transverse Strain(-)")



plt.subplots_adjust(wspace=0.6,hspace=0.6)
plt.savefig("loadings.png")
plt.show()