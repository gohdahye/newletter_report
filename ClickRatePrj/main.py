from operator import itemgetter

import pandas as pd
import csv

global result_s

result_s = 0

# extract 함수 호출되면 filename으로 된 txt파일 생성
def extract(csv_list, custom_Index, filename):
    global result_s
    # csv파일 list로 변환
    my_list = list(csv_list)

    # nan 결측치 제거
    # 결측치를 제거하면 이후에 for문에서 의미없는 값에 대한 메모리 사용을 줄일 수 있다.
    clean_List = [x for x in my_list if str(x) != 'nan']

    # 연령 리스트(clean_List)에서 custom_Index 항목에 몇 개씩 있는지 개수를 세서 csv 파일에 저장
    # 변수 설명
    # lines : 현재 엑셀 "직무" 열 내용이 리스트 형태로 저장됨
    # num : for문 인덱스를 가르키기 위한 변수

    # for문 설명
    # for 문을 0~7(ageIndex 총 개수)까지 반복시킨다.
    # python 특성 상 리스트(배열)을 인덱스(i)로 바로 가리킬 수 없어서 변수를 선언해서 인덱스를 가르켜야 함

    if custom_Index == jobIndex:
        # 직무당 개수 카운트해서 csv 파일로 저장
        num = 0
        f = open("count_job.csv", 'w', encoding='utf-8-sig', newline='')
        writer = csv.writer(f)
        for i in range(0, len(custom_Index)):
            result = clean_List.count(custom_Index[num])
            writer.writerow([custom_Index[num], result])
            num = num + 1
            result_s += result
        f.close()
        # 직무 개수 내림차순 정렬
        # 딕셔너리를 items()를 사용해서 튜플로 변환 시킨다.
        # (ex: dict{ ("임원":10), ("경영":10), ("인터넷":10) } )

        # pandas의 read_csv 사용
        # 이유: 기본 csv라이브러리는 숫자를 string으로 가져옴
        jobDict = pd.read_csv("count_job.csv", header=None, index_col=0, squeeze=True).to_dict()
        SortedJob = sorted(jobDict.items(), key=itemgetter(1), reverse=True)
        # 정렬된 직무 csv 파일 생성
        num = 0
        f = open(filename + ".csv", 'w', encoding='utf-8-sig', newline='')
        writer = csv.writer(f)
        writer.writerow([filename, '개수'])
        for i in range(0, len(custom_Index)):
            writer.writerow([SortedJob[num][0], SortedJob[num][1]])
            num = num + 1
        f.close()
    else:
        num = 0
        f = open(filename + ".csv", 'w', encoding='utf-8-sig', newline='')
        writer = csv.writer(f)
        writer.writerow([filename, '개수'])
        for i in range(0, len(custom_Index)):
            result = clean_List.count(custom_Index[num])
            writer.writerow([custom_Index[num], result])
            num = num + 1
            result_s += result
        f.close()

# 엑셀 파일 추출
file = pd.read_csv('(광고) _손에 파우더를 쥐어라_ (대실직 시대 생존법)_링크별 클릭 상세목록.csv_20221128.csv',
                   header=1, encoding='utf-8')

jobIndex = ["경영·사무", "홍보·마케팅·광고", "IT·인터넷", "연구개발(R&D)·설계", "기타", "학생·취업준비", "전문 특수직", "CEO·임원", "디자인",
            "영업·고객상담", "투자·금융", "품질·제조·생산", "공무·행정·교육", "무역·유통", "의료·제약", "건설·부동산", "서비스", "미디어",
            "자영업", "비공개"]

sexIndex = ["남성", "여성"]

ageIndex = ["10대 이하", "20대", "30대", "40대", "50대", "60대", "70대 이상"]


# csv 파일에서 특정 열 추출
csv_age = file.loc[:, '연령']
csv_job = file.loc[:, '직무']
csv_sex = file.loc[:, '성별']


# extract 함수 호출
extract(csv_job, jobIndex, "직무")
extract(csv_age, ageIndex, "연령")
extract(csv_sex, sexIndex, "성별")

print("전체 클릭 인원수 : " , result_s)

# job리스트 목록 백업용 추출
"""
f = open("joblist.txt", 'w')
for i in range(0, len(jobIndex)):
    f.write(jobIndex[i] + "\n")
f.close()
"""