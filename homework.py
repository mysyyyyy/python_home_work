import os
import pandas as pd


# 不要修改read_subway_data函数的内容
def read_subway_data(file_path):

    data = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                continue

            line = line.split("\t")
            line_name, station_list = line[0], line[-1].split("-")
            is_circle = (line[1] == "环线")

            data[line_name] = {
                "station_list": station_list,
                "is_circle": is_circle
            }

    return data


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
            start_station, end_station = line[0], line[1]
            change_subway_list = line[2].split("-")
            data.append([start_station, end_station, change_subway_list])

    return data


# 不要修改write_data函数的内容
def write_data(file_path, result):
    with open(file_path, "w", encoding="utf-8") as f:

        for i in range(len(result)):
            # === 对于每次的数据进行不同处理 ===
            output = str(result[i])

            f.write("Question %d:\n" % (i + 1))
            f.write("%s\n" % output)


def generate_path(end_station, station_index, station_list, is_visit, paths):
    path = []
    cur_station = end_station
    while is_visit[station_index[cur_station]] != station_index[cur_station]:
        path.append(cur_station)
        cur_station = station_list[is_visit[station_index[cur_station]]]
    path.append(cur_station)
    path.reverse()
    # print(path)
    paths.append(path)


def dfs(cur_station, end_station, change_subway_list, station_index, station_map, station_list, is_visit, paths, subway_index):
    if cur_station == end_station and subway_index == len(change_subway_list) - 1:
        generate_path(end_station, station_index,
                      station_list, is_visit, paths)
        return True
    arrive = False
    for i in range(len(station_list)):
        if is_visit[i] >= 0:
            continue
        for j in range(2):
            temp_subway_index = subway_index + j
            if temp_subway_index >= len(change_subway_list):
                break
            subway = change_subway_list[temp_subway_index]
            if station_map[station_index[cur_station]][i] != subway:
                continue
            is_visit[station_index[station_list[i]]
                     ] = station_index[cur_station]
            ret = dfs(station_list[i], end_station, change_subway_list, station_index,
                      station_map, station_list, is_visit, paths, temp_subway_index)
            if ret:
                arrive = arrive
                arrive = True
            is_visit[station_index[station_list[i]]] = -1
    return arrive


def search_route(subway_data, start_station, end_station, change_subway_list, show_detail=False):
    """
    根据输入的北京地铁数据subway_data，给定起始站start_station和结束站end_station，严格按照change_subway_list换乘地铁,
    从起始站start_station到结束站end_station的距离distance。distance为通过的不同地铁站的数量。
    如果通过环线，存在多条路径，返回distance较小的值。
    如果无法按照换成顺序到达，则返回-1

    [P.S.] 评分标准为：是否能到达判断正确占80%，distance计算正确占20%。例如正确distance为10，你的答案为9，distance计算错误，但是
    10和9都表示能到达，可以的80%分数。但如果你的答案为-1，判断为不能到达，会记为0分。
    预计10个测试样例，最多有2个样例涉及环线。

    :param subway_data: 字典，每个key为地铁线路的名称，value为字典，包含是否为环线，以及按顺序排列的地铁站名。例如
        subway_data["2号线"] = {
            "is_circle": True,
            "station_list": ["西直门", "积水潭", "鼓楼大街", ..., "阜成门", "车公庄"]
        }
        "is_circle"的value为True，表示这条地铁是环路
    :param start_station: 字符串，如: "北京大学东门" 或 "新宫"
    :param end_station: 字符串，如: "苏州街" 或 "西直门"
    :param change_subway_list: 列表，每个元素为代表线路的字符串，如: ["4号线", "13号线"]
    :return:

    example:
        start_station="北京大学东门", end_station="北京大学东门", change_subway_list=["4号线"], answer=1  # 路过一个地铁站
        start_station="北京大学东门", end_station="苏州街", change_subway_list=["4号线", "10号线"], answer=4
        start_station="北京大学东门", end_station="西红门", change_subway_list=["4号线", "1号线"], answer=-1 # 换乘1号线后到不了西红门
        start_station="北京大学东门", end_station="五棵松", change_subway_list=["4号线", "9号线", "1号线"], answer=12
        start_station="安河桥北", end_station="西直门", change_subway_list=["昌平线"], answer=-1
        start_station="复兴门", end_station="西直门", change_subway_list=["2号线"], answer=4  # 2号线是环线
    """

    # constuct graph
    station_list = []
    for value in subway_data.values():
        station_list += value["station_list"]
    station_list = list(set(station_list))
    station_list.sort()
    # print(station_list)
    station_list_length = len(station_list)
    station_index = {}
    for station in station_list:
        station_index[station] = station_list.index(station)
    # print(station_index)
    station_map = []
    for i in range(station_list_length):
        station_map.append(['no' for j in range(station_list_length)])
    is_visit = [-1 for i in range(station_list_length)]
    for key, value in subway_data.items():
        is_circle = value["is_circle"]
        stations = value["station_list"]
        for i in range(len(stations)):
            if i == len(stations) - 1 and not is_circle:
                break
            pre_station = stations[i]
            cur_station = stations[(i + 1) % len(stations)]
            if pre_station != cur_station:
                station_map[station_index[pre_station]
                            ][station_index[cur_station]] = key
                station_map[station_index[cur_station]
                            ][station_index[pre_station]] = key
    # df = pd.DataFrame(station_map, station_list, station_list)
    # df.to_excel('station_map.xlsx')
    is_visit[station_index[start_station]
             ] = station_index[start_station]
    arrive = False
    subway_index = 0
    paths = []
    arrive = dfs(start_station, end_station, change_subway_list,
                 station_index, station_map, station_list, is_visit, paths, subway_index)
    if not arrive:
        distance = -1
    else:
        distance = station_list_length
        for path in paths:
            if distance > len(path):
                distance = len(path)
    if show_detail:
        print("始发站：%s  到达站：%s  换乘顺序：%s  最短距离为：%d站" % (start_station,
              end_station, "-".join(change_subway_list), distance))

    return distance


# 不需要修改main函数
if __name__ == "__main__":

    subway_data = read_subway_data(file_path="./subway.txt")
    input_list = read_data(file_path="./input.txt")

    ouptut_list = []
    show_detail = True

    for start_station, end_station, change_subway_list in input_list:
        try:
            distance = search_route(
                subway_data, start_station, end_station, change_subway_list, show_detail=show_detail)
        except Exception as e:
            print("程序发生错误:", e)
            distance = -2

        ouptut_list.append(distance)

    write_data(file_path="./output.txt", result=ouptut_list)
