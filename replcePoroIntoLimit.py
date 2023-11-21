import random

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
    input_file_name = "normPoro2"  # 替换前的输入文件名
    output_file_name = "normPoroModified2.txt"  # 替换后的输出文件名

    replace_text(input_file_name, output_file_name)
    print("文本替换完成！已输出到文件",output_file_name,"中。")
