import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import time  
import read_input  
import algorithms  
import gantt_chart  

# --- Biến toàn cục ---
processes_data = []
latest_results = [] 
current_algo = ""   

def browse_file():
    """
    Mở hộp thoại chọn file CSV và nạp dữ liệu vào hệ thống.
    Đóng góp: Nguyễn Tiến Trung
    """
    global processes_data
    filename = filedialog.askopenfilename(title="Chọn file CSV", filetypes=(("CSV", "*.csv"), ("All", "*.*")))
    if filename:
        lbl_file.config(text=f"Đã chọn: {os.path.basename(filename)}", fg="green")
        processes_data = read_input.read_scheduling_data(filename)
        if not processes_data:
            messagebox.showerror("Lỗi", "Không đọc được dữ liệu. Kiểm tra lại cấu trúc file CSV!")

def show_results_in_table(results):
    """
    Hiển thị kết quả lên bảng Treeview và tính toán các giá trị trung bình.
    Đóng góp: Nguyễn Tiến Trung
    """
    for row in tree.get_children():
        tree.delete(row)
    
    for p in results:
        tree.insert("", tk.END, values=(p['ProcessID'], p['Arrival_Time'], p['Burst_Time'], p['Priority'], 
                                        p['Start_Time'], p['Completion_Time'], p['Turnaround_Time'], p['Waiting_Time']))
    
    # --- TÍNH TOÁN CHỈ SỐ TRUNG BÌNH (Cải tiến mới) ---
    if results:
        avg_wait = sum(p['Waiting_Time'] for p in results) / len(results)
        avg_turn = sum(p['Turnaround_Time'] for p in results) / len(results)
        # Cập nhật thông tin lên tiêu đề cửa sổ để báo cáo trực quan
        window.title(f"CPU Scheduling - Avg Wait: {avg_wait:.2f}ms | Avg Turnaround: {avg_turn:.2f}ms")

def run_fcfs():
    """Thực thi FCFS và đo hiệu suất xử lý."""
    global latest_results, current_algo
    if not processes_data:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn file input CSV trước!")
        return
    
    start_time = time.time()
    latest_results = algorithms.calculate_fcfs(processes_data)
    end_time = time.time()
    exec_time = (end_time - start_time) * 1000 
    
    current_algo = "FCFS"
    show_results_in_table(latest_results)
    algorithms.export_to_csv(latest_results, "fcfs_output.csv")
    
    messagebox.showinfo("Thành công", f"Đã thực thi xong thuật toán FCFS!\nThời gian xử lý hệ thống: {exec_time:.2f} ms")

def run_priority():
    """Thực thi Priority Non-preemptive và đo hiệu suất xử lý."""
    global latest_results, current_algo
    if not processes_data:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn file input CSV trước!")
        return
    
    start_time = time.time()
    latest_results = algorithms.calculate_priority_non_preemptive(processes_data)
    end_time = time.time()
    exec_time = (end_time - start_time) * 1000 
    
    current_algo = "Priority (Độc quyền)"
    show_results_in_table(latest_results)
    algorithms.export_to_csv(latest_results, "priority_output.csv")
    
    messagebox.showinfo("Thành công", f"Đã thực thi xong thuật toán Priority!\nThời gian xử lý hệ thống: {exec_time:.2f} ms")

def show_gantt():
    """Kiểm tra điều kiện và gọi module vẽ sơ đồ Gantt trực quan."""
    if not latest_results:
        messagebox.showwarning("Thông báo", "Vui lòng thực thi thuật toán để có dữ liệu trước khi vẽ sơ đồ Gantt.")
        return
    gantt_chart.draw_gantt(latest_results, current_algo)

# --- THIẾT KẾ GIAO DIỆN (GUI) ---
window = tk.Tk()
window.title("Mô phỏng Lập lịch CPU - Nhóm 6")
window.geometry("850x520") # Tăng nhẹ chiều cao để bảng cân đối hơn

# Header
tk.Button(window, text="📂 Chọn file Input CSV", command=browse_file, bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
lbl_file = tk.Label(window, text="Chưa chọn file dữ liệu", font=("Arial", 10, "italic"))
lbl_file.pack()

# Control Buttons
frame_btn = tk.Frame(window)
frame_btn.pack(pady=10)
tk.Button(frame_btn, text="▶ Chạy FCFS", command=run_fcfs, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=0, padx=10)
tk.Button(frame_btn, text="▶ Chạy Priority", command=run_priority, bg="#e67e22", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=1, padx=10)
tk.Button(frame_btn, text="📊 Xem Sơ đồ Gantt", command=show_gantt, bg="#9b59b6", fg="white", font=("Arial", 10, "bold"), width=18).grid(row=0, column=2, padx=10)

# Results Table
columns = ('ID', 'Arrival', 'Burst', 'Priority', 'Start', 'Completion', 'Turnaround', 'Waiting')
tree = ttk.Treeview(window, columns=columns, show='headings', height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=95, anchor=tk.CENTER)
tree.pack(pady=10, fill="x", padx=20)

# Footer info
lbl_footer = tk.Label(window, text="Phần mềm phát triển bởi Nhóm 6 - Học phần Hệ điều hành", font=("Arial", 8))
lbl_footer.pack(side="bottom", pady=5)

window.mainloop()