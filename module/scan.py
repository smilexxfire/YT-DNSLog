class Scanner:
    """scan bytes"""
    __mark_offset_byte, __mark_offset_bit = 0, 0

    def __init__(self, data: bytes, offset_byte=0, offset_bit=0):
        self.data = data
        self.__offset_byte = offset_byte
        self.__offset_bit = offset_bit

    def next_bits(self, n=1):
        if n > (len(self.data) - self.__offset_byte) * 8 - self.__offset_bit:
            raise RuntimeError('剩余数据不足{}位'.format(n))
        if n > 8 - self.__offset_bit:
            raise RuntimeError('不能跨字节读取读取位')
        result = self.data[self.__offset_byte] >> 8 - self.__offset_bit - n & (1 << n) - 1
        self.__offset_bit += n
        if self.__offset_bit == 8:
            self.__offset_bit = 0
            self.__offset_byte += 1
        return result

    def next_bytes(self, n=1, convert=True, move=True):
        if not self.__offset_bit == 0:
            raise RuntimeError('当前字节不完整，请先读取完当前字节的所有位')
        if n > len(self.data) - self.__offset_byte:
            raise RuntimeError('剩余数据不足{}字节'.format(n))
        result = self.data[self.__offset_byte: self.__offset_byte + n]
        if move:
            self.__offset_byte += n
        if convert:
            result = int.from_bytes(result, 'big')
        return result

    def next_bytes_until(self, stop, convert=True):
        """ 主要用于获取Question中的QNAME

        """
        if not self.__offset_bit == 0:
            raise RuntimeError('当前字节不完整，请先读取完当前字节的所有位')
        end = self.__offset_byte
        # stop指向一个函数，传入两个参数，分别为字符、偏移量
        # stop函数返回True or False
        while not stop(self.data[end], end - self.__offset_byte):
            end += 1
        # 根据偏移量获取对应区间数据
        result = self.data[self.__offset_byte: end]
        self.__offset_byte = end
        # 转换为字符串
        if convert:
            if result:
                result = map(lambda x: chr(x) if (31 < x < 127) else '.', result)   # 非打印字符以点代替
                result = "".join(list(result))[1:]  # 删除第一个点
            else:
                result = ''
        return result

    def position(self):
        return self.__offset_byte, self.__offset_bit