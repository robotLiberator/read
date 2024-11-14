# import netCDF4
import numpy as np
from scipy.interpolate import griddata
import h5py as h5




#他只能切二维的
with h5.File("/mnt/nfs/samba/数据聚变/气象数据/era5_rb_24var/test/2023/01/01.h5") as data:
    global_data = data["fields"][1,1]
print(global_data.shape)

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

print(us_temperature_interpolated.shape)