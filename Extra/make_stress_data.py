import pandas as pd
import random

def generate_stress_test_data(filename="stress_test_10k.csv", num_processes=10000):
    print(f"Đang tạo {num_processes} tiến trình CPU ảo...")
    data = []
    current_arrival = 0
    
    for i in range(num_processes):
        data.append({
            'ProcessID': f'P{i+1}',
            'Arrival_Time': current_arrival,
            # Tốc độ xử lý CPU từ 1 đến 50 đơn vị
            'Burst_Time': random.randint(1, 50),
            # Độ ưu tiên từ 1 (cao nhất) đến 10 (thấp nhất)
            'Priority': random.randint(1, 10)
        })
        # Giả lập thời gian đến rải rác
        current_arrival += random.randint(0, 3) 
        
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"[THÀNH CÔNG] Đã lưu file dữ liệu test siêu to khổng lồ vào: {filename}")

if __name__ == "__main__":
    generate_stress_test_data()