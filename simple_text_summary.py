#--*-- coding : utf-8 --*--
f = open("C:\\tmp\\target.txt", "r", encoding="utf-8")
line_list = []
for line in f.readlines():
    line = line.strip()
    if line:
        line_list.append(line)
f.close()

total_text = "".join(line_list)
nline_list = total_text.split(".")
nline_list = [line.strip() for line in nline_list if "다" in line.strip()]

para_no = 0
para_dict = {}
for line in nline_list:
    if "Q" == line[0]:
        para_no += 1
        para_dict[para_no] = [line.replace("Q", "") + "."]
    else:
        para_dict[para_no].append(line + ".")

f = open("C:\\tmp\\result.txt", "w+", encoding="utf-8")
summary = ""
for para_no in para_dict:
    summary += para_dict[para_no][0] + para_dict[para_no][-1]
summary = summary.replace("\n", "")
f.write(summary)
f.close()