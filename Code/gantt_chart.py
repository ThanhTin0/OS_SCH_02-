import matplotlib.pyplot as plt

def draw_gantt(results, algo_name="CPU Scheduling"):
    if not results:
        return

    # Khởi tạo khung biểu đồ
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_ylim(0, 1)
    ax.set_xlim(0, results[-1]['Completion_Time'] + 5)
    ax.set_yticks([]) # Ẩn trục Y
    ax.set_xlabel('Thời gian (ms)', fontweight='bold')
    ax.set_title(f'Sơ đồ Gantt - Thuật toán {algo_name}', fontweight='bold', fontsize=14)

    # Lấy danh sách màu sắc đẹp mắt
    colors = plt.cm.get_cmap('tab10', len(results))

    # Vẽ từng thanh tiến trình
    for i, p in enumerate(results):
        pid = p['ProcessID']
        start = p['Start_Time']
        burst = p['Burst_Time']
        
        # Vẽ khối chữ nhật (Thanh màu)
        ax.broken_barh([(start, burst)], (0.2, 0.6), facecolors=colors(i), edgecolor='black', linewidth=1.5)
        
        # In tên ID (P1, P2...) vào giữa thanh màu
        ax.text(start + burst / 2, 0.5, pid, ha='center', va='center', color='white', fontweight='bold', fontsize=11)
        
        # In mốc thời gian bắt đầu ở dưới
        ax.text(start, 0.1, str(start), ha='center', va='top', fontsize=10)
        
        # Nếu là tiến trình cuối cùng, in luôn mốc kết thúc
        if i == len(results) - 1: 
            ax.text(start + burst, 0.1, str(start + burst), ha='center', va='top', fontsize=10)

    # Hiển thị dạng lưới cho dễ nhìn
    plt.grid(True, axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()