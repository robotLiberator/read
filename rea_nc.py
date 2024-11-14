import netCDF4 as nc
import numpy as np

# 替换为你的 .nc 文件路径
nc_file_path = '2020010100.nc'
nc_file_path2 = '_surface_data.nc'

ds = nc.Dataset(nc_file_path, 'r')  # 'r' 表示以只读模式打开
ds2 = nc.Dataset(nc_file_path2, 'r')  # 'r' 表示以只读模式打开

t2m_data2 = ds2.variables['t2m'][:]
t2m_data = ds.variables['t2m'][:]
# print("文件打开成功！")

# # 列出所有变量
# print("文件中的变量有：")
# print(ds.variables.keys())


# lon_data = ds.variables['longitude'][:]
# print("\n'lon' 变量的数据：")
# print(lon_data)
# lon_data = ds.variables['latitude'][:]
# print("\n'lat' 变量的数据：")
# print(lon_data)

# # 假设我们想读取名为 't2m' 的变量
# if 't2m' in ds.variables:
#     t2m_data = ds.variables['t2m'][:]
#     print("\n't2m' 变量的数据：")
#     print(t2m_data)

#     # 打印 't2m' 变量的属性
#     print("\n't2m' 变量的属性：")
#     for attr_name, attr_value in ds.variables['t2m'].ncattrs().items():
#         print(f"{attr_name}: {attr_value}")


#     ds.close()
#     print("\n文件已关闭。")

# 你可以在此处继续其他数据处理或分析操作