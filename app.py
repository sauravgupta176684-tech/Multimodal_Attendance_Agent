import streamlit as st
import cv2
import mediapipe as mp
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="AI Attendance System", layout="wide")
st.title("Multimodal Attendance & Engagement Agent")

CSV_FILE = "attendance.csv"
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Name", "Date", "Time", "Status"]).to_csv(CSV_FILE, index=False)

def mark_attendance(name):
    df = pd.read_csv(CSV_FILE)
    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")
    
    if not ((df["Name"] == name) & (df["Date"] == today)).any():
        new_row = pd.DataFrame([{"Name": name, "Date": today, "Time": now_time, "Status": "Present"}])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Camera Feed")
    run_cam = st.checkbox("Start Camera")
    FRAME_WINDOW = st.image([])

with col2:
    st.subheader("Attendance Log")
    log_placeholder = st.empty()

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

while run_cam:
    ret, frame = cap.read()
    if not ret:
        st.write("Camera not accessible")
        break
    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb)
    
    if results.detections:
        for detection in results.detections:
            mp.solutions.drawing_utils.draw_detection(frame, detection)
        mark_attendance("Student_1")
        cv2.putText(frame, "Present & Focused", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No Face Detected", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    log_placeholder.dataframe(pd.read_csv(CSV_FILE))

cap.release()