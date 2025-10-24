import os
import streamlit as st
import pandas as pd
import time 
from datetime import datetime

ts=time.time()
date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp=datetime.fromtimestamp(ts).strftime("%H:%M-%S")

from streamlit_autorefresh import st_autorefresh

count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")


csv_path = os.path.join("Attendance", f"Attendance_{date}.csv")
txt_path = os.path.join("Attendance", f"Attendance_{date}.txt")

try:
    df = pd.read_csv(csv_path)
    st.dataframe(df.style.highlight_max(axis=0))
    # ensure directory exists and append a simple human-readable log
    os.makedirs(os.path.dirname(txt_path), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(txt_path, "a", encoding="utf-8") as f:
        f.write(f"---- {now} ----\n")
        f.write(df.to_string(index=False))
        f.write("\n\n")
    st.info(f"Saved simple log to {txt_path}")
except FileNotFoundError:
    st.error(f"CSV not found: {csv_path}")
except Exception as e:
    st.error(f"Error reading/saving attendance: {e}")