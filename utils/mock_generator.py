import numpy as np

class MockDataGenerator:
    """Class cung cấp dữ liệu giả để kiểm thử hệ thống khi chưa có ESP32."""
    
    @staticmethod
    def get_8ch_mock_data():
        sample_rate = 500000  # 500 kHz
        num_samples = 50000   # 100 ms
        
        time_array = np.arange(num_samples) / sample_rate 
        
        # Mảng 8-bit, khởi tạo mức CAO (0xFF / 255)
        buffer = np.full(num_samples, 255, dtype=np.uint8)
        
        # CH0: Xung Clock (Đảo mức mỗi 20 mẫu)
        for i in range(0, num_samples, 40):
            buffer[i:i+20] &= ~(1 << 0) & 0xFF 
            
        # CH1: UART 'A' (0x41) ở 9600 bps
        spb = int(sample_rate / 9600)
        start_idx = 1000 
        bits = [0, 1, 0, 0, 0, 0, 0, 1, 0, 1] 
        for i, bit in enumerate(bits):
            idx_from = start_idx + (i * spb)
            idx_to = start_idx + ((i + 1) * spb)
            if bit == 0:
                buffer[idx_from:idx_to] &= ~(1 << 1) & 0xFF
            else:
                buffer[idx_from:idx_to] |= (1 << 1) & 0xFF
                
        # CH2: I2C SDA giả (Mô phỏng Start condition)
        buffer[2000:3000] &= ~(1 << 2) & 0xFF
                
        return time_array, buffer