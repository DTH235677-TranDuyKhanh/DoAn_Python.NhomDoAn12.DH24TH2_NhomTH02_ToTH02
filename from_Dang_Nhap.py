import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  
import mysql.connector

# ====== HÀM KẾT NỐI DATABASE ======
def connect_db():
    # Trả về một đối tượng kết nối tới MySQL dùng mysql.connector
    return mysql.connector.connect(
        host="localhost",         # địa chỉ máy chủ MySQL
        user="root",              # tên người dùng MySQL
        password="Khanh@091025",  # mật khẩu MySQL (hãy cẩn thận khi lưu mật khẩu trong mã)
        database="quanly_diemsinhvien"  # tên database sẽ sử dụng
    )

# ====== HÀM ĐĂNG NHẬP ======
def check_login():
    # Lấy nội dung từ các ô nhập (Entry) và loại bỏ khoảng trắng thừa
    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    # Kiểm tra xem người dùng đã nhập đủ thông tin chưa
    if not username or not password:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
        return

    try:
        # Mở kết nối tới database
        conn = connect_db()
        cur = conn.cursor()
        # Thực hiện truy vấn an toàn (dùng tham số hóa để tránh SQL injection)
        cur.execute("SELECT * FROM giangvien WHERE hoTen=%s AND matKhau=%s", (username, password))
        result = cur.fetchone()  # Lấy một dòng kết quả
        conn.close()  # Đóng kết nối sau khi xong

        # Nếu tìm thấy bản ghi khớp thì đăng nhập thành công
        if result:
            messagebox.showinfo("Thành công", f"Xin chào {username}!")
            root.destroy()  # ✅ Đóng cửa sổ login hoàn toàn
            import DoAn_Python_QL_DiemSinhVien  # import module chính (chạy chương trình chính)
        else:
            # Nếu không có bản ghi nào khớp
            messagebox.showerror("Thất bại", "Sai tên đăng nhập hoặc mật khẩu!")

    except Exception as e:
        # Bắt và hiển thị lỗi nếu có vấn đề (ví dụ: không kết nối được DB)
        messagebox.showerror("Lỗi", str(e))

# ===== GIAO DIỆN LOGIN =====
root = tk.Tk()  # Tạo cửa sổ chính của ứng dụng
root.title("Đăng nhập - Giảng viên")  # Tiêu đề cửa sổ
root.geometry("700x550")  # Kích thước mặc định của cửa sổ
root.resizable(False, False)  # Không cho thay đổi kích thước cửa sổ

# ===== CĂN GIỮA MÀN HÌNH =====
window_width = 700
window_height = 550
screen_width = root.winfo_screenwidth()   # Lấy kích thước màn hình
screen_height = root.winfo_screenheight()
# Tính toạ độ để căn giữa cửa sổ
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2) - 60
# Thiết lập geometry với toạ độ x, y để cửa sổ xuất hiện ở giữa màn hình
root.geometry(f"{window_width}x{window_height}+{x}+{y}")  

# ===== CHÈN ẢNH NỀN =====
# Mở ảnh từ file
bg_image = Image.open("anh_truong.jpg")
# Thay đổi kích thước ảnh vừa với cửa sổ (resampling để giữ chất lượng)
bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
# Chuyển sang đối tượng PhotoImage của Tkinter để hiển thị
bg_photo = ImageTk.PhotoImage(bg_image)

# Tạo label chứa ảnh nền và đặt đầy khung cửa sổ
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ===== KHUNG LOGIN =====
# Tạo một khung (Label dùng làm background) để chứa form đăng nhập
login_frame = tk.Label(root,bg="#FBFBE2", width=450, height=300)  
# Đặt khung login ở giữa cửa sổ (relx/rely = 0.5 là trung tâm)
login_frame.place(relx=0.5, rely=0.5, anchor="center")
# Label tiêu đề nằm trong khung login
tk.Label(login_frame, text="QUẢN LÝ ĐIỂM SINH VIÊN", font=("Arial", 14, "bold"),
         bg="#FBFBE2", fg="black").pack(pady=20)

# Frame chứa form (tên đăng nhập + mật khẩu)
form_frame = tk.Label(login_frame, bg="#FBFBE2")
form_frame.pack(pady=10, padx=40, fill="x")

# ===== Tên đăng nhập =====
# Nhãn cho ô nhập tên đăng nhập
tk.Label(form_frame, text="Tên đăng nhập", bg="#FBFBE2", fg="black", anchor="w").pack(fill="x", pady=(0, 2))
# Ô nhập tên đăng nhập (Entry)
entry_user = tk.Entry(form_frame, width=40)
entry_user.pack(fill="x", pady=(0, 10))

# ===== Mật khẩu =====
# Nhãn cho ô nhập mật khẩu
tk.Label(form_frame, text="Mật khẩu", bg="#FBFBE2", fg="black", anchor="w").pack(fill="x", pady=(0, 2))
# Ô nhập mật khẩu, show="*" để che ký tự khi gõ
entry_pass = tk.Entry(form_frame, width=40, show="*")
entry_pass.pack(fill="x", pady=(0, 10))

# Nút đăng nhập (khi bấm sẽ gọi hàm check_login)
btn_login = ttk.Button(login_frame, text="Đăng nhập", command=check_login)
btn_login.pack(pady=20)

# Bắt đầu vòng lặp chính của Tkinter (hiển thị cửa sổ và chờ sự kiện)
root.mainloop()

# --- GHI CHÚ ---
# 1) Bảo mật: Không nên lưu mật khẩu DB trực tiếp trong mã nguồn. Có thể sử dụng biến môi trường
#    hoặc file cấu hình được phép truy cập/đọc an toàn.
# 2) Mật khẩu người dùng: Lưu mật khẩu người dùng (giảng viên) dưới dạng hash trong DB (ví dụ bcrypt),
#    không nên so sánh mật khẩu dạng plain text như hiện tại.
# 3) Xử lý lỗi: Nên xử lý thêm các ngoại lệ cụ thể (ví dụ lỗi kết nối, lỗi truy vấn) và luôn đóng
#    cursor/connection trong khối finally nếu cần.
# 4) Tối ưu giao diện: Có thể dùng Frame thay vì Label cho layout và thêm biểu tượng, phím Enter để
#    submit, hoặc tính năng "Quên mật khẩu" nếu cần.
