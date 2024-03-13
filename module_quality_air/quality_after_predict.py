import pandas as pd
import numpy as np

def avg_factor_quality(input_file):
    data = pd.read_csv(input_file)
    data['DATETIMEDATA'] = pd.to_datetime(data['DATETIMEDATA'])
    data.set_index('DATETIMEDATA', inplace=True)
    para_avg = data.resample('D').mean()
    para_avg = para_avg[['O3', 'WS', 'TEMP', 'RH', 'WD', 'PM25']]
    
    # เพิ่มเงื่อนไขเพื่อแสดงข้อความตามช่วงของค่า PM25
    conditions = [
        (para_avg['PM25'] <= 25),
        (para_avg['PM25'] <= 37),
        (para_avg['PM25'] <= 50),
        (para_avg['PM25'] <= 90),
        (para_avg['PM25'] > 90)
    ]
    choices = ['very good', 'good', 'medium', 'bad', 'very bad']
    para_avg['PM25_label'] = np.select(conditions, choices, default='Unknown')
    
    output_file = f"quality_of_{input_file}"
    para_avg.to_csv(output_file, index=True, float_format='%.2f')





