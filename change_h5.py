# import netCDF4
import numpy as np
from scipy.interpolate import griddata
import h5py as h5
import os
import glob
import numpy as np
from datetime import datetime, timedelta

# with h5.File('/nfs/samba/数据聚变/气象数据/hrrr区域划分实验数据/hrrr_440_24var_lb_mountain/geo.h5') as geo:
#             geo = geo['fields'][:]  


# '/mnt/nfs/samba/数据聚变/气象数据/era5_rb_24var/440/'+year+'/'+month.zfill(2)+'/'


def change_h5(year, month, day):
    with h5.File('/mnt/nfs/samba/数据聚变/气象数据/era5_rb_24var/440/'+year+'/'+month.zfill(2)+'/'+day.zfill(2)+'.h5') as era5_data:
        era5_data = era5_data['fields'][:]          
        temp = era5_data[:,19,:,:].copy()  # 创建副本
        era5_data[:,19,:,:] = era5_data[:,20,:,:].copy()
        era5_data[:,20,:,:] = temp
        output_file_path = '/mnt/nfs/samba/数据聚变/气象数据/era5_rb_24var/440/change/'+year+'/'+month.zfill(2)+'/'

        if not os.path.exists(output_file_path):
            os.makedirs(output_file_path)
        
        output_file_path = output_file_path + day.zfill(2)+'.h5'
        with h5.File(output_file_path, 'w') as h5_file:
            # 创建一个名为'data'的数据集，将数据写入其中
            h5_file.create_dataset('fields', data =   era5_data) 


    
    return 

def iterate_year(year):
    start_date = datetime(year, 1, 1, 00)  # 设置开始日期
    end_date = datetime(year, 12, 31, 23)  # 设置结束日期

    current_date = start_date
    while current_date <= end_date:
        
        
        
        change_h5(str(current_date.year), str(current_date.month).zfill(2), str(current_date.day).zfill(2))
        print(str(current_date.year), str(current_date.month).zfill(2), str(current_date.day).zfill(2))
        current_date += timedelta(days=1)
    
    return 

iterate_year(2019)  