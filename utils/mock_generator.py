import numpy as np

class MockDataGenerator:
    """Class cung cấp dữ liệu giả lập đa giao thức, trực quan và phức tạp để báo cáo."""

    @staticmethod
    def get_8ch_mock_data():
        sample_rate = 500000  # 500 kHz
        num_samples = 50000   # 100 ms

        time_array = np.arange(num_samples) / sample_rate

        # Khởi tạo mảng 8-bit toàn số 1 (0xFF - Mức CAO cho tất cả các kênh)
        buffer = np.full(num_samples, 255, dtype=np.uint8)

        # ĐÃ FIX BUG OVERFLOW: Dùng 255 - (1 << ch) để luôn ra số dương <= 255
        def set_low(start, end, ch):
            buffer[start:end] &= (255 - (1 << ch))

        def set_high(start, end, ch):
            buffer[start:end] |= (1 << ch)

        # --- CH0: XUNG CLOCK (Nhấp nháy đều đặn) ---
        for i in range(0, num_samples, 500):
            set_low(i, i + 250, 0)

        # --- CH1: UART TX (9600 bps) - Gửi chữ "O" và "K" ---
        spb_uart = int(sample_rate / 9600)
        def draw_uart(start_idx, char_val):
            set_low(start_idx, start_idx + spb_uart, 1) # Start bit
            for i in range(8):
                idx = start_idx + spb_uart * (i + 1)
                if not ((char_val >> i) & 1):
                    set_low(idx, idx + spb_uart, 1)

        draw_uart(2000, 0x4F) # Chữ 'O'
        draw_uart(2000 + spb_uart * 12, 0x4B) # Chữ 'K'

        # --- CH2 (SDA) & CH3 (SCL): I2C ---
        spb_i2c = 100 
        start_i2c = 15000
        # Start Condition
        set_low(start_i2c, start_i2c + spb_i2c, 2)
        set_low(start_i2c + spb_i2c//2, start_i2c + spb_i2c, 3)

        byte_i2c = 0x78 # Địa chỉ 0x3C
        curr = start_i2c + spb_i2c
        for bit in range(7, -1, -1):
            if (byte_i2c >> bit) & 1: set_high(curr, curr + spb_i2c, 2)
            else: set_low(curr, curr + spb_i2c, 2)
            set_low(curr, curr + spb_i2c//4, 3)
            set_high(curr + spb_i2c//4, curr + spb_i2c*3//4, 3)
            set_low(curr + spb_i2c*3//4, curr + spb_i2c, 3)
            curr += spb_i2c

        # Bit ACK
        set_low(curr, curr + spb_i2c, 2)
        set_low(curr, curr + spb_i2c//4, 3)
        set_high(curr + spb_i2c//4, curr + spb_i2c*3//4, 3)
        set_low(curr + spb_i2c*3//4, curr + spb_i2c, 3)
        curr += spb_i2c
        # Stop Condition
        set_high(curr, curr + spb_i2c, 3)
        set_low(curr, curr + spb_i2c//2, 2)
        set_high(curr + spb_i2c//2, curr + spb_i2c, 2)

        # --- CH4 (CS), CH5 (SCK), CH6 (MOSI): SPI ---
        set_low(0, num_samples, 5) # Idle Low
        set_low(0, num_samples, 6) # Idle Low

        spb_spi = 50
        start_spi = 30000

        set_low(start_spi, start_spi + spb_spi * 10, 4) # CS xuống thấp
        curr = start_spi + spb_spi
        byte_spi = 0x55 
        for bit in range(7, -1, -1):
            if (byte_spi >> bit) & 1: set_high(curr, curr + spb_spi, 6)
            else: set_low(curr, curr + spb_spi, 6)
            set_high(curr + spb_spi//2, curr + spb_spi, 5)
            curr += spb_spi

        set_high(curr, num_samples, 4)
        set_low(curr, num_samples, 6)

        return time_array, buffer