import csv

inverted_idx = {}
with open('jeopardy_csv.csv') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)

    for i, row in enumerate(reader):
        text = ''.join([row[3], row[5], row[6]]).split()
        text = [word.lower() for word in text]
        text = list(set(text))
        # print(i)
        for word in text:
            # print(word)
            if word in inverted_idx:
               inverted_idx[word].append(i)
            else:
                inverted_idx[word] = []
                inverted_idx[word].append(i)
                # print(inverted_idx)
            # break

print(inverted_idx['football'])
print(len(inverted_idx))

