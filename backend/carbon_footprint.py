import pandas as pd

MEMORY_POWER=0.3725 # W/GB
PUE = 1.67
PSF = 1.0
CARBON_INTENSITY = 500.0 # 500g? 0.5kg?

SEC_PER_HOUR = 3600.0
KILO = 1000.0

# power_draw_for_cores, usage만 구하면 됨
def get_carbon_footprint(java_execution_result, system_info):
    # 계수들 맞는지 확인하기
    tdp_data = pd.read_csv('./data/TDP_cpu.csv')

    # 제 cpu가 목록에 없어서 임의로 넣어놨습니다
    # processor_name = system_info['Processor name']
    processor_name = 'Core i5-4460'
    tdp_row = tdp_data.query('index == @processor_name')
    TDP_per_core=tdp_row['Unnamed: 3'].values[0]
    TDP_in_watt = float(tdp_row['in Watt'].values[0])
    #print(tdp_row)
    #print(tdp_row['in Watt'].values[0])
    runtime = java_execution_result['runtime'] / SEC_PER_HOUR
    usage = 1.0 # 뭔지 모르겠음

    # powerNeeded_CPU = PUE_used * n_CPUcores * CPUpower * usageCPU_used
    # PUE_used = 1.67
    # n_CPUcores = ???
    # CPUpower = ???
    # usageCPU_used = ???
    power_draw_for_cores=TDP_in_watt / KILO
    power_draw_for_memory=system_info['Available memory'] * MEMORY_POWER / KILO
    energy_needed = runtime * (power_draw_for_cores * usage+  power_draw_for_memory) * PUE * PSF
    carbon_footprint = energy_needed * CARBON_INTENSITY

    print(carbon_footprint)
    return carbon_footprint