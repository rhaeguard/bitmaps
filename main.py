class BitmapGenerator:

    def __init__(self, raw_pixel_data) -> None:
        self.raw_pixel_data = raw_pixel_data
        self.height = len(raw_pixel_data)
        self.width = len(raw_pixel_data[0])

        self.padding_size_per_row = (self.width * 3) % 4
        if self.padding_size_per_row != 0:
            self.padding_size_per_row = (4 - self.padding_size_per_row)

        pre_header_section=14

        self.bitmap_header_size=40
        self.pixel_section_size_bytes = self.width * self.height * 3 + self.padding_size_per_row * self.height
        self.total_file_size = pre_header_section + self.bitmap_header_size + self.pixel_section_size_bytes
        self.pixel_data_offset = pre_header_section + self.bitmap_header_size

    def persist(self, filename):
        file = open(filename, "wb")

        file.write(b'BM')
        file.write((self.total_file_size).to_bytes(4, 'little')) # file size
        file.write((0).to_bytes(2, 'little')) # reserved 1
        file.write((0).to_bytes(2, 'little')) # reserved 2
        file.write((self.pixel_data_offset).to_bytes(4, 'little')) # offset for pixel data, when the data starts
        file.write((self.bitmap_header_size).to_bytes(4, 'little')) # bitmap info header (BIH) size (including this section)
        file.write((self.width).to_bytes(4, 'little')) # BIH: width
        file.write((self.height).to_bytes(4, 'little')) # BIH: height
        file.write((1).to_bytes(2, 'little')) # BIH: plane count
        file.write((24).to_bytes(2, 'little')) # BIH: bits per pixel (24 = 8 (B) + 8 (G) + 8 (R))
        file.write((0).to_bytes(4, 'little')) # BIH: compression
        file.write((self.pixel_section_size_bytes).to_bytes(4, 'little')) # BIH: byte size of the pixel section => 5x5 x 3 + 5 (padding)
        file.write((0).to_bytes(4, 'little')) # BIH: print resolution
        file.write((0).to_bytes(4, 'little')) # BIH: print resolution
        file.write((0).to_bytes(4, 'little')) # BIH: color index
        file.write((0).to_bytes(4, 'little')) # BIH: important color count

        for r in range(self.height-1, -1, -1):
            for c in range(self.width):
                file.write(
                    self.raw_pixel_data[r][c]
                )
            for _ in range(self.padding_size_per_row):
                file.write(b'\x00')


        file.close()

raw_pixel_data = [
    [b'\x00\x00\xFF', b'\x00\x00\xFF', b'\x00\x00\xFF', b'\x00\x00\xFF', b'\x00\x00\xFF'],
    [b'\x00\x00\xFF', b'\x00\x00\xFF', b'\xFF\xFF\xFF', b'\x00\x00\xFF', b'\x00\x00\xFF'],
    [b'\x00\x00\xFF', b'\xFF\xFF\xFF', b'\xFF\xFF\xFF', b'\xFF\xFF\xFF', b'\x00\x00\xFF'],
    [b'\x00\x00\xFF', b'\x00\x00\xFF', b'\xFF\xFF\xFF', b'\x00\x00\xFF', b'\x00\x00\xFF'],
    [b'\x00\x00\xFF', b'\x00\x00\xFF', b'\x00\x00\xFF', b'\x00\x00\xFF', b'\x00\x00\xFF'],
]

BitmapGenerator(
    raw_pixel_data
).persist("swiss_flag.bmp")