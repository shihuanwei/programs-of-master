import random
import os

# 生成随机高斯分布的数字
def generate_gaussian_numbers(count, mean, std_dev):
    return [round(random.gauss(mean, std_dev), 7) for _ in range(count)]

# 混合砂体和泥岩的孔隙度列表，并返回混合后的新列表
def mix_lists(list1, list2):
    mixed_list = list1 + list2
    random.shuffle(mixed_list)  # 随机打乱顺序
    return mixed_list

# 主处理函数
def process_and_output(output_filename, 
                       a1_count, a1_mean, a1_std_dev,
                       a2_count, a2_mean, a2_std_dev,
                       b1_count, b1_mean, b1_std_dev,
                       b2_count, b2_mean, b2_std_dev,
                       c1_count, c1_mean, c1_std_dev,
                       c2_count, c2_mean, c2_std_dev,
                       d1_count, d1_mean, d1_std_dev,
                       d2_count, d2_mean, d2_std_dev,
                       e1_count, e1_mean, e1_std_dev,
                       e2_count, e2_mean, e2_std_dev):
    #cal sand poro gaussian
    a1_data = generate_gaussian_numbers(a1_count, a1_mean, a1_std_dev)
    b1_data = generate_gaussian_numbers(b1_count, b1_mean, b1_std_dev)
    c1_data = generate_gaussian_numbers(c1_count, c1_mean, c1_std_dev)
    d1_data = generate_gaussian_numbers(d1_count, d1_mean, d1_std_dev)
    e1_data = generate_gaussian_numbers(e1_count, e1_mean, e1_std_dev)
    #cal mudston poro gaussian
    a2_data = generate_gaussian_numbers(a2_count, a2_mean, a2_std_dev)
    b2_data = generate_gaussian_numbers(b2_count, b2_mean, b2_std_dev)
    c2_data = generate_gaussian_numbers(c2_count, c2_mean, c2_std_dev)
    d2_data = generate_gaussian_numbers(d2_count, d2_mean, d2_std_dev)
    e2_data = generate_gaussian_numbers(e2_count, e2_mean, e2_std_dev)

    # 混合数据
    a_data = mix_lists(a1_data, a2_data)
    b_data = mix_lists(b1_data, b2_data)
    c_data = mix_lists(c1_data, c2_data)
    d_data = mix_lists(d1_data, d2_data)
    e_data = mix_lists(e1_data, e2_data)

    # 储存数据
    all_data = []
    all_data.extend(a_data)
    all_data.extend(b_data)
    all_data.extend(c_data)
    all_data.extend(d_data)
    all_data.extend(e_data)

    #每行五个输出
    with open(output_filename, 'w') as outfile:
        for i in range(0, len(all_data), 5):
            outfile.write('\t'.join(map(str, all_data[i:i+5])) + '\n')

if __name__ == "__main__":
    
    ## 2.0-参照谢健论文的纵向物性差异版本
    a1_count = 3499#sandNum60%(最原始版本z2.0),先读取shanxi的砂体网格数，11664*0.3
   #a1_count = 1283#sandNum20%,先读取shanxi的砂体网格数
   #a1_count = 2566#sandNum40%,先读取shanxi的砂体网格数
   #a1_count = 4432#sandNum80%,先读取shanxi的砂体网格数
    a1_mean = 0.113
    a1_std_dev = 0.003333
    
    b1_count = 58320#sandNum60%
   #b1_count = 19829#sandNum20%
   #b1_count = 37325#sandNum40%
   #b1_count = 69984#sandNum80%
    b1_mean = 0.122
    b1_std_dev = 0.003333
 
    c1_count = 123638#sandNum60%
   #c1_count = 41990#sandNum20%
   #c1_count = 79315#sandNum40%
   #c1_count = 151632#sandNum80%
    c1_mean = 0.101
    c1_std_dev = 0.003333

    d1_count = 174960#sandNum60%
   #d1_count = 45490#sandNum20%
   #d1_count = 104976#sandNum40%
   #d1_count = 209952#sandNum80%
    d1_mean = 0.106
    d1_std_dev = 0.003333

    e1_count = 349920#sandNum60%
   #e1_count = 99144#sandNum20%
   #e1_count = 233280#sandNum40%
   #e1_count = 449064#sandNum80%
    e1_mean = 0.123
    e1_std_dev = 0.003333
    ## 初始1.0版孔隙度渗透率
  # a1_count = 3499#先读取shanxi的砂体网格数，11664*0.3
  # a1_mean = 0.089
  # a1_std_dev = 0.012

  # b1_count = 58320
  # b1_mean = 0.093
  # b1_std_dev = 0.009666667

  # c1_count = 123638
  # c1_mean = 0.0865
  # c1_std_dev = 0.014166667

  # d1_count = 174960
  # d1_mean = 0.089
  # d1_std_dev = 0.005666667

  # e1_count = 349920
  # e1_mean = 0.0975
  # e1_std_dev = 0.0085

    ## 泥岩物性不变
    a2_count = 8165 #sandNum60%先读取shanxi的泥岩网格数
   #a2_count = 10381#sandNum20%先读取shanxi的泥岩网格数
   #a2_count = 9098 #sandNum40%先读取shanxi的泥岩网格数
   #a2_count = 7232 #sandNum80%先读取shanxi的泥岩网格数
    a2_mean = 0.0085
    a2_std_dev = 0.000833333

    b2_count = 58320 #sandNum60%
   #b2_count = 96811#sandNum20%
   #b2_count = 79315 #sandNum40%
   #b2_count = 46656 #sandNum80%
    b2_mean = 0.0115
    b2_std_dev = 0.001166667

    c2_count = 109642 #sandNum60%
   #c2_count = 191290#sandNum20%
   #c2_count = 153965 #sandNum40%
   #c2_count = 81648 #sandNum80%
    c2_mean = 0.008
    c2_std_dev = 0.001333333

    d2_count = 174960 #sandNum60%
   #d2_count = 304430#sandNum20%
   #d2_count = 244944 #sandNum40%
   #d2_count = 139968 #sandNum80%
    d2_mean = 0.008
    d2_std_dev = 0.001

    e2_count = 233280 #sandNum60%
   #e2_count = 484056#sandNum20%
   #e2_count = 349920 #sandNum40%
   #e2_count = 134136 #sandNum80%
    e2_mean = 0.0105
    e2_std_dev = 0.001833333

    output_file = "normPoro"

    process_and_output(output_file, 
                       a1_count, a1_mean, a1_std_dev,
                       a2_count, a2_mean, a2_std_dev,
                       b1_count, b1_mean, b1_std_dev,
                       b2_count, b2_mean, b2_std_dev,
                       c1_count, c1_mean, c1_std_dev,
                       c2_count, c2_mean, c2_std_dev,
                       d1_count, d1_mean, d1_std_dev,
                       d2_count, d2_mean, d2_std_dev,
                       e1_count, e1_mean, e1_std_dev,
                       e2_count, e2_mean, e2_std_dev)
    print("处理完成，结果已输出到", output_file, "文件中。")

#替换溢出值
def replace_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            replaced_line = line.strip().split()
            output_line = []
            for word in replaced_line:
                try:
                    num = float(word)
                    if num < 0.004:
                        new_num = round(random.uniform(0.004, 0.01), 7)
                    elif 0.03 <= num < 0.044:
                        new_num = round(random.uniform(0.074,0.1), 7) 
                    elif 0.016 <= num < 0.03:
                        new_num = round(random.uniform(0.007,0.009), 7) 
                    elif num > 0.129:
                        new_num = round(random.uniform(0.1, 0.12), 7)
                    else:
                        new_num = num
                    output_line.append(str(new_num))
                    if len(output_line) == 5:
                        outfile.write('\t'.join(output_line) + '\n')
                        output_line = []
                except ValueError:
                    output_line.append(word)
            if output_line:
                outfile.write('\t'.join(output_line) + '\n')

if __name__ == "__main__":
    input_file_name = output_file  # 替换前的输入文件名
    final_output_file_name = os.path.splitext(output_file)[0] + "Mod-SN60%.txt"  # 替换后的输出文件名

    replace_text(input_file_name, final_output_file_name)
    print("文本替换完成！已输出到文件",final_output_file_name,"中。")