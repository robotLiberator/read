# import netCDF4
import numpy as np
from scipy.interpolate import griddata
import h5py as h5
import os
import glob
import numpy as np
from datetime import datetime, timedelta

def tohrrr(year, month, day):

    outdata = np.zeros((24, 24, 440, 408), dtype=np.float32)
    #他只能切二维的
    with h5.File('/mnt/nfs/samba/数据聚变/气象数据/era5_rb_24var/train/'+year+'/'+month+'/'+day+'.h5') as data:
        for h in range(24):
            for var in range(24):
                global_data = data["fields"][h,var]

                #era5坐标生成
                grid1 = np.linspace(50,22.75 , 110)
                grid2 = np.linspace(-100, -74.75, 102)
                global_longitudes, global_latitudes = np.meshgrid(grid2, grid1)

                #hrrr的经纬度坐标
                us_x = np.load("hrrr_lats.npy") 
                us_y = np.load("hrrr_lons.npy")

                us_temperature_interpolated = griddata(
                    (global_latitudes.flatten(), global_longitudes.flatten()),
                    global_data.flatten(),  #经纬度大区域era5的
                    (us_x, us_y),     #兰伯特目标区域hrrr的
                    method='linear',  # 插值方法
                    fill_value=np.nan  # 在插值失败的位置填充 NaN
                )

                # print(us_temperature_interpolated.shape)
                outdata[h, var, :, :] = np.float32(us_temperature_interpolated)

        # 从18年开始是新顺序
        a = [0, 1, 2, 3,  8, 9, 10, 11, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18, 19,  23, 20, 21, 22]
        # a = [0, 1, 2, 3,  8, 9, 10, 11, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18,  23, 19, 20, 21, 22]
        j = 0
        n_outdata = np.zeros((24, 24, 440, 408), dtype=np.float32)  # 定义变量个数24
        for nj in a:
            n_outdata[:, j, :, :] = outdata[:, nj, :, :]
            j += 1

        output_file_path = '/mnt/nfs/samba/数据聚变/气象数据/era5_rb_24var/440/'+year+'/'+month.zfill(2)+'/'

        if not os.path.exists(output_file_path):
            os.makedirs(output_file_path)
        
        output_file_path = output_file_path + day.zfill(2)+'.h5'
        with h5.File(output_file_path, 'w') as h5_file:
            # 创建一个名为'data'的数据集，将数据写入其中
            h5_file.create_dataset('fields', data =  n_outdata) 



    


def iterate_year(year):
    start_date = datetime(year, 1, 1, 00)  # 设置开始日期
    end_date = datetime(year, 12, 31, 23)  # 设置结束日期

    current_date = start_date
    while current_date <= end_date:
        
        
        
        tohrrr(str(current_date.year), str(current_date.month).zfill(2), str(current_date.day).zfill(2))
        print(str(current_date.year), str(current_date.month).zfill(2), str(current_date.day).zfill(2))
        current_date += timedelta(days=1)
    
    return 
# for year in range(2020,2014,-1):

#     # 测试代码
#     iterate_year(year)
iterate_year(2015)  