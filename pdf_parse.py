import csv


class DataBlock:

    def prepare_data(self, s):
        return [el for el in s[:-1].split(" ") if el != "" and el != ","]

    def __init__(self, f, first_line, writer):
        sub_index = 0
        self.blocks = []
        flag = False
        while True:
            sub_index += 1
            if sub_index % 1000 == 0:
                print("Sub index", sub_index)
            if sub_index > 1000000:
                return
            if first_line.find("Operated") != -1 or first_line == "" or first_line == "\n":
                first_line = f.readline()
                continue
            if first_line.find("FROM") != -1:
                if flag:
                    break
                flag = True

                self.first_from = []
                cur_line = self.prepare_data(first_line)[1:]
                index = 0
                for s in cur_line:
                    index += 1
                    if s.find("FROM") != -1:
                        break
                    else:
                        self.first_from.append(s)

                cur_line = cur_line[index:]
                self.second_from = []
                for s in cur_line:
                    self.second_from.append(s)

                self.first_to = []
                cur_line = self.prepare_data(f.readline())[1:]
                index = 0
                for s in cur_line:
                    index += 1
                    if s.find("TO") != -1:
                        break
                    else:
                        self.first_to.append(s)

                cur_line = cur_line[index:]
                self.second_to = []
                for s in cur_line:
                    self.second_to.append(s)

                cur_l = f.readline()
                print(self.first_from, self.first_to)
                while not (len(cur_l.split(" ")) > 0 and cur_l.split(" ")[0].isdigit()):
                    cur_l = f.readline()
                    if cur_l.find("FROM") != -1:
                        self.last_line = cur_l
                        return
                else:
                    first_line = cur_l[:-1]
            else:
                pair = DataPair(first_line, self.first_from, self.first_to, self.second_from, self.second_to)
                pair.print_to_csv(writer)

                # self.blocks.append(pair.get_first_line())
                # if pair.has_second_line():
                #     self.blocks.append(pair.get_second_line())

                first_line = f.readline()[:-1]

        self.last_line = first_line

    def print(self):
        for block in self.blocks:
            block.print()

    def len(self):
        return len(self.blocks)

    def print_to_csv(self, writer):
        for block in self.blocks:
            block.print_to_csv(writer)


class DataPair:
    def __init__(self, line, first_from, first_to, second_from, second_to):
        self.lines = []

        line = line.split(" ")
        line = [el for el in line if el != ""]

        line = self.parse_data_line(line, first_from, first_to)
        self.parse_data_line(line, second_from, second_to)

    def parse_data_line(self, line, from_value, to_value):
        if len(line) == 0 or line[0] == "Consult":
            return []

        validity = Date(line)
        cur_line = line[5:]
        days = []
        index = 0
        for day in cur_line:
            if day.isdigit():
                days.append(day)
                index += 1
            else:
                break
        cur_line = cur_line[index:]
        dep_time = cur_line[0]
        cur_line = cur_line[1:]
        arr_time = cur_line[0]
        cur_line = cur_line[1:]
        flight = cur_line[0]
        cur_line = cur_line[1:]
        aircraft = cur_line[0]
        cur_line = cur_line[1:]
        travel_time = cur_line[0].replace("\n", "")
        cur_line = cur_line[1:]

        self.lines.append(
            DataLine(validity, days, dep_time, arr_time, flight, aircraft, travel_time, from_value, to_value))

        return cur_line

    def get_first_line(self):
        return self.lines[0]

    def has_second_line(self):
        return len(self.lines) > 1

    def get_second_line(self):
        return self.lines[1]

    def print_to_csv(self, writer):
        self.lines[0].print_to_csv(writer)
        if self.has_second_line():
            self.lines[1].print_to_csv(writer)


class DataLine:
    def __init__(self, validity, days, dep_time, arr_time, flight, aircraft, travel_time, from_value, to_value):
        self.validity = validity
        self.days = days
        self.dep_time = dep_time
        self.arr_time = arr_time
        self.flight = flight
        self.aircraft = aircraft
        self.travel_time = travel_time
        self.from_value = from_value
        self.to_value = to_value

    def print(self):
        self.validity.print()
        print("|", end="")
        print(self.days, end="|")
        print(self.dep_time, end="|")
        print(self.arr_time, end="|")
        print(self.flight, end="|")
        print(self.aircraft, end="|")
        print(self.travel_time)

    def print_to_csv(self, writer):
        data = [self.validity.to_string(), ", ".join(self.days), self.dep_time, self.arr_time, self.flight,
                self.aircraft, self.travel_time, self.from_value, self.to_value]
        writer.writerow(data)


class Date:
    def __init__(self, splitted):
        self.start_day = int(splitted[0])
        self.start_month = splitted[1]

        self.end_day = int(splitted[3])
        self.end_month = splitted[4][:-1]

    def print(self):
        print(self.start_day, end=" ")
        print(self.start_month, end=" ")
        print(self.end_day, end=" ")
        print(self.end_month, end="")

    def to_string(self):
        return str(self.start_day) + " " + self.start_month + " - " + str(self.end_day) + " " + self.end_month


file = open("target3.txt", "r")
f = open('csv_file.csv', 'w')

header = ["validity", "days", "dep_time", "arr_time", "flight", "aircraft", "travel_time", "from_value", "to_value"]
writer = csv.writer(f)
writer.writerow(header)

l = file.readline()
errors = 0
correct = 0
index = 0
for i in range(20000):
    try:
        index += 1
        if index % 100 == 0:
            print(index)
        d = DataBlock(file, l, writer)
        # if d.len() > 0:
        correct += 1
            # d.print_to_csv(writer)
        l = d.last_line
    except:
        print("THAT ALL")
        break

print("CORRECTS " + str(correct))
print("ERRORS " + str(errors))

f.close()
