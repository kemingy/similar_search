class SimHash:
    def __init__(self, bit=64, limit=3):
        self.bit = bit
        self.limit = limit
        self.docs = []

    def compute_bits(self, text):
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

    def hamming_distance(self, x, y):
        return bin(x ^ y).count('1')

    def add_doc(self, text):
        text_bits = self.compute_bits(text)
        for doc in self.docs:
            if self.hamming_distance(doc, text_bits) < self.limit:
                return False

        self.docs.append(text_bits)
        return True

    def compare(self, x, y):
        bit_x = self.compute_bits(x)
        bit_y = self.compute_bits(y)
        print('x: {}\ny: {}'.format(bin(bit_x), bin(bit_y)))
        return self.hamming_distance(bit_x, bit_y)


class SegmentSimHash(SimHash):
    def __init__(self, bit=64, limit=3, num_segment=4):
        super().__init__(bit, limit)
        self.docs = {}

        assert bit % num_segment == 0
        self.num_segment = num_segment
        self.seg_length = bit // num_segment
        self.masks = [int('1' * self.seg_length + '0' * self.seg_length * i, 2) 
                      for i in range(num_segment)]

    def compute_segments(self, text):
        text_bits = super().compute_bits(text)
        segments = [(text_bits & self.masks[i]) >> i * self.seg_length 
                    for i in range(self.num_segment)]

        return text_bits, segments

    def add_doc(self, text):
        text_bits, segments = self.compute_segments(text)

        # find similar doc
        for seg in segments:
            if seg in self.docs:
                for doc_seg in self.docs[seg]:
                    if super().hamming_distance(text_bits, doc_seg) < self.limit:
                        return False

        # add to docs
        for seg in segments:
            if seg not in self.docs:
                self.docs[seg] = set()
            self.docs[seg].add(text_bits)

        return True


if __name__ == '__main__':
    text = ['we all scream for ice cream', 'we all scream for ice']
    simhash = SimHash()
    print(simhash.compare(text[0], text[1]))

    segment = SegmentSimHash()
    for t in text:
        segment.add_doc(t)

    print(segment.docs)
