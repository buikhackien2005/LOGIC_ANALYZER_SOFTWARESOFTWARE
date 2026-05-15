import numpy as np
from .base_decoder import ProtocolDecoder

class SPIDecoder(ProtocolDecoder):
    def __init__(self, sck_channel, mosi_channel, cpol=0, cpha=0, bit_order='MSB'):
        # Chống lỗi kiểu dữ liệu từ giao diện
        self.sck_channel = int(str(sck_channel).replace('CH', '').strip())
        self.mosi_channel = int(str(mosi_channel).replace('CH', '').strip())
        self.cpol = int(cpol)
        self.cpha = int(cpha)
        self.bit_order = bit_order

    def decode(self, sample_rate, buffer_array):
        transactions = []
        sck = (buffer_array >> self.sck_channel) & 1
        mosi = (buffer_array >> self.mosi_channel) & 1
        
        # ÉP KIỂU INT8 CHỐNG UNDERFLOW
        sck_diff = np.diff(sck.astype(np.int8))
        
        if self.cpol == self.cpha:
            sample_edges = np.where(sck_diff == 1)[0]
        else:
            sample_edges = np.where(sck_diff == -1)[0]
            
        for i in range(0, len(sample_edges) - 7, 8):
            byte_val = 0
            chunk = sample_edges[i:i+8]
            
            for bit_idx, sample_pos in enumerate(chunk):
                bit = mosi[sample_pos]
                if self.bit_order == 'MSB':
                    byte_val |= (bit << (7 - bit_idx))
                else:
                    byte_val |= (bit << bit_idx)
            
            time_sec = chunk[0] / sample_rate
            transactions.append({
                'time_val': time_sec,
                'time': f"{time_sec:.5f}s",
                'protocol': 'SPI',
                'channel': f"SCK:CH{self.sck_channel}|MOSI:CH{self.mosi_channel}",
                'data': f"0x{byte_val:02X}"
            })
            
        return transactions