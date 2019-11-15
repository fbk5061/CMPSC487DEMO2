filepath = '/home/jbb5882/NOV_Avail_Dates'
availDates = []
with open(filepath) as fp:
	line = fp.readline()
	availDates.append(line)
	while line:
		line = fp.readline()
		availDates.append(line);

file = '/home/jbb5882/test'
with open(file) as f:
	date = f.readline()
	x = date in availDates
	print(x)
