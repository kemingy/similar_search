class SimHash:
    def __init__(self, bit=64, limit=3):
        self.bit = bit
        self.limit = limit
        self.docs = []

    def __compute_bits(self, text):
        word_hash = []
        for word in text:
            word_hash.append(hash(word))

        hash_bits = []
        while len(hash_bits) < self.bit:
            bit = 0
            for i, word in enumerate(word_hash):
                if word & 1:
                    bit += 1
                else:
                    bit -= 1

                word_hash[i] = word >> 1

            hash_bits.append(bit)

        # print(hash_bits)
        return int(''.join(['1' if b > 0 else '0' for b in hash_bits[::-1]]), 2)

    def __hamming_distance(self, x, y):
        return bin(x ^ y).count('1')

    def add_doc(self, text):
        text_bits = self.__compute_bits(text)
        for doc in self.docs:
            if self.__hamming_distance(doc, text_bits) < self.limit:
                return False

        self.docs.append(text_bits)
        return True

    def compare(self, x, y):
        bit_x = self.__compute_bits(x)
        bit_y = self.__compute_bits(y)
        print('x: {}\ny: {}'.format(bin(bit_x), bin(bit_y)))
        return self.__hamming_distance(bit_x, bit_y)


class SegmentSimHash(SimHash):
    def __init__(self, bit, limit, num_segment):
        super().__init__(bit, limit)
        self.docs = [{}] * num_segment



if __name__ == '__main__':
    simhash = SimHash()
    print(simhash.compare('we all scream for ice cream', 'we all scream for ice'))
