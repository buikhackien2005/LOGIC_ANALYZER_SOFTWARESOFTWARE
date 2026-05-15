import numpy as np
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QPushButton)

class StatsDialog(QDialog):
    def __init__(self, transactions, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Statistical Report")
        self.resize(700, 300)
        
        layout = QVBoxLayout(self)
        
        # Bảng hiển thị kết quả
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Protocol/Channel", "Total Packets", "Min Delay (ms)", "Max Delay (ms)", "Avg Delay (ms)"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("background-color: #FAFAFA; color: #000; font-weight: bold;")
        
        layout.addWidget(self.table)
        
        btn_close = QPushButton("Close Report")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)
        
        self.calculate_statistics(transactions)

    def calculate_statistics(self, transactions):
        if not transactions:
            return
            
        # 1. Gom nhóm gói tin theo Giao thức + Kênh
        grouped_data = {}
        for t in transactions:
            key = f"{t['protocol']} ({t['channel']})"
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append(t['time_val'])
            
        # 2. Xóa bảng và tính toán
        self.table.setRowCount(0)
        
        for key, times in grouped_data.items():
            count = len(times)
            
            # Tính khoảng cách thời gian giữa các gói tin liên tiếp (Deltas)
            if count > 1:
                # np.diff sẽ trừ các phần tử liền kề: t[1]-t[0], t[2]-t[1]...
                deltas = np.diff(times) * 1000 # Nhân 1000 để đổi ra mili-giây (ms)
                min_d = f"{np.min(deltas):.3f}"
                max_d = f"{np.max(deltas):.3f}"
                avg_d = f"{np.mean(deltas):.3f}"
            else:
                min_d = max_d = avg_d = "N/A" # Không đủ 2 gói tin để tính khoảng cách
                
            # Đẩy kết quả vào bảng
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(key))
            self.table.setItem(row, 1, QTableWidgetItem(str(count)))
            self.table.setItem(row, 2, QTableWidgetItem(min_d))
            self.table.setItem(row, 3, QTableWidgetItem(max_d))
            self.table.setItem(row, 4, QTableWidgetItem(avg_d))