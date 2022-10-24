from operator import itemgetter

import wordcloud
import pandas as pd

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

import csv
from collections import Counter

# 오픈 횟수의 분석
def countExtract(csv_count, custom_Index):

    # csv파일 list로 변환
    my_list = list(csv_count)

    # nan 결측치 제거
    # 결측치를 제거하면 이후에 for문에서 의미없는 값에 대한 메모리 사용을 줄일 수 있다.
    clean_List = [x for x in my_list if str(x) != 'nan']

    num = len(custom_Index) - 1
    f = open("1번파일.csv", 'w', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    writer.writerow(['오픈 횟수', '명'])
    for i in range(len(custom_Index), 0, -1):
        result = list(filter( lambda x : x >= custom_Index[num], clean_List))
        writer.writerow([custom_Index[num], len(result)])
        num = num - 1

    writer.writerow(['유니크오픈 횟수', sum(clean_List)])
    writer.writerow(['광고효과', sum(clean_List)*150])

    f.close()

# 이메일에 해당하는 오픈 개수를 누적시키는 함수
# 설명 : email 리스트에서 같은 이메일을 찾아서 해당 이메일의 오픈횟수를 누적시킨다.
def findindex(email_list, cnt_list, index):
    result_list = list(filter(lambda x : email_list[x] == index, range(len(email_list))))
    sum = 0
    # result_list 는 같은 이메일을 가진 원소에 인덱스를 리스트 형태로 가지고 있다.
    # 인덱스에 매칭되는 오픈 수 리스트(cnt_list) 개수를 누적시킨다.
    for i in result_list:
        sum = sum + cnt_list[i]
    return sum


# 회사별 이메일 추출 함수
def OpenRate(csv_email, csv_count):

    # csv파일 list로 변환
    email_list = list(csv_email)
    count_list = list(csv_count)

    # csv파일에서 이메일주소만 추출
    # 목표 : @부터 . 사이에 문자열을 추출해서 오픈 수를 카운팅하는 함
    # 함수 설명
    # 이메일 주소에서 @에 인덱스 추출 후 리스트에 넣는다. 1번 인덱스에 @이후 문자열이 담긴다.
    # 이메일 주소에서 .(첫번째 위치를 찾아)냄 인덱스 추출
    # 회사 도메인이 naver, gmail 등등 인지 체크 후 csv 파일에 저장

    f = open("index.csv", 'w', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    writer.writerow(['이메일', '오픈수'])
    num = 0
    clean_list = []
    for i in email_list:
        gol = i.split(sep='@')
        str = gol[1]
        index = str.find('.')
        if str[:index] == 'naver' or str[:index] == 'gmail' or str[:index] == 'outlook' \
                or str[:index] == 'hanmail' or str[:index] == 'hotmail' or str[:index] == 'daum' \
                or str[:index] == 'nate' or str[:index] == 'icloud' or str[:index] == 'm':
            pass
        else:
            writer.writerow([str[:index], count_list[num]])
        num = num + 1
    f.close()

    # 이메일과 오픈수를 리스트로 만든다.
    csv_open = pd.read_csv('index.csv', encoding='utf-8')
    calc_email = csv_open.loc[:, '이메일']
    calc_cnt = csv_open.loc[:, '오픈수']

    # check 리스트를 활용해서 이미 계산한 이메일은 함수는(findindex)를 실행하지 않는다.
    check = []
    # email 딕셔너리에 오픈된 횟수를 키-값(email-count)으로 넣는다.
    emaildic = {}

    for i in calc_email:
        if i not in check:
            val = findindex(calc_email, calc_cnt, i)
            emaildic[i] = val
            check.append(i)
        else:
            pass

    # email 딕셔너리를 items로 튜플화 시켜서 내림차순으로 정렬시킨다.
    Sortedmail = sorted(emaildic.items(), key=itemgetter(1), reverse=True)

    # 정렬된 직무 csv 파일 생성
    f = open("2번파일.csv", 'w', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    writer.writerow(['이메일', '총 오픈수'])
    num = 0
    for i in range(0, len(emaildic)):
        writer.writerow([Sortedmail[num][0], Sortedmail[num][1]])
        num = num + 1
    f.close()


# 엑셀 파일 추출
csv_file = pd.read_csv('여기에 파일명을 붙여넣어 주세요.csv', encoding='utf-8')

# csv 파일에서 특정 열 추출
csv_count = csv_file.loc[:, '오픈(중복 포함)']
csv_email = csv_file.loc[:, '이메일 주소']

countIndex = [3, 4, 5, 10, 20, 30, 50, 80, 100]

# 오픈횟수 함수 호출
countExtract(csv_count, countIndex)

# 회사별 이메일 추출 함수
OpenRate(csv_email, csv_count)





