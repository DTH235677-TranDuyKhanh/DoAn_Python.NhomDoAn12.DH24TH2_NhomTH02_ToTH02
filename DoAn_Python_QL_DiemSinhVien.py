import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
# ====== Kết nối MySQL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",     # Địa chỉ của server MySQL (thường là localhost nếu bạn cài trên máy)
        user="root",          # Tên người dùng MySQL của bạn (mặc định là root)
        password="Khanh@091025",          # Mật khẩu MySQL của bạn (điền vào nếu bạn có đặt)
        database="ql_diem_sinhvien" # Tên database bạn muốn kết nối tới
    )
# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=700, h=500):
 ws = win.winfo_screenwidth()
 hs = win.winfo_screenheight()
 x = (ws // 2) - (w // 2)
 y = (hs // 2) - (h // 2)
 win.geometry(f'{w}x{h}+{x}+{y}')
