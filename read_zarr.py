import xarray as xr
import datetime
from datetime import datetime, timedelta
from tqdm import tqdm
import os
dataset  = xr.open_zarr('/mnt/nfs/samba/数据聚变/气象数据/pangu/2018-2022_0012_0p25.zarr')

# 定义保存文件的根目录
root_dir = './pangu'


# 定义要下载的时间范围（2022 年 12 月）
start_date = datetime(2022, 1, 1 , 00)
end_date = datetime(2022, 12, 31, 23)  # 结束日期为 2023 年 1 月 1 日的零点
# 筛选出时间范围内的数据
surface_variables_list = ['mean_sea_level_pressure', '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_temperature']
upper_air_variables_list = ['geopotential', 'temperature', 'specific_humidity', 'u_component_of_wind', 'v_component_of_wind']
variables_list = surface_variables_list + upper_air_variables_list


selected_data = dataset[variables_list].sel(time=slice(start_date, end_date))


    