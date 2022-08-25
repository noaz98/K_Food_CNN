import re
from collections import Counter
from PIL import Image
import numpy as np
import  matplotlib.pyplot as plt
from wordcloud import WordCloud
from konlpy.tag import *
def get_clean_text(df):  # 불용어 제거
    text = []

    for i in range(0, len(df)):
        if (str(df['main_text'][i]) == 'nan'):  # 지우고 싶은 글자가 있는 컬럼
            temp = ''
        else:
            temp = df['main_text'][i]
            temp = re.sub(
                '[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…《\》]', '', temp)  # 특수문자
            temp = re.sub('([ㄱ-ㅎㅏ-ㅣ]+)', '', temp)  # 한글 자음, 한글 모음
            temp = re.sub('([♡❤✌❣♥ᆢ✊❤️✨⤵️☺️;”“]+)', '', temp)  # 이모티콘
            only_BMP_pattern = re.compile("["
                                          u"\U00010000-\U0010FFFF"  # BMP characters 이외
                                          "]+", flags=re.UNICODE)
            temp = only_BMP_pattern.sub(r'', temp)  # BMP characters만
            emoji_pattern = re.compile("["
                                       u"\U0001F600-\U0001F64F"  # emoticons
                                       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                       u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                       "]+", flags=re.UNICODE)
            temp = emoji_pattern.sub(r'', temp)  # 유니코드로 이모티콘 지우기
            text.append(temp)

    return text


def convert_date(date): # 년/월/일로 변환
    if date == None:
        return np.Nan
    date = date.replace(",", "일")
    a_1 = date[:date.index("일")+1]
    a_2 = date[date.index("일")+2:]+"년"
    a_2 = a_2 + " " + a_1

    return a_2


def count_string(string): # 공백 제거
    new_string = re.sub(r'[0-9]+', '', str(string))
    count_space = re.sub('\n', '', str(new_string))

    return len(count_space)


def word_cloud(data_frame, cloud_shape_path, font_path):  # 워드 크라우드 생성
    df = data_frame
    okt = Okt()
    df_list = df["main_text"].to_list()

    ban_list = ["인스타", "그램", "맞팔", "스타", "날씨",
                "오늘", "지금"]  # 그램 , 인스타 등의 문자열을 의미없다고 판단
    df_word = []
    for i in df_list:
        word = okt.pos(i)
        df_word.extend(word)
    noun_adj_list = []

    # tag가 명사이거나 형용사인 단어들만 noun_adj_list에 넣어준다.
    for word, tag in df_word:
        if tag in ["Noun"] and word not in ban_list:
            noun_adj_list.append(word)

    counts = Counter(noun_adj_list)
    tags = counts.most_common(50)

    mask = Image.open(cloud_shape_path)
    mask = np.array(mask)

    wc = WordCloud(font_path=font_path, background_color="white",
                   prefer_horizontal=True, mask=mask, colormap="cool", contour_width=3, max_font_size=400)

    cloud = wc.generate_from_frequencies(dict(tags))
    plt.figure(figsize=(10, 10))
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()
