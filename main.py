import streamlit as st #스트림릿 페이지


#import 대상 ->파일(.py)
#from 파일 import 함수, 클래스 -> 해당 파일의 일부 함수/클래스만 임포트
#import crawling as cr
from crawling import crawling_saramin, crawling_work24
#레이아웃(웹 페이지의 생김새)
#스트림릿 웹페이지의 '헤더'역할
st.set_page_config(page_title = '채용공고 자동 크롤링 서비스',
                    layout = 'wide')
st.title('채용 공고 조회 서비스')
st.write('''이 서비스는 사람인과 고용24 페이지에 검색어를 입력하여 자동으로 공고를
          크롤링하도록 만든 서비스 입니다. 크롤링 된 내용은 하단의 표에서
          확인 가능하며 csv파일로 다운로드 받아 엑셀로 열어보실 수 있습니다.''')

#공고를 조회할 사이트를 선택
site_select = st.radio('크롤링할 사이트 선택', ['사람인', '고용24'], horizontal = True)

# with st.sidebar:
#     st.write('사이드 확장')

with st.expander('상세 검색 조건', expanded = True):
    col1, col2 = st.columns(2)

    with col1:
        search_text = st.text_input('검색어를 입력', placeholder = '예 : 파이썬, 인공지능')

        except_text = st.text_input('제외할 검색어', placeholder = '예 : 야간 근무, 출장')

        max_pages = st.number_input('크롤링 페이지 수', min_value = 1, max_value = 30)

    with col2:
        if site_select == '사람인':
            #사람인 사이트에서 '지역'을 의미하는 코드만 분리한 것. 사람인에서만 사용가능
            loc_options = {
                "전체": None,
                "서울": "101000",
                "경기": "102000",
                "인천": "108000",
                "부산": "106000",
                "대구": "104000",
                "광주": "103000",
                "대전": "105000"
            }
            #딕셔너리인 loc_options의 '키'만 모아서 리스트로 변환
            selected_location = st.multiselect('지역을 선택하세요.', list(loc_options.keys()), default = ['서울'])

            #st.write(selected_location)
            #크롤링 진행할 때 사용하기 위해서 문자열을 추출
            #elected_location으로 '서울', '경기', '부산' 같은 '지역 명' 추출
            #loc_options(딕셔너리)이므로, loc_options['부산'] => 값
            #x는 '서울', '경기', '부산' 같은 '지역 명'
            #if조건이 붙는 이유 : '지역명'이 없는 '지역'이라면 추가 안됨. 예외처리 한 것.
            #크롤링과 연결하기 위해 이렇게 하는듯?
            locations = [loc_options[x] for x in selected_location if loc_options[x]]

            #직무 검색
            cat_options = {
                "전체": None,
                "IT개발·데이터": "2",
                "경영·사무": "3",
                "마케팅·홍보": "4",
                "디자인": "9",
                "영업": "5"
            }

            selected_category = st.multiselect('직무를 선택하세요', list(cat_options.keys()), default = ['IT개발·데이터'])
            
            category = [cat_options[x] for x in selected_category if cat_options[x]]

            #경력
            career_option = {'전체' : '0', '신입' : '1', '경력' : '2', '신입/경력' : '3'}
            selected_career = st.selectbox('경력을 선택하세요', list(career_option.keys()))
            career = career_option[selected_career]
            
            #학력
            edu_option = {'전체' : '0', '고졸' : '1', '대졸(2,3년)' : '2', '대졸(4년)' : '3', '석사' : '4', '박사' : '5'}
            selected_edu = st.selectbox('학력을 선택하세요', list(edu_option.keys()))
            edu = edu_option[selected_edu]
        else :
            #지역, 직무, 경력, 학력
            region = st.text_input('지역 코드를 입력하세요', value = '11000',
                                    help = '지역 코드 알 수 없는 관계로 서울로 제한')
            occupation = st.text_input('직종 코드를 입력하세요', value = '024',
                                        help = '직종 코드 제한')
            career_options = {"전체": "A", "신입": "N", "경력": "E",
                               "관계없음": "Z"}
            edu_options = {"전체": "noEdu", "중졸이하": "01,02", "고졸": "03",
                            "대졸(2~3년)": "04", "대졸(4년)": "05", "석사": "06",
                              "박사": "07", "학력무관": "00"}

            career = st.selectbox('경력을 선택하세요', list(career_options.keys()))
            career = career_options[career]
            edu = st.selectbox('학력을 선택하세요', list(edu_options.keys()))
            edu = edu_options[edu]

#st.button(버튼에 들어갈 글자, ) '크기조절 옵션'
crawling_clicked = st.button('크롤링 시작',
                             use_container_width = True,
                             type = 'primary')

#crawling_clicked -> True(버튼을 눌렀음) / False(버튼을 누르지 않았음)
# if crawling_clicked:
#     st.write('버튼을 누름')
# else:
#     st.write('버튼을 안누름')

#크롤링 시행
#1. 크롤링한 결과를 어떻게 받아올 것인가?

#2. 크롤링 하는동안 어떻게 안내할 것인가?
if crawling_clicked:
    #2-1. 검색어나 필수요소가 누락된 경우 안내
    #검색어(search_text)가 없다(not)
    if not search_text:
        st.warning('검색어를 입력해주세요')
#2-2. 크롤링 시행하는 동안 '기다려주세요'라는 내용 표시
    else:
        with st.spinner(f'{site_select}에서 {search_text} 검색 결과 가져오는 중....'):
            #st.write(f'{site_select}에서{search_text} 검색 결과 가져오는 중...')
            if site_select == '사람인':
                #사람인 사이트의 내용을 크롤링하는 함수
                df = crawling_saramin()

            else : 
                #고용24 사이트의 내용을 크롤링 하는 함수
                df = crawling_work24()
    
    st.session_state['df'] = df
#st.session_state가 뭘까?
#이 코드가 있어야 df이 보임
#화면을 랜더링 할 때에도 'df'의 정보를 기억하도록 만들어주는 코드
#session_state는 '딕셔너리' 처럼 저장
#session_state['df']와 동일
#df['expection'] == df.espection
df = st.session_state['df']