import h5py
import numpy as np
with h5py.File('/mnt/nfs/samba/数据聚变/气象数据/hrrr区域划分实验数据/hrrr_440_24var_lb_mountain/hrrr_nwp_h5_110/01/02.h5') as d1:
    with h5py.File('/mnt/nfs/samba/数据聚变/气象数据/pangu/40_24_440_lb_m/2022/01/10.h5') as d2:
            d1 = d1['fields'][:]  
            d2 = d2['fields'][:]  
            print(d1)
            # print(d1-d2)