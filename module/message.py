import struct
from module.scan import Scanner

class Message:
    u"""All communications inside of the domain protocol are carried in a single format called a message"""

    def __init__(self, data: bytes, header=None, question=None, answer=None, authority=None, additional=None):
        self.data = data
        self.header = header
        self.question = question
        self.answer = answer
        self.authority = authority
        self.additional = additional

    def get_header(self, scanner):
        header = dict()
        header['ID'] = scanner.next_bytes(2)
        header['QR'] = scanner.next_bits(1)
        header['OPCODE'] = scanner.next_bits(4)
        header['AA'] = scanner.next_bits(1)
        header['TC'] = scanner.next_bits(1)
        header['RD'] = scanner.next_bits(1)
        header['RA'] = scanner.next_bits(1)
        header['Z'] = scanner.next_bits(3)
        header['RCODE'] = scanner.next_bits(4)
        header['QDCOUNT'] = scanner.next_bytes(2)
        header['ANCOUNT'] = scanner.next_bytes(2)
        header['NSCOUNT'] = scanner.next_bytes(2)
        header['ARCOUNT'] = scanner.next_bytes(2)
        self.header = header

    def get_question(self, scanner):
        questions = list()
        for _ in range(self.header['QDCOUNT']):
            question = dict()
            question['QNAME'] = scanner.next_bytes_until(lambda current, _: current == 0)
            scanner.next_bytes(1)  # 跳过0
            question['QTYPE'] = scanner.next_bytes(2)
            question['QCLASS'] = scanner.next_bytes(2)
            questions.append(question)
        self.question = questions

    @classmethod
    def from_bytes(cls, data: bytes):
        message = Message(data)
        scanner = Scanner(data)
        # 读取header
        message.get_header(scanner)
        # 读取question
        message.get_question(scanner)
        # 初始化answer、authority、additional
        answer, authority, additional = list(), list(), list()
        message.answer = answer
        message.authority = authority
        message.additional = additional
        return message

    def transfer_to_answer(self):
        rr = {
            "NAME": 0xc00c,
            "TYPE": 0x01,           # A记录
            "CLASS": 0x01,
            "TTL": 60,              # 存活1分钟
            "RDLENGTH": 0x04,
            "RDATA": "127.0.0.1"    # 记录值
        }
        self.answer.append(rr)
        self.header['QR'] = 0x01
        self.header['ANCOUNT'] +=1


    def to_bytes(self):
        def get_flag():
            return (self.header['QR'] << 15) | (self.header['OPCODE'] << 11) |\
                   (self.header['AA'] << 10) | (self.header['TC'] << 9) | (self.header['RD'] << 8) |\
                   (self.header['RA'] << 7) | (self.header['Z'] << 4) | (self.header['RCODE'])
        # 封装头部
        res = struct.pack('>HHHHHH', self.header['ID'], get_flag(), self.header['QDCOUNT'],
                            self.header['ANCOUNT'], self.header['NSCOUNT'], self.header['ARCOUNT'])
        # 封装Question
        pos = 13 + self.data[12:].find(b'\x00')
        res = res + self.data[12:pos]
        res = res + struct.pack(">HH", self.question[0]['QTYPE'], self.question[0]['QCLASS'])
        # 封装Answer
        for rr in self.answer:
            res = res + struct.pack('>HHHIH', rr['NAME'], rr['TYPE'], rr['CLASS'],
                                    rr['TTL'], rr['RDLENGTH'])
            s = rr['RDATA'].split('.')
            res = res + struct.pack('>BBBB', int(s[0]), int(s[1]), int(s[2]), int(s[3]))
        return res