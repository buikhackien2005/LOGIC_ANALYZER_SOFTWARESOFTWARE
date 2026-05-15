import numpy as np
from .base_decoder import ProtocolDecoder

class UARTDecoder(ProtocolDecoder):
    def __init__(self, tx_channel, baud_rate=9600):
        # Chống lỗi nếu giao diện truyền vào chuỗi "CH1" thay vì số nguyên 1
        if isinstance(tx_channel, str):
            self.tx_channel = int(tx_channel.replace('CH', '').strip())
        else:
            self.tx_channel = int(tx_channel)
            
        self.baud_rate = int(baud_rate)

    def decode(self, sample_rate, buffer_array):
        transactions = []
        spb = float(sample_rate) / self.baud_rate
        
        # 1. Trích xuất riêng kênh TX
        tx_data = (buffer_array >> self.tx_channel) & 1
        
        # 2. ÉP KIỂU SANG INT8 ĐỂ SỬA LỖI UNDERFLOW TOÁN HỌC
        diff = np.diff(tx_data.astype(np.int8))
        falling_edges = np.where(diff == -1)[0]
        
        skip_until = 0
        for edge_idx in falling_edges:
            if edge_idx < skip_until:
                continue
                
            if edge_idx + int(spb * 10) >= len(tx_data):
                break 

            center_start_idx = int(edge_idx + spb / 2)
            if tx_data[center_start_idx] != 0:
                continue 

            byte_value = 0
            for bit_pos in range(8):
                sample_idx = int(edge_idx + (spb / 2) + ((bit_pos + 1) * spb))
                if sample_idx < len(tx_data):
                    byte_value |= (tx_data[sample_idx] << bit_pos)

            stop_idx = int(edge_idx + (spb / 2) + (9 * spb))
            if stop_idx < len(tx_data) and tx_data[stop_idx] == 1:
                # --- ĐÓNG GÓI CHUẨN ĐẦU RA CHO UI ---
                time_sec = edge_idx / sample_rate
                char_val = chr(byte_value) if 32 <= byte_value <= 126 else '?'
                data_str = f"0x{byte_value:02X} ('{char_val}')"
                
                transactions.append({
                    'time_val': time_sec, # BẮT BUỘC PHẢI CÓ KEY NÀY ĐỂ ĐỒNG BỘ LOG
                    'time': f"{time_sec:.5f}s",
                    'protocol': 'UART',
                    'channel': f"CH{self.tx_channel}",
                    'data': data_str
                })
            
            skip_until = edge_idx + int(spb * 10)

        return transactions