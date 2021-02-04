import csv
import collections


def generate_participation_file(input_filename, output_filename):
    section = input_filename[0]

    # return a sorted dic with {email: [name, email, False, duration]}
    order_dic = extract_participation(input_filename, section)

    if output_filename == ".csv":
        print("Building init report")
        init_writing("{}-lab1".format(section)+".csv", order_dic, section)
    else:
        print("Building update report")
        writing(output_filename, order_dic, section)


def writing(output_filename, order_dic, section):
    # return a lab number based on previous lab number
    lab = get_lab(output_filename)
    newfilename = output_filename.split("-")[0] + "-lab{0}".format(lab, section) + ".csv"
    with open('outputCSV/{0}'.format(output_filename), 'r', newline='') as input_file:
        spamreader = csv.reader(input_file)
        with open('outputCSV/{0}'.format(newfilename), 'w+', newline='') as output_file:
            writer = csv.writer(output_file)
            line = 0
            for row in spamreader:
                line += 1
                if line == 1:
                    writer.writerow(row + ["lab{}".format(lab)])
                else:
                    email = row[1]
                    status = get_status(order_dic[email])
                    writer.writerow(row + [status])
    print('Output file saved as: ' + 'outputCSV/{0}'.format(newfilename))


def init_writing(output_filename, order_dic, section):
    with open('outputCSV/{0}'.format(output_filename), 'w+', newline='') as output_file:
        fieldnames = ['Name', 'Email', 'Lab1']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for value in order_dic.values():
            status = get_status(value)
            writer.writerow({'Name': value[0], 'Email': value[1], 'Lab1': status})
    print('Initial output file saved as: '+'outputCSV/{0}'.format(output_filename))


# calculate based on if on-time and accumulative duration
def get_status(value: []) -> str:
    status = "Absent"
    student_is_on_time = value[2]
    duration = value[3]
    if student_is_on_time and duration >= 10:
        status = "Present"
    elif student_is_on_time and duration < 10:
        status = "Left Early"
    elif duration >= 10:
        status = "Late"
    return status


def university_email(email: str) -> bool:
    split_email = email.split("@")
    if len(split_email) == 2 and split_email[1] == "illinois.edu":
        return True
    return False


def participation(row: [], section) -> (bool, int):
    on_time_result = False
    duration = 0

    join_time = row[2]
    leave_time = row[3]

    join_time = join_time.split(" ")[1].split(":")
    leave_time = leave_time.split(" ")[1].split(":")

    join_hour = int(join_time[0])
    join_minute = int(join_time[1])

    leave_hour = int(leave_time[0])
    leave_minute = int(leave_time[1])

    begin_hour = get_begin_time(section)

    if join_hour < begin_hour and leave_hour > begin_hour-1:
        join_hour = begin_hour
        join_minute = 0

    if leave_hour < begin_hour:
        leave_hour = begin_hour
        leave_minute = 0

    if join_hour == begin_hour and join_minute <= 5:
        on_time_result = True
        duration += max(0, leave_minute - join_minute) + (leave_hour - join_hour) * 60
    elif join_hour == begin_hour and join_minute > 5:
        on_time_result = False
        duration += max(0, leave_minute - join_minute) + (leave_hour - join_hour) * 60
    return on_time_result, duration


def get_lab(output_filename) -> int:
    lab = 1
    with open('outputCSV/{0}'.format(output_filename), 'r', newline='') as file:
        spamreader = csv.reader(file)
        lab = 1
        for row in spamreader:
            lab_label = row[-1]
            number: str = lab_label[-1]
            if number.isdigit():
                lab = int(number) + 1
            break
    return lab


def get_begin_time(section:str)-> int:
    if section == "B":
        return 15
    return 9


def extract_participation(input_filename, section) -> dict:
    with open('inputCSV/{0}'.format(input_filename), newline='') as inputfile:
        # spamreader = csv.reader(inputfile, delimiter=' ', quotechar='|')
        spamreader = csv.reader(inputfile)

        dic = {}

        """
        original input
        row:
            [name, email, join, leave, duration, guest]
        """
        row_num = 0
        for row in spamreader:
            row_num += 1
            if row_num == 1:
                continue
            # if row_num == 3:  # for test purpose
            #     break
            name: str = row[0]
            email: str = row[1]
            if not university_email(email):  # ignore non-university email
                continue

            is_on_time, duration = participation(row, section)
            if email not in dic:
                dic[email] = [name, email, is_on_time, duration]
            else:
                dic[email][2] = (dic[email][2] or is_on_time)
                dic[email][3] += duration

    # dic[email] = [name, email, False, duration]
    order_dic = collections.OrderedDict(sorted(dic.items()))
    return order_dic


def main():
    input_name = input("Enter the input CSV filename: ")
    exist_name = input("Enter the filename for previous lab that you want to inherit: ")

    input_name = input_name + ".csv"
    exist_name = exist_name + ".csv"
    generate_participation_file(input_name, exist_name)
    print("Finished.")


# execute the script
main()