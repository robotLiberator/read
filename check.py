import os
from datetime import datetime, timedelta

    
def check_month_complete(root_path, current_date, end_date):
    missing_files = []
    # days_in_month = (datetime(current_date.year, current_date.month % 12 + 1, 1) - timedelta(days=1)).day
 
    # for day in range(1, days_in_month + 1):
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        day = current_date.day

        day_folder_path = os.path.join(root_path, f"{year}/{month:02d}/{day:02d}")

        if not os.path.isdir(day_folder_path):
            print('no ',day)
            continue

        files_in_day = os.listdir(day_folder_path)
        if len(files_in_day) != 24:

            missing_hours = [f"{year}-{month}-{day}-{str(hour).zfill(2)}" 
                             for hour in range(0,24) 
                            #  if f"hrrr.t00z.wrfprsf{hour:02d}.grib2" 
                            # hrrr_20150116_hrrr_t00z_wrfprsf00.grib2
                             if f"hrrr_{year}{month:02d}{day:02d}_hrrr_t{hour:02d}z_wrfprsf00.grib2"
                            #  if f"hrrr_{year}{month:02d}{day:02d}_hrrr_t00z_wrfprsf{hour:02d}.grib2"
                             not in files_in_day]
            
            missing_files.extend(missing_hours)
            
            
        current_date += timedelta(days=1)

    if missing_files:
        return False, missing_files
    else:
        return True, None


root_path = "/mnt/nfs/samba/数据聚变/气象数据/hrrr_nwp_grib"  
# root_path = "/mnt/nfs/samba/数据聚变/气象数据/hrrr_grib"  

current_date = datetime(2024, 1, 1)
end_date = datetime(2024, 9, 30)

complete, missing_files = check_month_complete(root_path, current_date, end_date)
if complete:
    print(f"文件夹 '{root_path}' 中的月份是完整的。")
else:
    print(f"文件夹 '{root_path}' 中的月份不完整，缺失的文件为:")
        # 打开文件用于写入
    with open('miss_list.txt', 'w') as file:

            # 文件会在with语句块结束时自动关闭
        for missing_file in missing_files:
            print(missing_file)
            file.write(missing_file+"\n")
        


