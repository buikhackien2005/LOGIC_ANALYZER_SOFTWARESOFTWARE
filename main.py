from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from ui.plot_manager import PlotManager
from utils.mock_generator import MockDataGenerator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logic Analyzer - Pro Edition")
        self.resize(1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        
        # === KHU VỰC BÊN TRÁI: ĐỒ THỊ & LOG ===
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        
        # Nhúng PlotManager vào
        self.plot_manager = PlotManager()
        self.left_layout.addWidget(self.plot_manager, stretch=7)
        
        # Tạm thời để một nút Test ở đây (Sau này sẽ xóa khi có Control Panel)
        self.btn_test_mock = QPushButton("TEST: Load Mock Data")
        self.btn_test_mock.setStyleSheet("padding: 10px; background-color: #007ACC; color: white; font-weight: bold;")
        self.btn_test_mock.clicked.connect(self.run_test_flow)
        self.left_layout.addWidget(self.btn_test_mock)
        
        # Giữ chỗ cho Transaction Log
        self.placeholder_log = QLabel("[Transaction Log Table sẽ nằm ở đây]")
        self.placeholder_log.setStyleSheet("background-color: #222; color: gray; alignment: center;")
        self.left_layout.addWidget(self.placeholder_log, stretch=3)
        
        # === KHU VỰC BÊN PHẢI: CONTROL PANEL ===
        self.placeholder_right = QLabel("[Control Panel sẽ nằm ở đây]")
        self.placeholder_right.setStyleSheet("background-color: #333; color: white; alignment: center;")
        
        # Ép tỷ lệ 7:3 cho Trái/Phải
        self.main_layout.addWidget(self.left_panel, stretch=7)
        self.main_layout.addWidget(self.placeholder_right, stretch=3)

    def run_test_flow(self):
        """Hàm mô phỏng luồng chạy khi có dữ liệu mới."""
        # 1. Lấy dữ liệu từ utils
        t, buf = MockDataGenerator.get_8ch_mock_data()
        
        # 2. Đẩy dữ liệu vào ui/plot_manager để vẽ
        self.plot_manager.update_data(t, buf)