import pandas as pd
import os

def read_scheduling_data(file_name):
    """
    Đọc dữ liệu lập lịch từ file CSV sử dụng thư viện pandas.
    """
    try:
        # Đường dẫn tuyệt đối đến file nằm trong thư mục Extra (giả sử file code chạy ở thư mục gốc project)
        # Nếu code chạy từ thư mục 'Code', ta cần lùi 1 cấp
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, '..', 'Extra', file_name)
        
        # Đọc CSV bằng pandas
        df = pd.read_csv(file_path)
        
        print("Đọc dữ liệu thành công!")
        print("-" * 30)
        print(df) # In ra bảng dữ liệu để kiểm tra
        print("-" * 30)
        
        # Chuyển đổi pandas DataFrame thành List of Dictionaries để dễ xử lý logic thuật toán sau này
        processes = df.to_dict('records')
        return processes

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file tại đường dẫn: {file_path}")
        return None
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
        return None

if __name__ == "__main__":
    # Test thử hàm đọc file
    input_file = 'data_input.csv'
    processes_list = read_scheduling_data(input_file)
    
    if processes_list:
        print("\nDữ liệu sau khi chuyển đổi sang List:")
        for proc in processes_list:
            print(proc)