import streamlit as st
import pandas as pd

def process_and_display_data(df):
    """
    데이터프레임을 가공하고 Streamlit에 표시하는 함수.
    - '지역' 열의 '계'를 '전국'으로 변경
    - 취업률 및 실업률 계산
    """
    try:
        st.info("데이터 처리 중...")
        st.write("파일에서 읽어온 열 목록:", df.columns.tolist())
        # 1. '지역' 열의 '계'를 '전국'으로 변경
        if '지역' in df.columns:
            df['지역'] = df['지역'].replace('계', '전국')
        else:
            st.warning("'지역' 열을 찾을 수 없어 값을 변경하지 못했습니다.")

        # 2. 취업률 및 실업률 계산
        required_cols = ['취업자', '실업자', '경제활동인구']
        if all(col in df.columns for col in required_cols):
            # 0으로 나누는 경우를 방지하고, 결과가 NaN이면 0으로 채움
            df['취업률'] = (df['취업자'] / df['경제활동인구'] * 100).fillna(0)
            df['실업률'] = (df['실업자'] / df['경제활동인구'] * 100).fillna(0)
            st.success("취업률 및 실업률 계산 완료!")
        else:
            st.warning(f"계산에 필요한 열({', '.join(required_cols)})이 없어 취업률/실업률을 계산하지 못했습니다.")

        st.dataframe(df)

    except Exception as e:
        st.error(f"데이터 처리 중 오류가 발생했습니다: {e}")


# --- Streamlit 앱 시작 ---

st.set_page_config(layout="wide")
st.title('경제활동 데이터 분석')

try:
    # UTF-8으로 파일 읽기 시도
    df = pd.read_csv('경제활동_통합.csv', encoding='utf-8')
    st.success('파일을 성공적으로 읽었습니다 (UTF-8 인코딩).')
    process_and_display_data(df)

except FileNotFoundError:
    st.error("오류: '경제활동_통합.csv' 파일을 현재 디렉토리에서 찾을 수 없습니다.")

except Exception as e:
    st.warning(f"UTF-8 인코딩으로 파일을 읽는 데 실패했습니다. ({e})")
    st.info("cp949 인코딩으로 다시 시도합니다...")
    try:
        # UTF-8 실패 시 cp949로 파일 읽기 시도
        df = pd.read_csv('경제활동_통합.csv', encoding='cp949')
        st.success('파일을 성공적으로 읽었습니다 (cp949 인코딩).')
        process_and_display_data(df)

    except Exception as e2:
        st.error(f"cp949 인코딩으로도 파일을 읽는 데 실패했습니다. ({e2})")
        st.error("파일의 인코딩을 확인하거나, 파일이 올바른 CSV 형식이 맞는지 확인해주세요.")