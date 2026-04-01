import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import read_input  # File đọc dữ liệu của nhóm
import algorithms  # File chứa thuật toán của Tín

# Biến toàn cục lưu dữ liệu đọc được từ file CSV
processes_data = []

def browse_file():
    global processes_data
    filename = filedialog.askopenfilename(title="Chọn file CSV", filetypes=(("CSV", "*.csv"), ("All", "*.*")))
    if filename:
        lbl_file.config(text=f"Đã chọn: {os.path.basename(filename)}", fg="green")
        # Gọi hàm đọc file
        processes_data = read_input.read_scheduling_data(filename)
        if not processes_data:
            messagebox.showerror("Lỗi", "Không đọc được dữ liệu. Kiểm tra lại file CSV!")

def show_results_in_table(results):
    """Xóa dữ liệu cũ và in kết quả mới vào bảng"""
    for row in tree.get_children():
        tree.delete(row)
    for p in results:
        tree.insert("", tk.END, values=(p['ProcessID'], p['Arrival_Time'], p['Burst_Time'], p['Priority'], 
                                        p['Start_Time'], p['Completion_Time'], p['Turnaround_Time'], p['Waiting_Time']))

def run_fcfs():
    if not processes_data:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn file input CSV trước!")
        return
    # Gọi hàm thuật toán của Tín
    results = algorithms.calculate_fcfs(processes_data)
    show_results_in_table(results)
    algorithms.export_to_csv(results, "fcfs_output.csv")
    messagebox.showinfo("Thành công", "Đã chạy xong FCFS và xuất file output!")

def run_priority():
    if not processes_data:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn file input CSV trước!")
        return
    # Gọi hàm thuật toán của Tín
    results = algorithms.calculate_priority_non_preemptive(processes_data)
    show_results_in_table(results)
    algorithms.export_to_csv(results, "priority_output.csv")
    messagebox.showinfo("Thành công", "Đã chạy xong Priority và xuất file output!")

# --- VẼ CỬA SỔ ---
window = tk.Tk()
window.title("Mô phỏng Lập lịch CPU - Nhóm 6 người")
window.geometry("850x500")

# Nút chọn file
tk.Button(window, text="📂 Chọn file Input CSV", command=browse_file, bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
lbl_file = tk.Label(window, text="Chưa chọn file", font=("Arial", 10, "italic"))
lbl_file.pack()

# Khung chứa nút thuật toán
frame_btn = tk.Frame(window)
frame_btn.pack(pady=10)
tk.Button(frame_btn, text="▶ Chạy FCFS", command=run_fcfs, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=0, padx=10)
tk.Button(frame_btn, text="▶ Chạy Priority", command=run_priority, bg="#e67e22", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=1, padx=10)

# Bảng hiển thị kết quả (Treeview)
columns = ('ID', 'Arrival', 'Burst', 'Priority', 'Start', 'Completion', 'Turnaround', 'Waiting')
tree = ttk.Treeview(window, columns=columns, show='headings', height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=90, anchor=tk.CENTER)
tree.pack(pady=10, fill="x", padx=20)

window.mainloop()