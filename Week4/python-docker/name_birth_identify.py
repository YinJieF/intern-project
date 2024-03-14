from underthesea import ner

def named_entity_recognition(sentence):
    return ner(sentence) 

def find_elements(sentence):
    names, birthday_keywords, dates = [], [], []
    for i in range(len(sentence)):
        # find brithday keywords
        if 'Sinh' in sentence[i][0] or 'sinh' in sentence[i][0]:
            birthday_keywords.append((i, sentence[i][0]))

        # find names
        # name are Np (Proper Noun) and must more than one words
        elif sentence[i][1] == 'Np' and len(sentence[i][0].split(' ')) > 1:
            name = sentence[i][0]
            names.append((i, name))

        # find dates
        #case 1 : dd/mm/yyyy are separated by other words
        elif i < len(sentence) - 5 and sentence[i][1] == 'M' and sentence[i+2][1] == 'M' and sentence[i+4][1] == 'M':
            date = sentence[i][0] + "/" + sentence[i+2][0] + "/" + sentence[i+4][0]
            dates.append((i, date))
        #case 2 : 'dd/mm/yyyy' is a whole word, categorized as 'M' or 'N'
        elif (sentence[i][1] == 'M' or sentence[i][1] == 'N') and sentence[i][0].count('/') == 2:
            date = sentence[i][0]
            if ' ' in date:
                date = date.split(' ')
                date = date[0]
            dates.append((i, date))

    return names, birthday_keywords, dates

# find the group of data that are related
# every element in the list can only be use once
def combination(names_list, sinh_list, dates_list):
    result = []
    # Determine the minimun number of elements in the list
    min_len = min(len(dates_list), len(sinh_list), len(names_list))
    date_start, name_start = 0, 0
    for m in range(min_len):
        closest_name = None
        closest_date = None
        min_diff_name = float('inf')
        min_diff_date = float('inf')
        skip = False
        sinh = sinh_list[m]
        # determine if the sinh is usable
        for i in range(m+1, len(sinh_list)):
            #print(sinh_list[i][0], dates_list[date_start][0], sinh[0], dates_list[date_start][0])
            if abs(sinh_list[i][0] - dates_list[date_start][0]) < abs(sinh[0] - dates_list[date_start][0]):
                skip = True
                break
        if not skip:
            for j in range(date_start, len(dates_list)):
                date = dates_list[j]
                if abs(date[0] - sinh[0]) < min_diff_date:
                    min_diff_date = abs(date[0] - sinh[0])
                    closest_date = date
            
            for k in range(name_start, len(names_list)):
                name = names_list[k]
                if abs(name[0] - sinh[0]) < min_diff_name and name[0] != sinh[0]:
                    min_diff_name = abs(name[0] - sinh[0])
                    closest_name = name
            
            return [closest_name[1], closest_date[1]]
            date_start, name_start = dates_list.index(closest_date) + 1, names_list.index(closest_name) + 1
            
    return result

# sentence = "1/ Trần Văn T, sinh ngày 01 tháng 01 năm 1987 tại Quảng Nam; Nơi cư trú: thôn 04, xã TG, huyện Bắc Trà My, tỉnh Quảng Nam; nghề nghiệp: nông; trình độ văn hoá: 03/12; dân tộc: Cadong; giới tính: nam; tôn giáo: không; quốc tịch: Việt Nam; con ông Trần Văn Tiếu và bà Thanh Thị Liên; vợ tên Phạm Thị Hiếm và 02 con; tiền án, tiền sự: không; Bị cáo bị áp dụng biện pháp ngăn chặn: “Cấm đi khỏi nơi cư trú”, có mặt tại phiên tòa. 2/ Đinh Tấn M, sinh ngày 21 tháng 6 năm 1995 tại Quảng Nam; Nơi cư trú: thôn 04, xã TG, huyện Bắc Trà My, tỉnh Quảng Nam; nghề nghiệp: nông; trình độ"
# ner_sentence = named_entity_recognition(sentence)
# names, sinh, dates = find_elements(ner_sentence)
# result = combination(names, sinh, dates)
# print(result[0][0])

