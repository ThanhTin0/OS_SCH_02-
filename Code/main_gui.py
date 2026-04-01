import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import time  # Thêm thư viện đo thời gian của Bạn số 2
import read_input  
import algorithms  
import gantt_chart  

# Biến toàn cục
processes_data = []
latest_results = [] 
current_algo = ""   

def browse_file():
    global processes_data
    filename = filedialog.askopenfilename(title="Chọn file CSV", filetypes=(("CSV", "*.csv"), ("All", "*.*")))
    if filename:
        lbl_file.config(text=f"Đã chọn: {os.path.basename(filename)}", fg="green")
        processes_data = read_input.read_scheduling_data(filename)
        if not processes_data:
            messagebox.showerror("Lỗi", "Không đọc được dữ liệu. Kiểm tra lại file CSV!")

def show_results_in_table(results):
    for row in tree.get_children():
        tree.delete(row)
    for p in results:
        tree.insert("", tk.END, values=(p['ProcessID'], p['Arrival_Time'], p['Burst_Time'], p['Priority'], 
                                        p['Start_Time'], p['Completion_Time'], p['Turnaround_Time'], p['Waiting_Time']))

def run_fcfs():
    global latest_results, current_algo
    if not processes_data:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn file input CSV trước!")
        return
    
    # 1. BẮT ĐẦU BẤM GIỜ
    start_time = time.time()
    
    # Gọi hàm thuật toán của Tín
    latest_results = algorithms.calculate_fcfs(processes_data)
    
    # 2. DỪNG ĐỒNG HỒ VÀ TÍNH TOÁN
    end_time = time.time()
    exec_time = (end_time - start_time) * 1000 # Đổi ra mili-giây
    
    current_algo = "FCFS"
    show_results_in_table(latest_results)
    algorithms.export_to_csv(latest_results, "fcfs_output.csv")
    
    # 3. HIỂN THỊ KẾT QUẢ THỜI GIAN LÊN MÀN HÌNH
    messagebox.showinfo("Thành công", f"Đã chạy xong FCFS!\nThời gian xử lý: {exec_time:.2f} ms")

def run_priority():
    global latest_results, current_algo
    if not processes_data:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn file input CSV trước!")
        return
    
    # 1. BẮT ĐẦU BẤM GIỜ
    start_time = time.time()
    
    # Gọi hàm thuật toán của Tín
    latest_results = algorithms.calculate_priority_non_preemptive(processes_data)
    
    # 2. DỪNG ĐỒNG HỒ VÀ TÍNH TOÁN
    end_time = time.time()
    exec_time = (end_time - start_time) * 1000 # Đổi ra mili-giây
    
    current_algo = "Priority (Độc quyền)"
    show_results_in_table(latest_results)
    algorithms.export_to_csv(latest_results, "priority_output.csv")
    
    # 3. HIỂN THỊ KẾT QUẢ THỜI GIAN LÊN MÀN HÌNH
    messagebox.showinfo("Thành công", f"Đã chạy xong Priority!\nThời gian xử lý: {exec_time:.2f} ms")

def show_gantt():
    if not latest_results:
        messagebox.showwarning("Cảnh báo", "Ông phải bấm Chạy FCFS hoặc Priority trước để có số liệu rồi mới vẽ sơ đồ được!")
        return
    gantt_chart.draw_gantt(latest_results, current_algo)

# --- VẼ CỬA SỔ ---
window = tk.Tk()
window.title("Mô phỏng Lập lịch CPU - Nhóm 6 người")
window.geometry("850x500")

tk.Button(window, text="📂 Chọn file Input CSV", command=browse_file, bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
lbl_file = tk.Label(window, text="Chưa chọn file", font=("Arial", 10, "italic"))
lbl_file.pack()

frame_btn = tk.Frame(window)
frame_btn.pack(pady=10)
tk.Button(frame_btn, text="▶ Chạy FCFS", command=run_fcfs, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=0, padx=10)
tk.Button(frame_btn, text="▶ Chạy Priority", command=run_priority, bg="#e67e22", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=1, padx=10)
tk.Button(frame_btn, text="📊 Xem Sơ đồ Gantt", command=show_gantt, bg="#9b59b6", fg="white", font=("Arial", 10, "bold"), width=18).grid(row=0, column=2, padx=10)

columns = ('ID', 'Arrival', 'Burst', 'Priority', 'Start', 'Completion', 'Turnaround', 'Waiting')
tree = ttk.Treeview(window, columns=columns, show='headings', height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=90, anchor=tk.CENTER)
tree.pack(pady=10, fill="x", padx=20)

window.mainloop()