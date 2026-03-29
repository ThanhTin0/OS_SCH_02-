import pandas as pd
import os
from read_input import read_scheduling_data

def calculate_fcfs(processes):
    """Tính toán thuật toán lập lịch FCFS."""
    procs = [p.copy() for p in processes] # Tạo bản sao để không ảnh hưởng dữ liệu gốc
    procs.sort(key=lambda x: x['Arrival_Time'])
    current_time = 0
    results = []

    for p in procs:
        if current_time < p['Arrival_Time']:
            current_time = p['Arrival_Time']

        start_time = current_time
        completion_time = start_time + p['Burst_Time']
        turnaround_time = completion_time - p['Arrival_Time']
        waiting_time = turnaround_time - p['Burst_Time']

        results.append({
            'ProcessID': p['ProcessID'],
            'Arrival_Time': p['Arrival_Time'],
            'Burst_Time': p['Burst_Time'],
            'Priority': p['Priority'],
            'Start_Time': start_time,
            'Completion_Time': completion_time,
            'Turnaround_Time': turnaround_time,
            'Waiting_Time': waiting_time
        })
        current_time = completion_time

    return results

def calculate_priority_non_preemptive(processes):
    """Tính toán thuật toán lập lịch Priority (Độc quyền)."""
    procs = [p.copy() for p in processes]
    # Sắp xếp theo Arrival Time ban đầu
    procs.sort(key=lambda x: x['Arrival_Time'])

    current_time = 0
    completed_count = 0
    n = len(procs)
    results = []
    is_completed = [False] * n

    while completed_count < n:
        # Tìm tất cả các tiến trình đã đến nhưng chưa hoàn thành
        available_procs = []
        for i in range(n):
            if not is_completed[i] and procs[i]['Arrival_Time'] <= current_time:
                available_procs.append((i, procs[i]))

        if not available_procs:
            # Nếu CPU rảnh mà chưa có ai tới, tua thời gian đến lúc người tiếp theo tới
            next_arrival = min([procs[i]['Arrival_Time'] for i in range(n) if not is_completed[i]])
            current_time = next_arrival
            continue

        # Chọn tiến trình có Priority cao nhất (Số Priority nhỏ nhất)
        # Nếu Priority bằng nhau, ưu tiên người đến trước (đã được sort theo Arrival_Time từ đầu)
        available_procs.sort(key=lambda x: x[1]['Priority'])
        selected_index = available_procs[0][0]
        p = procs[selected_index]

        # Tính toán mốc thời gian
        start_time = current_time
        completion_time = start_time + p['Burst_Time']
        turnaround_time = completion_time - p['Arrival_Time']
        waiting_time = turnaround_time - p['Burst_Time']

        results.append({
            'ProcessID': p['ProcessID'],
            'Arrival_Time': p['Arrival_Time'],
            'Burst_Time': p['Burst_Time'],
            'Priority': p['Priority'],
            'Start_Time': start_time,
            'Completion_Time': completion_time,
            'Turnaround_Time': turnaround_time,
            'Waiting_Time': waiting_time
        })

        # Cập nhật trạng thái
        is_completed[selected_index] = True
        completed_count += 1
        current_time = completion_time

    return results

def export_to_csv(results, filename):
    """Xuất kết quả ra file CSV lưu vào thư mục Output."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_path, '..', 'Output')
    os.makedirs(output_dir, exist_ok=True) 
    
    file_path = os.path.join(output_dir, filename)
    df = pd.DataFrame(results)
    df.to_csv(file_path, index=False)
    print(f"[THÀNH CÔNG] Đã xuất kết quả ra file: {filename}")

if __name__ == "__main__":
    input_file = 'data_input.csv'
    processes_list = read_scheduling_data(input_file)
    
    if processes_list:
        # Chạy và xuất FCFS
        print("\n" + "="*50)
        print("[1] KẾT QUẢ THUẬT TOÁN FCFS")
        fcfs_result = calculate_fcfs(processes_list)
        print(pd.DataFrame(fcfs_result).to_string(index=False))
        export_to_csv(fcfs_result, "fcfs_output.csv")
        
        # Chạy và xuất Priority
        print("\n" + "="*50)
        print("[2] KẾT QUẢ THUẬT TOÁN PRIORITY (NON-PREEMPTIVE)")
        priority_result = calculate_priority_non_preemptive(processes_list)
        print(pd.DataFrame(priority_result).to_string(index=False))
        export_to_csv(priority_result, "priority_output.csv")
        print("="*50 + "\n")