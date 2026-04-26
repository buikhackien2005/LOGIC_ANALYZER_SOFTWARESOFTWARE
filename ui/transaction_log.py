from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

class TransactionLog(QTableWidget):
    """Bảng hiển thị danh sách các dữ liệu đã giải mã theo thứ tự thời gian."""
    def __init__(self):
        super().__init__()
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Time", "Channel", "Protocol", "Data"])
        
        # Cấu hình giao diện: Tự dãn đều các cột
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QTableWidget.NoEditTriggers) # Không cho sửa
        self.setSelectionBehavior(QTableWidget.SelectRows) # Chọn cả dòng
        self.setStyleSheet("background-color: #1E1E1E; color: #BBB; gridline-color: #333;")

    def update_logs(self, transactions):
        """Xóa bảng cũ và đổ dữ liệu mới vào."""
        self.setRowCount(0)
        for entry in transactions:
            row = self.rowCount()
            self.insertRow(row)
            self.setItem(row, 0, QTableWidgetItem(entry['time']))
            self.setItem(row, 1, QTableWidgetItem(entry['channel']))
            self.setItem(row, 2, QTableWidgetItem(entry['protocol']))
            self.setItem(row, 3, QTableWidgetItem(entry['data']))