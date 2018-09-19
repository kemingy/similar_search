from collections import Counter

def cosine(x, y):
    feature_x = Counter(x.split(' '))
    feature_y = Counter(y.split(' '))

    molecular = sum([feature_x[k] * feature_y[k] 
                     for k in feature_x if k in feature_y])
    denominator = sum(feature_x.values()) ** 0.5 * sum(feature_y.values()) ** 0.5
    return molecular / denominator


if __name__ == '__main__':
    text = ['we all scream for ice cream', 'we all scream for ice']
    print(cosine(text[0], text[1]))
