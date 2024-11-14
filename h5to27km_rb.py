import xarray as xr
import datetime
from datetime import datetime, timedelta
import os
import numpy as np
from scipy.interpolate import griddata
import h5py as h5py

def interpolate(data, var_num):
    outdata = np.zeros((48, var_num, 49, 52), dtype=np.float32)
    for h in range(48):
        for var in range(var_num):
            global_data = data[h,var,:,:]

            #era5坐标生成
            grid1 = np.linspace(28.75, 40.75 , 49)
            # grid2 = np.linspace(-100, -74.75, 102)
            grid2 = np.linspace(-108, -95.25, 52)
            global_longitudes, global_latitudes = np.meshgrid(grid2, grid1)

            #hrrr的经纬度坐标
            us_x = np.load("lats_lb.npy") 
            us_y = np.load("lons_lb.npy")

            us_temperature_interpolated = griddata(
                (us_x.flatten(), us_y.flatten()),     #兰伯特目标区域hrrr的
                global_data.flatten(),  #经纬度大区域era5的
                (global_latitudes, global_longitudes),
                
                method='nearest',  # 插值方法
                fill_value=np.nan  # 在插值失败的位置填充 NaN
            )

            # print(us_temperature_interpolated.shape)
            outdata[h, var, :, :] = np.float32(us_temperature_interpolated)
    return outdata





def getdata(year, month, day):
    #打开hrrr文件
    with h5py.File('/mnt/nfs/samba/数据聚变/气象数据/hrrr_440_24var_rb/hrrr_nwp_h5/2022/'+month+'/'+day+'.h5') as d1:
        d1 = d1['fields'][:]


    #吧hrrr文件插值到0.25°
        h5_data = interpolate(d1, 24)
    #存下来
        print(sum(sum(sum(sum(np.isnan(h5_data))))))
        hdf5_path = '/mnt/nfs/samba/数据聚变/气象数据/hrrr_440_24var_rb/hrrr_nwp_h5_110/' + month
        if not os.path.exists(hdf5_path):
            os.makedirs(hdf5_path)
        hdf5_file = hdf5_path +"/"+ day+".h5"




        with h5py.File(hdf5_file, "w") as f:
            f.create_dataset("fields", data = h5_data)
        print(hdf5_file )


def iterate_year(year):
    #2024_lb_m年搞到3月3号了
    start_date = datetime(year, 1, 1, 00)  # 设置开始日期
    end_date = datetime(year, 12, 31, 23)  # 设置结束日期

    current_date = start_date
    while current_date <= end_date:
        
        
        
        getdata(str(current_date.year).zfill(2), str(current_date.month).zfill(2), str(current_date.day).zfill(2))
        print(str(current_date.year), str(current_date.month), str(current_date.day))
        current_date += timedelta(days=1)
    
    return 

iterate_year(2022)  






# dataset  = xr.open_zarr('/mnt/nfs/samba/数据聚变/气象数据/pangu/2018-2022_0012_0p25.zarr')


# # 定义保存文件的根目录
# root_dir = '/'


# # 定义要下载的时间范围（2022 年 12 月）
# start_date = datetime(2022, 1, 11, 00)
# end_date = datetime(2022, 12, 31, 23)  # 结束日期为 2023 年 1 月 1 日的零点
# # 筛选出时间范围内的数据
# surface_variables_list = ['mean_sea_level_pressure', '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_temperature']
# upper_air_variables_list = ['geopotential', 'temperature', 'specific_humidity', 'u_component_of_wind', 'v_component_of_wind']
# variables_list = surface_variables_list + upper_air_variables_list


# selected_data = dataset[variables_list].sel(time=slice(start_date, end_date))




# 遍历每个小时（倒着遍历）
# for hour in range(0,len(selected_data['time']),2):
#     # 获取当前小时的数据
#     hour_data = selected_data.isel(time=hour)
    
#     # 获取当前小时对应的日期
#     current_date = start_date + timedelta(hours=hour*12)
    
#     # 构建文件和文件夹的路径
#     year_folder = os.path.join(root_dir, str(current_date.year))
#     month_folder = os.path.join(year_folder, str(current_date.month).zfill(2))
  

    
 



#     surface_data = [ ]
#     upper_air_data = [ ]
#     for var in surface_variables_list:
#         # selected_var = hour_data[var].values[:, 160:270,1040:1142].reshape(40, 1, 110 , 102)
#         selected_var = hour_data[var].values[:, 160:270,1040-60:1142-60].reshape(40, 1, 110 , 102)
#         selected_var = interpolate(selected_var, 1)
#         surface_data.append(selected_var)

#     for var in upper_air_variables_list:
#         # selected_var = hour_data[var].sel(level=[50,500,850,1000 ]).values[:, :, 160:270,1040:1142]
#         selected_var = hour_data[var].sel(level=[50,500,850,1000 ]).values[:, :, 160:270,1040-60:1142-60]
#         selected_var = interpolate(selected_var, 4)
#         upper_air_data.append(selected_var) 

#     surface_data = np.concatenate(surface_data, axis=1)
#     upper_air_data = np.concatenate(upper_air_data, axis=1)
#     h5_data = np.concatenate([ upper_air_data, surface_data], axis=1)


#     print(sum(sum(sum(sum(np.isnan(h5_data))))))
#     hdf5_path = '/mnt/nfs/samba/数据聚变/气象数据/pangu/40_24_110_lb_m/test' + month_folder
#     if not os.path.exists(hdf5_path):
#         os.makedirs(hdf5_path)
#     hdf5_file = hdf5_path +"/"+ str(current_date.day).zfill(2)+".h5"




#     with h5py.File(hdf5_file, "w") as f:
#         f.create_dataset("fields", data = h5_data)
#     print(hdf5_file )




    
