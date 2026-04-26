from abc import ABC, abstractmethod

class ProtocolDecoder(ABC):
    """Lớp cha trừu tượng cho mọi thuật toán giải mã."""
    
    @abstractmethod
    def decode(self, sample_rate, buffer_array):
        """
        Hàm giải mã bắt buộc phải được ghi đè (override) ở class con.
        
        Args:
            sample_rate (int): Tốc độ lấy mẫu (VD: 500000)
            buffer_array (np.array): Mảng byte chứa toàn bộ dữ liệu 8 kênh.
            
        Returns:
            list: Danh sách các giao dịch đã được chuẩn hóa hóa dạng chuỗi.
                  Mẫu: [{'time': '0.00200s', 'protocol': 'UART', 'channel': 'CH1', 'data': "0x41 ('A')"}]
        """
        pass