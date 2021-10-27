import os
import csv
import datetime


# 不要修改read_data函数的内容
def read_data(file_path):
    data = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                continue

            # === 对于每次的数据进行不同处理 ===
            line = line.split("\t")
            start_date, end_date = line[0], line[1]
            data.append([start_date, end_date])

    return data


# 不要修改write_data函数的内容
def write_data(file_path, result):
    with open(file_path, "w", encoding="utf-8") as f:

        for i in range(len(result)):
            # === 对于每次的数据进行不同处理 ===
            output = str(result[i])

            f.write("Question %d:\n" % (i + 1))
            f.write("%s\n" % output)


def read_stock_data(file_path):
    """
    根据输入的文件路径，读入股票信息
    :param file_path: 存储股票信息的csv文件路径
    :return:
    """

    data = []
    csv_file = csv.reader(open('./stock_data.csv', 'r', encoding='utf-8'))
    first_line = True
    for line in csv_file:
        if first_line:
            first_line = False
            continue
        data.append(line)
    return data


def find_data_in_date(data, date):
    data.insert(0, ['0000-00-00', '0', '0', '0', '0'])
    for i in range(len(data) - 1):
        pre_data = data[i]
        cur_data = data[i + 1]
        if pre_data[0] < date and date <= cur_data[0]:
            return cur_data


def find_best_stock(stock_data, start_date, end_date, show_detail=False):
    """
    根据给定的2019年股票数据（每日股票的开盘价，收盘价等），求出在给定买入日期和卖出日期的情况下，涨幅最高的股票。返回股票的代码，例如“600150.XSHG”
    为求简单，我们定义：涨幅 = (卖出日收盘价 - 买入日收盘价) / 买入日收盘价
    如果买入或卖出的日期不是交易日，则会在此日期之后，最近的交易日进行买入or卖出。
    :param stock_data: 自行读入的股票数据。
    :param start_date: 买入日期，字符串类型，例如“2019-01-01”，注意：给定日期可能不是交易日
    :param end_date: 卖出日期，字符串类型，例如“2019-02-01”，注意：给定日期可能不是交易日
    :return:
    """

    best_stock = ""

    stock_map = {}
    for data in stock_data:
        stock_map[data[0]] = []
    for data in stock_data:
        stock_map[data[0]].append(data[1:])
    for data in stock_map.values():
        sorted(data, key=lambda x: x[0], reverse=True)
    # print(stock_map)
    stock_list = []
    max_growth = 0
    for stock, data in stock_map.items():
        start_data = find_data_in_date(data, start_date)
        end_data = find_data_in_date(data, end_date)
        growth = (float(end_data[2]) -
                  float(start_data[2])) / float(start_data[2])
        if max_growth < growth:
            max_growth = growth
            best_stock = stock

    if show_detail:
        print("如果从%s买入，%s卖出，赚的最多的股票为：%s" % (start_date, end_date, best_stock))

    return best_stock


# 不需要修改main函数
if __name__ == "__main__":

    input_list = read_data(file_path="./input.txt")
    stock_data = read_stock_data(file_path="./stock_data.csv")

    ouptut_list = []
    show_detail = True

    for start_date, end_date in input_list:
        try:
            stock_index = find_best_stock(
                stock_data, start_date, end_date, show_detail=show_detail)
        except Exception as e:
            print("程序发生错误:", e)
            stock_index = "Null"

        ouptut_list.append(stock_index)

    write_data(file_path="./output.txt", result=ouptut_list)
