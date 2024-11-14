# 初始化最大值和最小值为None或适当的初始值
max_lon = float('-inf')
min_lon = float('inf')

# 打开文件
with open('/mnt/nfs/samba/数据聚变/气象数据/china_data/87_stations_3years_summer/2021060112.txt', 'r') as file:
    next(file)  # 跳过标题行
    for line in file:
        # 分割行数据
        parts = line.split()
        # 将lon列的数据转换为浮点数
        lon_value = float(parts[2])  # 假设lon是第三列
        
        # 更新最大值和最小值
        if lon_value > max_lon:
            max_lon = lon_value
        if lon_value < min_lon:
            min_lon = lon_value

# 打印结果
print(f"Maximum Longitude: {max_lon}")
print(f"Minimum Longitude: {min_lon}")