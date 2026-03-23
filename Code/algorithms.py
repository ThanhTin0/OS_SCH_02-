from read_input import read_scheduling_data
import pandas as pd

def calculate_fcfs(processes):
    """
    Hàm tính toán thuật toán lập lịch FCFS.
    processes: List of dictionaries chứa thông tin tiến trình.
    """
    # 1. Sắp xếp các tiến trình theo thời gian đến (Arrival Time)
    # Nếu có 2 tiến trình đến cùng lúc, thuật toán sẽ tự giữ nguyên thứ tự gốc
    processes.sort(key=lambda x: x['Arrival_Time'])

    current_time = 0
    results = []

    for p in processes:
        # Nếu CPU đang rảnh mà tiến trình chưa tới, phải đẩy thời gian lên lúc tiến trình tới
        if current_time < p['Arrival_Time']:
            current_time = p['Arrival_Time']

        # Tính toán các mốc thời gian
        start_time = current_time
        completion_time = start_time + p['Burst_Time']
        turnaround_time = completion_time - p['Arrival_Time']
        waiting_time = turnaround_time - p['Burst_Time']

        # Lưu kết quả của tiến trình này
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

        # Cập nhật thời gian hiện tại cho tiến trình tiếp theo
        current_time = completion_time

    return results

if __name__ == "__main__":
    # Đọc dữ liệu từ file csv (gọi lại hàm bạn đã làm thành công)
    input_file = 'data_input.csv'
    processes_list = read_scheduling_data(input_file)
    
    if processes_list:
        print("\n[BẮT ĐẦU CHẠY THUẬT TOÁN FCFS]")
        fcfs_result = calculate_fcfs(processes_list)
        
        # Dùng lại pandas để in bảng kết quả cho đẹp
        df_result = pd.DataFrame(fcfs_result)
        print("\nKết quả tính toán FCFS:")
        print("-" * 70)
        print(df_result.to_string(index=False))
        print("-" * 70)
        
        # Tính thời gian chờ và lưu lại trung bình
        avg_tat = df_result['Turnaround_Time'].mean()
        avg_wt = df_result['Waiting_Time'].mean()
        print(f"Thời gian lưu lại trung bình (Average TAT): {avg_tat:.2f}")
        print(f"Thời gian chờ trung bình (Average WT): {avg_wt:.2f}")