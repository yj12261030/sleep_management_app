import streamlit as st
import pandas as pd
import os
import csv

st.title("수면 코드 진단 및 맞춤형 수면 개선 프로그램")

def sleep_duration(bed_h, bed_m, wake_h, wake_m):
    bed = bed_h * 60 + bed_m
    wake = wake_h * 60 + wake_m

    if wake <= bed:
        wake += 24 * 60

    return (wake - bed) / 60


def mid_sleep(bed_h, bed_m, wake_h, wake_m):
    bed = bed_h * 60 + bed_m
    wake = wake_h * 60 + wake_m

    if wake <= bed:
        wake += 24 * 60

    return (bed + wake) / 2


st.header("1. 크로노타입")

focus_time = st.radio(
    "하루 중 언제 가장 정신이 맑고 집중이 잘 됩니까?",
    [1, 2, 3, 4],
    format_func=lambda x: ["오전", "오후", "저녁", "밤 또는 새벽"][x - 1],
)

preferred_bedtime = st.radio(
    "내일 아무 일정이 없다면 언제 잠들고 싶습니까?",
    [1, 2, 3, 4],
    format_func=lambda x: ["밤 10시 이전", "밤 10시~자정", "자정~새벽 2시", "새벽 2시 이후"][x - 1],
)


st.header("2. 수면 시간")

col1, col2 = st.columns(2)

with col1:
    st.subheader("평일")
    weekday_bed_h = st.number_input("평일 취침 시", 0, 23, 0)
    weekday_bed_m = st.number_input("평일 취침 분", 0, 59, 0)
    weekday_wake_h = st.number_input("평일 기상 시", 0, 23, 7)
    weekday_wake_m = st.number_input("평일 기상 분", 0, 59, 0)

with col2:
    st.subheader("주말")
    weekend_bed_h = st.number_input("주말 취침 시", 0, 23, 1)
    weekend_bed_m = st.number_input("주말 취침 분", 0, 59, 0)
    weekend_wake_h = st.number_input("주말 기상 시", 0, 23, 9)
    weekend_wake_m = st.number_input("주말 기상 분", 0, 59, 0)


st.header("3. 피로도 및 학습 효율성")

sleepy_class = st.radio(
    "1~4교시 중 졸음을 참기 어렵습니까?",
    [1, 2, 3, 4],
    format_func=lambda x: ["매우 그렇다", "대체로 그렇다", "대체로 그렇지 않다", "전혀 그렇지 않다"][x - 1],
)

low_concentration = st.radio(
    "피곤해서 수업 내용이나 지문이 잘 들어오지 않습니까?",
    [1, 2, 3, 4],
    format_func=lambda x: ["자주", "가끔", "거의 없음", "전혀 없음"][x - 1],
)

failed_selfstudy = st.radio(
    "피로 때문에 계획한 자습 분량을 못 채웁니까?",
    [1, 2, 3, 4],
    format_func=lambda x: ["매우 그렇다", "대체로 그렇다", "대체로 그렇지 않다", "전혀 그렇지 않다"][x - 1],
)

negative_academic = st.radio(
    "수면 습관이 학업 성취에 부정적 영향을 준다고 생각합니까?",
    [1, 2, 3, 4],
    format_func=lambda x: ["매우 그렇다", "대체로 그렇다", "대체로 그렇지 않다", "전혀 그렇지 않다"][x - 1],
)


if st.button("진단 결과 보기"):
    score = focus_time + preferred_bedtime

    if score <= 3:
        chronotype = "아침형(M)"
        chrono_code = "M"
    elif score <= 6:
        chronotype = "중간형(N)"
        chrono_code = "N"
    else:
        chronotype = "저녁형(E)"
        chrono_code = "E"

    weekday_sleep = sleep_duration(
        weekday_bed_h,
        weekday_bed_m,
        weekday_wake_h,
        weekday_wake_m,
    )

    weekend_sleep = sleep_duration(
        weekend_bed_h,
        weekend_bed_m,
        weekend_wake_h,
        weekend_wake_m,
    )

    weekday_mid = mid_sleep(
        weekday_bed_h,
        weekday_bed_m,
        weekday_wake_h,
        weekday_wake_m,
    )

    weekend_mid = mid_sleep(
        weekend_bed_h,
        weekend_bed_m,
        weekend_wake_h,
        weekend_wake_m,
    )

    social_jetlag = abs(weekend_mid - weekday_mid) / 60

    if social_jetlag > 12:
        social_jetlag = 24 - social_jetlag

    if weekday_sleep < 5:
        sleep_amount = "S형(심각한 수면 부족군)"
        sleep_code = "S"
    elif weekday_sleep < 7:
        sleep_amount = "I형(만성 수면 부족군)"
        sleep_code = "I"
    else:
        sleep_amount = "L형(수면량 양호군)"
        sleep_code = "L"

    if social_jetlag < 1:
        jetlag_type = "A형(정상군)"
        jetlag_code = "A"
    elif social_jetlag < 2:
        jetlag_type = "B형(경도 위험군)"
        jetlag_code = "B"
    else:
        jetlag_type = "C형(고위험군)"
        jetlag_code = "C"

    final_code = f"{chrono_code}-{sleep_code}-{jetlag_code}"

    fatigue_score = (5 - sleepy_class) + (5 - low_concentration)
    learning_score = (5 - failed_selfstudy) + (5 - negative_academic)

    if fatigue_score >= 7:
        fatigue_level = "매우 높음"
    elif fatigue_score >= 5:
        fatigue_level = "높음"
    elif fatigue_score >= 3:
        fatigue_level = "보통"
    else:
        fatigue_level = "낮음"

    if learning_score >= 7:
        learning_level = "매우 낮음"
    elif learning_score >= 5:
        learning_level = "낮음"
    elif learning_score >= 3:
        learning_level = "보통"
    else:
        learning_level = "높음"

    st.success(f"최종 수면 코드: {final_code}")

    st.write("크로노타입:", chronotype)
    st.write("평일 수면 시간:", round(weekday_sleep, 2), "시간")
    st.write("주말 수면 시간:", round(weekend_sleep, 2), "시간")
    st.write("수면량 유형:", sleep_amount)
    st.write("사회적 시차:", round(social_jetlag, 2), "시간")
    st.write("사회적 시차 유형:", jetlag_type)
    st.write("피로도 지수:", fatigue_score, "/ 8점")
    st.write("피로도 수준:", fatigue_level)
    st.write("학습 효율성 지수:", learning_score, "/ 8점")
    st.write("학습 효율성 수준:", learning_level)

    st.subheader("맞춤형 수면 개선 전략")

    if chrono_code == "E":
        st.write("- 저녁형 성향이 있으므로 취침 시간을 하루에 15~30분씩 점진적으로 앞당겨 보세요.")
        st.write("- 기상 직후 햇빛을 쬐는 습관을 들이면 생체 리듬 조절에 도움이 됩니다.")
    elif chrono_code == "M":
        st.write("- 아침형 성향이 있으므로 현재의 규칙적인 기상 리듬을 유지하는 것이 좋습니다.")
    else:
        st.write("- 중간형 성향이므로 수면 시간과 기상 시간을 일정하게 유지하는 것이 중요합니다.")

    if sleep_code == "S":
        st.write("- 평일 수면 시간이 5시간 미만으로 매우 부족한 상태입니다. 우선 수면 시간을 단계적으로 늘리는 것이 필요합니다.")
    elif sleep_code == "I":
        st.write("- 평일 수면 시간이 5~7시간 미만으로 부족한 편입니다. 최소 7시간 이상을 목표로 수면 시간을 확보해 보세요.")
    else:
        st.write("- 평일 수면 시간이 비교적 양호합니다. 현재 수면 시간을 유지하되 취침·기상 시간의 규칙성을 함께 관리하세요.")

    if jetlag_code == "C":
        st.write("- 사회적 시차가 2시간 이상으로 높은 편입니다. 주말 늦잠을 줄이고 기상 시간을 평일과 비슷하게 유지해 보세요.")
    elif jetlag_code == "B":
        st.write("- 사회적 시차가 다소 존재합니다. 평일과 주말의 수면 시간 차이를 조금씩 줄여보세요.")
    else:
        st.write("- 사회적 시차가 낮은 편입니다. 현재의 규칙적인 수면 리듬을 유지하는 것이 좋습니다.")

    if fatigue_level in ["높음", "매우 높음"]:
        st.write("- 낮 시간 피로도가 높은 편이므로 취침 전 스마트폰 사용과 늦은 취침 습관을 점검해 보세요.")

    if learning_level in ["낮음", "매우 낮음"]:
        st.write("- 주관적 학습 효율성이 낮게 나타났으므로 집중력이 높은 시간대에 핵심 과목을 배치해 보세요.")

    file_exists = os.path.exists("sleep_data.csv")

    with open("sleep_data.csv", "a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "수면코드",
                "크로노타입",
                "평일수면시간",
                "주말수면시간",
                "사회적시차",
                "피로도점수",
                "학습효율점수",
            ])
            st.subheader("데이터 다운로드")

    with open("sleep_data.csv", "rb") as file:
        st.download_button(
            label="CSV 파일 다운로드",
            data=file,
            file_name="sleep_data.csv",
            mime="text/csv"
        )       

        writer.writerow([
            final_code,
            chronotype,
            round(weekday_sleep, 2),
            round(weekend_sleep, 2),
            round(social_jetlag, 2),
            fatigue_score,
            learning_score,
        ])

    st.info("데이터가 저장되었습니다.")


if os.path.exists("sleep_data.csv"):
    st.header("누적 통계")

    data = pd.read_csv("sleep_data.csv")

    st.write("총 참여자 수:", len(data), "명")
    st.write("평균 평일 수면시간:", round(data["평일수면시간"].mean(), 2), "시간")
    st.write("평균 사회적 시차:", round(data["사회적시차"].mean(), 2), "시간")
    st.write("평균 피로도:", round(data["피로도점수"].mean(), 2), "점")
    st.write("평균 학습 효율성 저하 지수:", round(data["학습효율점수"].mean(), 2), "점")

    st.subheader("데이터 다운로드")

    with open("sleep_data.csv", "rb") as file:
        st.download_button(
            label="CSV 파일 다운로드",
            data=file,
            file_name="sleep_data.csv",
            mime="text/csv"
        )

    st.subheader("수면 코드 분포")
    st.bar_chart(data["수면코드"].value_counts())

    st.subheader("수면 코드별 평균 피로도")
    st.bar_chart(data.groupby("수면코드")["피로도점수"].mean())

    st.subheader("수면 코드별 평균 학습 효율성 저하")
    st.bar_chart(data.groupby("수면코드")["학습효율점수"].mean())