import numpy as np
from .base_decoder import ProtocolDecoder

class SPIDecoder(ProtocolDecoder):
    def __init__(self, sck_channel, mosi_channel, cpol=0, cpha=0, bit_order='MSB'):
        self.sck_channel = sck_channel
        self.mosi_channel = mosi_channel
        self.cpol = cpol
        self.cpha = cpha
        self.bit_order = bit_order

    def decode(self, sample_rate, buffer_array):
        transactions = []
        sck = (buffer_array >> self.sck_channel) & 1
        mosi = (buffer_array >> self.mosi_channel) & 1
        
        # Quyết định sườn lấy mẫu: 
        # Nếu CPOL == CPHA -> Lấy mẫu ở sườn LÊN (Rising)
        # Nếu CPOL != CPHA -> Lấy mẫu ở sườn XUỐNG (Falling)
        if self.cpol == self.cpha:
            sample_edges = np.where(np.diff(sck) == 1)[0]
        else:
            sample_edges = np.where(np.diff(sck) == -1)[0]
            
        # Duyệt qua các sườn xung để gom thành từng byte (8 bits)
        for i in range(0, len(sample_edges) - 7, 8):
            byte_val = 0
            chunk = sample_edges[i:i+8] # Lấy 8 sườn liên tiếp
            
            for bit_idx, sample_pos in enumerate(chunk):
                bit = mosi[sample_pos]
                if self.bit_order == 'MSB':
                    byte_val |= (bit << (7 - bit_idx))
                else:
                    byte_val |= (bit << bit_idx)
            
            time_sec = sample_edges[i] / sample_rate
            transactions.append({
                'time_val': time_sec,  # Dùng để sắp xếp logic sau này
                'time': f"{time_sec:.5f}s",
                'protocol': 'SPI',
                'channel': f"SCK:{self.sck_channel}|MOSI:{self.mosi_channel}",
                'data': f"0x{byte_val:02X}"
            })
            
        return transactions