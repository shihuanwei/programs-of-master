import math

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

    for value in numbers[:aa]:
        if value >= 0.04:#porosity of sand#
            #2.0版本，纵向物性差异
            #aa_results = calculate_exponential([value], 22.49845, -3.2759, decimal_places)
            #2.1
            #aa_results = calculate_exponential([value], 10.54266827, -1.580744853, decimal_places)
            #2.2
            #aa_results = calculate_exponential([value], 6.952349526, -0.991816132, decimal_places)
            #2.3
            #aa_results = calculate_exponential([value], 5.194806693, -0.66583337, decimal_places)
            #2.4
            aa_results = calculate_exponential([value], 3.454045957, -0.291308744, decimal_places)
        #最后一行均为1.0版本的物性
        #    aa_results = calculate_exponential([value], 16.1248, -1.23814, decimal_places)
        elif value < 0.04:# poro of mudstone
            aa_results = calculate_exponential([value], 139.794, -2.83876, decimal_places)

        all_results.extend(aa_results)

    for value in numbers[aa:aa+bb]:
        if value >= 0.04:#porosity of sand
            #bb_results = calculate_exponential([value], 6.2469, -0.921506, decimal_places)
            #2.1
            #bb_results = calculate_exponential([value], 3.020796124, -0.211224367, decimal_places)
            #2.2
            #bb_results = calculate_exponential([value], 2.021432853, 0.085353382, decimal_places)
            #2.3
            #bb_results = calculate_exponential([value], 1.357612302, 0.339309116, decimal_places)
            #2.4
            bb_results = calculate_exponential([value], 1.04167329, 0.492927001, decimal_places)
        #    bb_results = calculate_exponential([value], 19.2891, -1.57562, decimal_places)
        elif value < 0.04:# poro of mudstone
            bb_results = calculate_exponential([value], 129.013, -3.0321, decimal_places)

        all_results.extend(bb_results)
        
    for value in numbers[aa+bb:aa+bb+cc]:
        if value >= 0.04:#porosity of sand
            #cc_results = calculate_exponential([value], 6.8419, -0.8902, decimal_places)
            #2.1
            #cc_results = calculate_exponential([value], 3.399853955, -0.237504703, decimal_places)
            #2.2
            #cc_results = calculate_exponential([value], 2.173284689, 0.080984694, decimal_places)
            #2.3
            #cc_results = calculate_exponential([value], 1.738105313, 0.222043658, decimal_places)
            #2.4
            cc_results = calculate_exponential([value], 1.316446936, 0.385353307, decimal_places)
        #    cc_results = calculate_exponential([value], 14.775, -1.08789, decimal_places)
        elif value < 0.04:# poro of mudstone
            cc_results = calculate_exponential([value], 47.5264, -1.49114, decimal_places)

        all_results.extend(cc_results)

    for value in numbers[aa+bb+cc:aa+bb+cc+dd]:
        if value >= 0.04:#porosity of sand
            #dd_results = calculate_exponential([value], 0.4620, 0.92413, decimal_places)
            #2.1
            #dd_results = calculate_exponential([value], 0.531598742, 0.855840056, decimal_places)
            #2.2
            #dd_results = calculate_exponential([value], 0.620462899, 0.779284652, decimal_places)
            #2.3
            #dd_results = calculate_exponential([value], 0.755370913, 0.67953284, decimal_places)
            #2.4
            dd_results = calculate_exponential([value], 1.085962485, 0.486812208, decimal_places)
        #    dd_results = calculate_exponential([value], 21.7981, -1.86189, decimal_places)
        elif value < 0.04:# poro of mudstone
            dd_results = calculate_exponential([value], 73.2243, -1.6963, decimal_places)

        all_results.extend(dd_results)

    for value in numbers[aa+bb+cc+dd:aa+bb+cc+dd+ee]:
        if value >= 0.04:#porosity of sand
            #ee_results = calculate_exponential([value], 0.3981, 0.9888, decimal_places)
            #2.1
            #ee_results = calculate_exponential([value], 0.447742133, 0.931676372, decimal_places)
            #2.2
            #ee_results = calculate_exponential([value], 0.517041667, 0.860652384, decimal_places)
            #2.3
            #ee_results = calculate_exponential([value], 0.620462899, 0.768736783, decimal_places)
            #2.4
            ee_results = calculate_exponential([value], 0.789713359, 0.64315615, decimal_places)
        #    ee_results = calculate_exponential([value], 19.8059, -1.71845, decimal_places)
        elif value < 0.04:# poro of mudstone
            ee_results = calculate_exponential([value], 62.5234, -1.5834, decimal_places)

        all_results.extend(ee_results)

    with open(output_filename, 'w') as outfile:
        for i in range(0, len(all_results), 5):
            outfile.write('\t'.join(f"{result:.{decimal_places}f}" for result in all_results[i:i+5]) + '\n')

if __name__ == "__main__":
    input_file = "normPoroMod-SN60%.txt"
    output_file = "normPermMod-SN60%-z2.4.txt"
    #shenhua total grid num:hsg583200 ljg349920 sqf233280 shz116640 shx11664

    aa = 11664 #要计算的数量
    bb = 116640
    cc = 233280
    dd = 349920
    ee = 583200

    decimal_places = 7 #保留的小数位数

    process_and_output(input_file, output_file, aa, bb, cc, dd, ee, decimal_places)
    print("处理完成，结果已输出到", output_file, "文件中。")
