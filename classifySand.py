import os
import random
import math
#DMatlas导出的带有砂体/河道位置和极大极小物性的.cmg文件
Dmatlas_sandGrid_filename = "Lu2_SR20.cmg"
#提取文件名（不含后缀）
DM_sandGrid_Poro_filename = os.path.splitext(Dmatlas_sandGrid_filename)[0] + "NewPoro.txt"

#拥有正态分布物性的分配文件
norm_poro_modified_filename = "normPoroMod-SN60%.txt"#z-2.0的normal孔隙度，sandNum=60%
big_poro_filename = "BigPoro.txt"
small_poro_filename = "SmallPoro.txt"

final_poro_filename = os.path.splitext(Dmatlas_sandGrid_filename)[0] + "FinalPoro.txt"
blank_cmg_filename = "Lu2gridOrigin _blank.cmg"
#最终结果文件
final_cmg_filename = os.path.splitext(Dmatlas_sandGrid_filename)[0] + "z2.1.cmg"

#***处理DM导出的.cmg文件，导出孔隙度文件***
# 标志，表示当前是否在 "PORO" 到 "PERMI" 范围内
in_range = False

with open(Dmatlas_sandGrid_filename, 'r') as input_file, open(DM_sandGrid_Poro_filename, 'w') as output_file:
    for line in input_file:
        # 去除行首和行尾的空格和换行符
        line = line.strip()

        # 如果找到了 "PORO"，标志置为 True
        if line == "*POR *ALL":
            print("找到Poro")
            in_range = True
            continue

        # 如果找到了 "PERMI"，标志置为 False 并结束循环
        if line == "*PERMI *ALL":
            print("找到Perm")
            in_range = False
            break

        # 如果在范围内，处理数值并写入输出文件
        if in_range:
            values = line.split('		')  # 数值之间用制表符分隔
            new_line = []
            for value in values:
                try:
                    float_value = float(value)
                    if float_value >= 0.48:# 区分砂体的孔隙度设置;河道最好用0.1，随机砂体0.48
                        new_line.append("1")
                    else:
                        new_line.append("0")
                except ValueError:
                    # 如果无法转换为浮点数，保持原样
                    new_line.append(value)
            output_file.write("		".join(new_line) + "\n")

print("处理完成，并已写入到", DM_sandGrid_Poro_filename)

#***把孔隙度文件按地层分类，每个地层的孔隙度再按照大小排序***
#***排序后区分砂体位置的孔隙度，分类后随机输出，汇总为大小两个孔隙度文件***

# 初始化各层砂体网格计数器
aa1_count = 0
bb1_count = 0
cc1_count = 0
dd1_count = 0
ee1_count = 0

# 定义范围
aa = 11664 # shanxi网格数
bb = aa + 116640
cc = bb + 233280
dd = cc + 349920
ee = dd + 583200

with open(DM_sandGrid_Poro_filename, 'r') as input_file:

    value_count = 0  # 用于跟踪读取的数值个数
    for line in input_file:
        values = line.strip().split('		')  # 以制表符分隔值
        for value in values:
            value_count += 1  # 每读取一个数值，增加计数

            if value_count <= aa:
                if value == "1":
                    aa1_count += 1
            elif aa < value_count <= bb:
                if value == "1":
                    bb1_count += 1
            elif bb < value_count <= cc:
                if value == "1":
                    cc1_count += 1
            elif cc < value_count <= dd:
                if value == "1":
                    dd1_count += 1
            elif dd < value_count <= ee:
                if value == "1":
                    ee1_count += 1
print ("value_count =",value_count)# 此处很奇怪，读取了233,0467个网格数据，但是一共才1294704个网格


print("由下往上每层含有砂体网格数分别为",aa1_count,bb1_count,cc1_count,dd1_count,ee1_count)

a = 11664
b = 116640
c = 233280
d = 349920
e = 583200

a1 = aa1_count
b1 = bb1_count
c1 = cc1_count
d1 = dd1_count
e1 = ee1_count

# 初始化一个空的列表，用于存储数据
data = []

# 打开随机高斯分布的孔隙度文件并逐行读取数据
with open(norm_poro_modified_filename, "r") as file:
    for line in file:
        # 去除行首和行尾的空格和换行符
        line = line.strip()
        
        # 如果行不为空，再尝试将字符串转换为浮点数
        if line:
            values = line.split()
            for value in values:
                data.append(float(value))

# 将数据按顺序分为5段，每段的数据个数分别为a, b, c, d, e

# 取出首先读取的shanxi组的数据，进行从大到小排序
segment1 = sorted(data[0:a], reverse=True)
# shihezi
segment2 = sorted(data[a:a+b], reverse=True)
#shiqianfeng
segment3 = sorted(data[a+b:a+b+c], reverse=True)
#liujiagou
segment4 = sorted(data[a+b+c:a+b+c+d], reverse=True)
#heshanggou
segment5 = sorted(data[a+b+c+d:a+b+c+d+e], reverse=True)

# 筛选出砂体个数的数据，进行随机排列
segment11 = segment1[:a1]
segment12 = segment1[a1:a]

segment21 = segment2[:b1]
segment22 = segment2[b1:b]

segment31 = segment3[:c1]
segment32 = segment3[c1:c]

segment41 = segment4[:d1]
segment42 = segment4[d1:d]

segment51 = segment5[:e1]
segment52 = segment5[e1:e]

random.shuffle(segment11)
random.shuffle(segment12)
random.shuffle(segment21)
random.shuffle(segment22)
random.shuffle(segment31)
random.shuffle(segment32)
random.shuffle(segment41)
random.shuffle(segment42)
random.shuffle(segment51)
random.shuffle(segment52)

# 合并成一个列表
big_poro_data = segment11 + segment21 + segment31 + segment41 + segment51
small_poro_data = segment12 + segment22 + segment32 + segment42 + segment52

# 打开文本文件以写入数据
with open(big_poro_filename, "w") as output_file:
    for i, item in enumerate(big_poro_data, start=1):
        # 每五个数据换行
        if i % 5 == 0:
            output_file.write(str(item) + "\n")
        else:
            output_file.write(str(item) + "		")  # 制表符分隔

    # 如果最后一行不足五个数据，添加换行符
    if len(big_poro_data) % 5 != 0:
        output_file.write("\n")

with open(small_poro_filename, "w") as output_file:
    for i, item in enumerate(small_poro_data, start=1):
        # 每五个数据换行
        if i % 5 == 0:
            output_file.write(str(item) + "\n")
        else:
            output_file.write(str(item) + "		")  # 制表符分隔

    # 如果最后一行不足五个数据，添加换行符
    if len(small_poro_data) % 5 != 0:
        output_file.write("\n")

## ***最后一步，将三个文件进行一一替换***
def read_values(filename):
    with open(filename, 'r') as file:
        for line in file:
            for value in line.strip().split('		'):
                yield value

# 逐个读取数值
a_values = read_values(DM_sandGrid_Poro_filename)
b_values = read_values(big_poro_filename)
c_values = read_values(small_poro_filename)

output = []
try:
    for value_a in a_values:
        if value_a == '1':
            output.append(next(b_values))
        else:
            output.append(next(c_values))
except StopIteration:
    pass  # 生成器遍历完，结束循环

# 将结果写入新的文本文件
with open(final_poro_filename, 'w') as output_file:
    for i in range(0, len(output), 5):
        output_file.write('		'.join(output[i:i+5]) + '\n')

print ("已完成替换，将正态随机孔隙度按大小输出到砂体位置，输出文件为", final_poro_filename)


# 按照指定公式计算孔隙度并保留指定的小数位数
def calculate_exponential(numbers, multiplier, addend, decimal_places):
    return [round(10**(multiplier * num + addend), decimal_places) for num in numbers]

# 主处理函数
def process_and_output(input_filename, output_filename, aa, bb, cc, dd, ee, decimal_places):
    numbers = []

    with open(input_filename, 'r') as infile:
        for line in infile:
            numbers.extend(map(float, line.strip().split()))

    all_results = []
    #2.0版本渗透率计算
    for value in numbers[:aa]:
        if value >= 0.04:#porosity of sand#
            #2.0版本，纵向物性差异
            #aa_results = calculate_exponential([value], 22.49845, -3.2759, decimal_places)
            #2.1
            aa_results = calculate_exponential([value], 10.54266827, -1.580744853, decimal_places)
            #2.2
            #aa_results = calculate_exponential([value], 6.952349526, -0.991816132, decimal_places)
            #2.3
            #aa_results = calculate_exponential([value], 5.194806693, -0.66583337, decimal_places)
            #2.4
            #aa_results = calculate_exponential([value], 3.454045957, -0.291308744, decimal_places)
        #最后一行均为1.0版本的物性
        #    aa_results = calculate_exponential([value], 16.1248, -1.23814, decimal_places)
        elif value < 0.04:# poro of mudstone
            aa_results = calculate_exponential([value], 139.794, -2.83876, decimal_places)

        all_results.extend(aa_results)

    for value in numbers[aa:aa+bb]:
        if value >= 0.04:#porosity of sand
            #bb_results = calculate_exponential([value], 6.2469, -0.921506, decimal_places)
            #2.1
            bb_results = calculate_exponential([value], 3.020796124, -0.211224367, decimal_places)
            #2.2
            #bb_results = calculate_exponential([value], 2.021432853, 0.085353382, decimal_places)
            #2.3
            #bb_results = calculate_exponential([value], 1.357612302, 0.339309116, decimal_places)
            #2.4
            #bb_results = calculate_exponential([value], 1.04167329, 0.492927001, decimal_places)
        #    bb_results = calculate_exponential([value], 19.2891, -1.57562, decimal_places)
        elif value < 0.04:# poro of mudstone
            bb_results = calculate_exponential([value], 129.013, -3.0321, decimal_places)

        all_results.extend(bb_results)
        
    for value in numbers[aa+bb:aa+bb+cc]:
        if value >= 0.04:#porosity of sand
            #cc_results = calculate_exponential([value], 6.8419, -0.8902, decimal_places)
            #2.1
            cc_results = calculate_exponential([value], 3.399853955, -0.237504703, decimal_places)
            #2.2
            #cc_results = calculate_exponential([value], 2.173284689, 0.080984694, decimal_places)
            #2.3
            #cc_results = calculate_exponential([value], 1.738105313, 0.222043658, decimal_places)
            #2.4
            #cc_results = calculate_exponential([value], 1.316446936, 0.385353307, decimal_places)
        #    cc_results = calculate_exponential([value], 14.775, -1.08789, decimal_places)
        elif value < 0.04:# poro of mudstone
            cc_results = calculate_exponential([value], 47.5264, -1.49114, decimal_places)

        all_results.extend(cc_results)

    for value in numbers[aa+bb+cc:aa+bb+cc+dd]:
        if value >= 0.04:#porosity of sand
            #dd_results = calculate_exponential([value], 0.4620, 0.92413, decimal_places)
            #2.1
            dd_results = calculate_exponential([value], 0.531598742, 0.855840056, decimal_places)
            #2.2
            #dd_results = calculate_exponential([value], 0.620462899, 0.779284652, decimal_places)
            #2.3
            #dd_results = calculate_exponential([value], 0.755370913, 0.67953284, decimal_places)
            #2.4
            #dd_results = calculate_exponential([value], 1.085962485, 0.486812208, decimal_places)
        #    dd_results = calculate_exponential([value], 21.7981, -1.86189, decimal_places)
        elif value < 0.04:# poro of mudstone
            dd_results = calculate_exponential([value], 73.2243, -1.6963, decimal_places)

        all_results.extend(dd_results)

    for value in numbers[aa+bb+cc+dd:aa+bb+cc+dd+ee]:
        if value >= 0.04:#porosity of sand
            #ee_results = calculate_exponential([value], 0.3981, 0.9888, decimal_places)
            #2.1
            ee_results = calculate_exponential([value], 0.447742133, 0.931676372, decimal_places)
            #2.2
            #ee_results = calculate_exponential([value], 0.517041667, 0.860652384, decimal_places)
            #2.3
            #ee_results = calculate_exponential([value], 0.620462899, 0.768736783, decimal_places)
            #2.4
            #ee_results = calculate_exponential([value], 0.789713359, 0.64315615, decimal_places)
        #    ee_results = calculate_exponential([value], 19.8059, -1.71845, decimal_places)
        elif value < 0.04:# poro of mudstone
            ee_results = calculate_exponential([value], 62.5234, -1.5834, decimal_places)

## 3.0版本渗透率计算
#    for value in numbers[:aa]:
#        if value >= 0.04:#porosity of sand#
#            aa_results = calculate_exponential([value], 10.54266827, -1.580744853, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            aa_results = calculate_exponential([value], 139.794, -2.83876, decimal_places)
#
#        all_results.extend(aa_results)
#
#    for value in numbers[aa:aa+bb]:
#        if value >= 0.04:#porosity of sand
#            bb_results = calculate_exponential([value], 3.107395337, -0.234084925, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            bb_results = calculate_exponential([value], 129.013, -3.0321, decimal_places)
#
#        all_results.extend(bb_results)
#        
#    for value in numbers[aa+bb:aa+bb+cc]:
#        if value >= 0.04:#porosity of sand
#            cc_results = calculate_exponential([value], 3.399853955, -0.237504703, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            cc_results = calculate_exponential([value], 47.5264, -1.49114, decimal_places)
#
#        all_results.extend(cc_results)
#
#    for value in numbers[aa+bb+cc:aa+bb+cc+dd]:
#        if value >= 0.04:#porosity of sand
#            dd_results = calculate_exponential([value], 0.510958259, 0.875227293, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            dd_results = calculate_exponential([value], 73.2243, -1.6963, decimal_places)
#
#        all_results.extend(dd_results)
#
#    for value in numbers[aa+bb+cc+dd:aa+bb+cc+dd+ee]:
#        if value >= 0.04:#porosity of sand
#            ee_results = calculate_exponential([value], 0.443173017, 0.936693183, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            ee_results = calculate_exponential([value], 62.5234, -1.5834, decimal_places)

## 4.0版本渗透率计算
#    for value in numbers[:aa]:
#        if value >= 0.04:#porosity of sand#
#            aa_results = calculate_exponential([value], 5.194806693, -0.66583337, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            aa_results = calculate_exponential([value], 139.794, -2.83876, decimal_places)
#
#        all_results.extend(aa_results)
#
#    for value in numbers[aa:aa+bb]:
#        if value >= 0.04:#porosity of sand
#            bb_results = calculate_exponential([value], 1.551711687, 0.257572055, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            bb_results = calculate_exponential([value], 129.013, -3.0321, decimal_places)
#
#        all_results.extend(bb_results)
#        
#    for value in numbers[aa+bb:aa+bb+cc]:
#        if value >= 0.04:#porosity of sand
#            cc_results = calculate_exponential([value], 2.263999073, 0.054047472, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            cc_results = calculate_exponential([value], 47.5264, -1.49114, decimal_places)
#
#        all_results.extend(cc_results)
#
#    for value in numbers[aa+bb+cc:aa+bb+cc+dd]:
#        if value >= 0.04:#porosity of sand
#            dd_results = calculate_exponential([value], 0.668198078, 0.742032959, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            dd_results = calculate_exponential([value], 73.2243, -1.6963, decimal_places)
#
#        all_results.extend(dd_results)
#
#    for value in numbers[aa+bb+cc+dd:aa+bb+cc+dd+ee]:
#        if value >= 0.04:#porosity of sand
#            ee_results = calculate_exponential([value], 0.542896379, 0.8362798, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            ee_results = calculate_exponential([value], 62.5234, -1.5834, decimal_places)

## 5.0版本渗透率计算
#    for value in numbers[:aa]:
#        if value >= 0.04:#porosity of sand#
#            aa_results = calculate_exponential([value], 3.454045957, -0.291308744, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            aa_results = calculate_exponential([value], 139.794, -2.83876, decimal_places)
#
#        all_results.extend(aa_results)
#
#    for value in numbers[aa:aa+bb]:
#        if value >= 0.04:#porosity of sand
#            bb_results = calculate_exponential([value], 1.034229943, 0.496950103, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            bb_results = calculate_exponential([value], 129.013, -3.0321, decimal_places)
#
#        all_results.extend(bb_results)
#        
#    for value in numbers[aa+bb:aa+bb+cc]:
#        if value >= 0.04:#porosity of sand
#            cc_results = calculate_exponential([value], 1.241179186, 0.418531611, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            cc_results = calculate_exponential([value], 47.5264, -1.49114, decimal_places)
#
#        all_results.extend(cc_results)
#
#    for value in numbers[aa+bb+cc:aa+bb+cc+dd]:
#        if value >= 0.04:#porosity of sand
#            dd_results = calculate_exponential([value], 1.085962485, 0.486812208, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            dd_results = calculate_exponential([value], 73.2243, -1.6963, decimal_places)
#
#        all_results.extend(dd_results)
#
#    for value in numbers[aa+bb+cc+dd:aa+bb+cc+dd+ee]:
#        if value >= 0.04:#porosity of sand
#            ee_results = calculate_exponential([value], 0.789713359, 0.64315615, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            ee_results = calculate_exponential([value], 62.5234, -1.5834, decimal_places)

## 1.0版本渗透率计算
#    for value in numbers[:aa]:
#        if value >= 0.04:#porosity of sand#
#            aa_results = calculate_exponential([value], 16.1248, -1.23814, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            aa_results = calculate_exponential([value], 139.794, -2.83876, decimal_places)
#
#        all_results.extend(aa_results)
#
#    for value in numbers[aa:aa+bb]:
#        if value >= 0.04:#porosity of sand
#            bb_results = calculate_exponential([value], 19.2891, -1.57562, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            bb_results = calculate_exponential([value], 129.013, -3.0321, decimal_places)
#
#        all_results.extend(bb_results)
#        
#    for value in numbers[aa+bb:aa+bb+cc]:
#        if value >= 0.04:#porosity of sand
#            cc_results = calculate_exponential([value], 14.775, -1.08789, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            cc_results = calculate_exponential([value], 47.5264, -1.49114, decimal_places)
#
#        all_results.extend(cc_results)
#
#    for value in numbers[aa+bb+cc:aa+bb+cc+dd]:
#        if value >= 0.04:#porosity of sand
#            dd_results = calculate_exponential([value], 21.7981, -1.86189, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            dd_results = calculate_exponential([value], 73.2243, -1.6963, decimal_places)
#
#        all_results.extend(dd_results)
#
#    for value in numbers[aa+bb+cc+dd:aa+bb+cc+dd+ee]:
#        if value >= 0.04:#porosity of sand
#            ee_results = calculate_exponential([value], 19.8059, -1.71845, decimal_places)
#        elif value < 0.04:# poro of mudstone
#            ee_results = calculate_exponential([value], 62.5234, -1.5834, decimal_places)

        all_results.extend(ee_results)

    with open(output_filename, 'w') as outfile:
        for i in range(0, len(all_results), 5):
            outfile.write('		'.join(f"{result:.{decimal_places}f}" for result in all_results[i:i+5]) + '\n')

if __name__ == "__main__":
    input_file = final_poro_filename
    perm_output_file = os.path.splitext(Dmatlas_sandGrid_filename)[0] + "FinalPerm.txt"
    #shenhua grid num:hsg583200 ljg349920 sqf233280 shz116640 shx11664

    aa = 11664 #要计算的数量
    bb = 116640
    cc = 233280
    dd = 349920
    ee = 583200
    decimal_places = 7 #保留的小数位数

    process_and_output(input_file, perm_output_file, aa, bb, cc, dd, ee, decimal_places)
    print("处理完成，渗透率已输出到", perm_output_file, "文件中。")

# 读取文件内容
with open(blank_cmg_filename, 'r') as file1:
    content1 = file1.read()

with open(final_poro_filename, 'r') as file2:
    content2 = file2.read()

with open(perm_output_file, 'r') as file3:
    content3 = file3.read()

# 合并文件内容
combined_content = []
lines = content1.split('\n')
for line in lines:
    combined_content.append(line)
    if "*POR *ALL" in line:
        combined_content.append(content2)
    elif "*PERMI *ALL" in line:
        combined_content.append(content3)

# 将合并后的内容写入文件4
with open(final_cmg_filename, 'w') as file4:
    file4.write('\n'.join(combined_content))

print(f"文件 '{final_cmg_filename}' 已成功生成。")