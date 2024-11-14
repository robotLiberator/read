import pygrib
import h5py
import os
import glob
import numpy as np
from datetime import datetime, timedelta

variables = {
    'Geopotential height': [50,500,850,1000,'isobaricInhPa'],
    'Temperature': [2,50,500,850,1000,'isobaricInhPa','heightAboveGround'],
    'Specific humidity': [50,500,850,1000,'isobaricInhPa'],
    'u-component of wind': [10,50,500,850,1000,'isobaricInhPa','heightAboveGround'],
    'v-component of wind': [10,50,500,850,1000,'isobaricInhPa','heightAboveGround'],
    '198':[0,'meanSea'],
    # 'Downward long-wave radiation flux':[0,'surface'],
    # 'Name:Downward short-wave radiation flux':[0,'surface']
} 


father_path = '/mnt/nfs/samba/数据聚变/气象数据/hrrr_nwp_grib'


def grib2h5(year, month, day):
    #创建一个形状为(48, 24, 440, 408)的全0数组
    outdata = np.zeros((48, 24, 440, 408), dtype=np.float32)  # 指定数据类型为float32
    for hour in range(48):
        
        # file_path = father_path + '/'+year+'/'+month+'/'+day+'/hrrr.t00z.wrfprsf'+str(hour+1).zfill(2)+'.grib2'
        file_path = father_path + '/'+year+'/'+month+'/'+day+'/hrrr_'+year+month+day+'_hrrr_t00z_wrfprsf'+str(hour+1).zfill(2)+'.grib2'

        # '/mnt/nfs/samba/数据聚变/气象数据/hrrr_nwp_grib/2023/1/1/hrrr.t00z.wrfprsf01.grib2'
        # hrrr_20240101_hrrr_t00z_wrfprsf00.grib2

        gri = pygrib.open(file_path.encode('utf-8'))  # 打开 GRIB 文件


        i = 0
        # hour = 0

        for message in gri:
            # 获取变量名称和层次值
            variable_name = message.parameterName
            level = message.level
            level_type = message.typeOfLevel
            # print("var_name:",variable_name, "level:",level, "level_type:",level_type)
            # print(message.values.shape)
            
            # 这里可以优化，直接去取就好了，不需要遍历
            if variable_name in variables and level in variables[variable_name] and level_type in variables[variable_name]:
                outdata[hour, i, :, :] = np.float32(message.values)[252:252+440,969:969+408]#rb
                # outdata[hour, i, :, :] = np.float32(message.values)[252:252+440,969-408:969]#lb_m

         
                i += 1
        gri.close()  # 释放资源


    
    # 改顺序
        
    a = [0, 5, 10, 20, 1, 6, 11, 15, 2, 7, 12, 16, 3, 8, 13, 17, 4, 9, 14, 18, 19, 22, 23, 21]
    j = 0
    n_outdata = np.zeros((48, 24, 440, 408), dtype=np.float32)  # 定义变量个数24
    for nj in a:
        n_outdata[:, j, :, :] = outdata[:, nj, :, :]
        j += 1



    # output_file_path = '/mnt/nfs/samba/数据聚变/气象数据/hrrr_nwp_h5/2023/1/1.h5'
    
    output_file_path = '/mnt/nfs/samba/数据聚变/气象数据/hrrr_440_24var_rb/hrrr_nwp_h5/'+year+'/'+month.zfill(2)+'/'
    
    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)
    
    output_file_path = output_file_path + day.zfill(2)+'.h5'
    with h5py.File(output_file_path, 'w') as h5_file:
        # 创建一个名为'data'的数据集，将数据写入其中
        h5_file.create_dataset('fields', data = n_outdata) 



    
    return




def iterate_year(year):
    #2024_lb_m年搞到3月3号了
    start_date = datetime(year, 1, 1, 00)  # 设置开始日期
    end_date = datetime(year, 3, 3, 23)  # 设置结束日期

    current_date = start_date
    while current_date <= end_date:
        
        
        
        grib2h5(str(current_date.year).zfill(2), str(current_date.month).zfill(2), str(current_date.day).zfill(2))
        print(str(current_date.year), str(current_date.month), str(current_date.day))
        current_date += timedelta(days=1)
    
    return 

iterate_year(2024)  