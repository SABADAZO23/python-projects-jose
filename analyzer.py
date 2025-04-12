filename = "mbox.txt"
counts = dict()

with open(filename, 'r') as f:
    for line in f:
        if line.startswith('From: '):
            email = line.split()[1]
            counts[email] = counts.get(email, 0) + 1

for email, count in counts.items():
    print(email, count)