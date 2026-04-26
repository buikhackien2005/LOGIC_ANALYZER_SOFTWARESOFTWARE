import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class PlotManager(QWidget):
    """Quản lý khu vực vẽ đồ thị Waveform cho 8 kênh."""
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0) # Xóa viền thừa
        
        # Cấu hình UI của Plot
        pg.setConfigOption('background', '#121212')
        pg.setConfigOption('foreground', '#E0E0E0')
        self.plot_widget = pg.PlotWidget(title="Waveform Viewer (8 Channels)")
        layout.addWidget(self.plot_widget)
        
        # Khởi tạo trục Y cho 8 kênh
        self.plot_widget.setYRange(-1, 16)
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        
        # Cài đặt nhãn cho các kênh
        ay = self.plot_widget.getAxis('left')
        ticks = [[(i * 2 + 0.5, f"CH{i}") for i in range(8)]]
        ay.setTicks(ticks)
        
        # Bảng màu cố định cho 8 kênh
        self.colors = ['#FF5252', '#448AFF', '#69F0AE', '#FFD740', 
                       '#E040FB', '#18FFFF', '#FFAB40', '#B0BEC5']

    def update_data(self, time_array, buffer_array):
        """Hàm này nhận data nhị phân và tự động unpack để vẽ lên đồ thị."""
        self.plot_widget.clear()
        
        for ch in range(8):
            # Giải mã bitwise và offset trục Y
            ch_data = (buffer_array >> ch) & 1 
            y_render = ch_data + (ch * 2)
            
            # Vẽ đường sóng
            pen = pg.mkPen(self.colors[ch], width=1.5)
            self.plot_widget.plot(time_array, y_render, pen=pen)