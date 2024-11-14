from datetime import datetime, timedelta
import os
import h5py
import xarray as xr
import numpy as np

def nc2h5(year, month, day):
    root = '/mnt/nfs/samba/数据聚变/气象数据/hrrr区域划分实验数据/hrrr_440_24var_lb_mountain/era5'
    with xr.open_dataset(root+'/'+year+'/'+month+'/'+day+'/'+'/'+'_upper_air_data.nc', engine='netcdf4') as ds1, \
            xr.open_dataset(root+'/'+year+'/'+month+'/'+day+'/'+'/'+'_surface_data.nc', engine='netcdf4') as ds2:
            surface_variables_list = ['msl', 'u10', 'v10', 't2m']
            upper_air_variables_list = ['z', 't', 'q', 'u', 'v']

            # 提取所有变量的数据
            data_vars1 = [ds1[var_name].values[:,[-9,15,6,0], :-1,:] for var_name in upper_air_variables_list]
            data_vars2 = [ds2[var_name].values[:,:-1,:].reshape(24,1,110,102) for var_name in surface_variables_list]



            # 将所有数据变量堆叠成一个大张量
            combined_data = np.concatenate(data_vars1+data_vars2, axis=1)



            hdf5_path = '/mnt/nfs/samba/数据聚变/气象数据/hrrr区域划分实验数据/hrrr_440_24var_lb_mountain/era5_h5/'+year+'/'+month
            if not os.path.exists(hdf5_path):
                os.makedirs(hdf5_path)
            hdf5_file = hdf5_path +'/'+day+'.h5'
            print(hdf5_file)
            with h5py.File(hdf5_file, "w") as f:
                f.create_dataset("fields", data = combined_data )


def iterate_year(year):
    start_date = datetime(year, 9, 1, 00)  # 设置开始日期
    end_date = datetime(year, 12, 31, 23)  # 设置结束日期

    current_date = start_date
    while current_date <= end_date:
        
        
        # year, month, day, hour = current_date.strftime("%Y-%m-%d-%h").split("-")

        nc2h5(str(current_date.year), str(current_date.month).zfill(2), str(current_date.day).zfill(2))
        current_date += timedelta(days=1)
    
    return 






# 测试代码
iterate_year(2022)