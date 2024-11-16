import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu từ file CSV
def read_data(filename):
    return pd.read_csv(filename, sep=",", header = 0, index_col = None)

# Create - nhập vào một dữ liệu mới từ bàn phím
def add_row(filename):
    df = read_data(filename) # đọc dữ liệu bằng hàm đọc dữ liệu
    print("Nhập dữ liệu mới:")
    new_data = {} # tạo thư viễn rỗng để lưu dât mới
    for column in df.columns:
        value = input(f"Nhập giá trị cho {column}: ")
        new_data[column] = value # ghi lại dữ liệu cần cập nhật theo yêu cầu của người dùng
    # Sử dụng concat thay cho append
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    # tạo một frame data mới cho nội dung cần cập nhật, concat để ghi nội dung cần cập nhật vào file
    # tham khảo ở đây: https://www.geeksforgeeks.org/pandas-concat-function-in-python/
    df.to_csv(filename, index=False) # lưu lại dữ liệu đã được cập nhật
    print("Dữ liệu mới đã được thêm.")

# Update - cập nhật data theo yêu cầu từ người dùng
def update_row(filename):
    df = read_data(filename)
    print("Nhập thông tin cần cập nhật:")
    condition_column = input("Nhập tên cột để cập nhật: ")
    condition_value = input(f"Nhập giá trị cập nhật '{condition_column}': ")

    # Tìm hàng cần cập nhật
    condition = (df[condition_column] == condition_value)
    if df[condition].empty:
        print("Không tìm thấy dữ liệu thỏa mãn.")
        return

    # Nhập dữ liệu cập nhật
    print("Nhập dữ liệu cập nhật:")
    updated_data = {}
    for column in df.columns:
        if column != condition_column:  # Không cập nhật cột điều kiện
            updated_data[column] = input(f"Nhập giá trị mới cho {column}: ")
    df.loc[condition, list(updated_data.keys())] = list(updated_data.values())
    df.to_csv(filename, index=False)
    print("Dữ liệu đã được cập nhật.")

# Delete - Xóa một hàng mà người dùng yêu cầu
def delete_row(filename):
    df = read_data(filename)
    print("Nhập vị trí cần xóa:")
    condition_column = input("Nhập tên cột cần xóa: ")
    condition_value = input(f"Nhập giá trị xóa '{condition_column}': ")

    # Tìm và xóa vị trí người dùng cần
    condition = (df[condition_column] == condition_value)
    if df[condition].empty:
        print("Không tìm thấy dữ liệu thỏa mãn điều kiện.")
        return

    df = df.drop(df[condition].index)
    df.to_csv(filename, index=False)
    print("Dữ liệu đã được xóa.")

# Làm sạch dữ liệu
def clean_data(df):
    # Xử lý giá trị thiếu
    df = df.dropna() # Bất kỳ dữ liệu nào bị thiếu một giá trị trở lên sẽ bị loại bỏ
    # Loại bỏ dữ liệu trùng lặp
    df = df.drop_duplicates() # Bất kỳ dữ liệu nào giống hệt nhau sẽ bị loại bỏ
    # Tái định dạng dữ liệu
    if 'column_name' in df.columns:
        df['column_name'] = df['column_name'].str.lower()
        df['column_name'] = df['column_name'].str.strip()
    # giúp chuyển chữ hoa thành chữ thường và loại bỏ khoảng trắng, dấu cách thừa
    print("Dữ liệu đã được làm sạch.")
    return df

# Chuẩn hóa dữ liệu
def normalize_data(df):
    # Chuyển đổi kiểu dữ liệu
    if 'numeric_column' in df.columns:
        df['numeric_column'] = pd.to_numeric(df['numeric_column'], errors='coerce')

    # Chuẩn hóa đơn vị
    if 'height_cm' in df.columns:
        df['height_m'] = df['height_cm'] / 100

    print("Dữ liệu đã được chuẩn hóa.")
    return df

# Trực quan hóa dữ liệu
def plot_data(df):

  #Biểu đồ cột giá tiền các loại bất động sản
  plt.bar(df['property_type'], df['price'], color='g', width=0.5, label="Price")
  plt.xlabel('Loại bất động sản')
  plt.ylabel('Giá')
  plt.title('Quan hệ giữa loại bất động sản và giá')
  plt.xticks(rotation=45)  # Rotate x labels for better readability
  plt.legend()
  plt.tight_layout()  # Adjust layout to make room for rotated labels
  plt.show()

  #Biểu đồ cột cho số lượng các loại bất động sản
  df['property_type'].value_counts().plot(kind='bar', color='skyblue')
  plt.title("Số lượng các loại bất động sản")
  plt.xlabel("Loại bất động sản")
  plt.ylabel("Số lượng")
  plt.show()

  #Biểu đồ phân tán giữa diện tích và giá
  plt.scatter(df['Area_in_Marla'], df['price'], color='coral')
  plt.title("Mối quan hệ giữa Diện tích và Giá")
  plt.xlabel("Diện tích (Marla)")
  plt.ylabel("Giá (VNĐ)")
  plt.show()

# Hàm main
def main():
    filename = 'Cleaned_data_for_model (1).csv'

    while True:
        print("\nChọn chức năng:")
        print("1. Đọc dữ liệu")
        print("2. Thêm dữ liệu mới")
        print("3. Cập nhật dữ liệu")
        print("4. Xóa dữ liệu")
        print("5. Làm sạch dữ liệu")
        print("6. Chuẩn hóa dữ liệu")
        print("7. Trực quan hóa dữ liệu (biểu đồ)")
        print("0. Thoát")

        choice = input("Nhập lựa chọn của bạn: ")

        if choice == "1":
            df = read_data(filename)
            print("Dữ liệu hiện tại:")
            print(df.head())
        elif choice == "2":
            add_row(filename)
        elif choice == "3":
            update_row(filename)
        elif choice == "4":
            delete_row(filename)
        elif choice == "5":
            df = read_data(filename)
            df = clean_data(df)
            df.to_csv(filename, index=False)
        elif choice == "6":
            df = read_data(filename)
            df = normalize_data(df)
            df.to_csv(filename, index=False)
        elif choice == "7":
            df = read_data(filename)
            plot_data(df)
        elif choice == "0":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

# Chạy hàm chính
if __name__ == "__main__":
  main()
