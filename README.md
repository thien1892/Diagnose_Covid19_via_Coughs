# Chẩn đoán covid19 qua tiếng ho

 **Động lực**: Tiếng ho cũng như tiếng nói của mỗi người đều có những âm sắc riêng, việc sử dụng AI sẽ giúp chúng ta thấy được những âm sắc mà con người không cảm nhận được. Đây là động lực để tôi cho rằng ta có thể chẩn đoán covid-19 thông qua tiếng ho chỉ với một chiếc điện thoại. Để đào tạo mô hình thực hiện điều này, tôi đã sử dụng dữ liệu từ 5733 tiếng ho khác nhau (1199 tiếng ho từ dữ liệu warm-up, 30 tiếng ho sample và 4504 tiếng ho giai đoạn 2). **Phương pháp**: Mỗi âm thanh sẽ được xử lý qua một bộ lọc để xác định tiếng ho, và sau đó trích xuất tính năng thông qua thư viện libsora và mô hình Vggish để tạo thành vecto đặc trưng 732 chiều. Mô hình AI sẽ dự được đào tạo để dự đoán xác suất nhiễm covid-19. Mô hình của tôi được đào tạo, xác thực trên 5733 tiếng ho, kiểm tra trên dữ liệu private_test 1627 file âm thanh. **Kết quả**: Với dữ liệu test_private mô hình cho kết quả AUC: 90.43%. **Kết luận**: AI có thể tạo ra một công cụ sàng lọc với quy mô lớn, miễn phí, và không cần can thiệp xâm lấn tới con người, và cho kết quả ngay theo thời gian thực.

 # Dữ liệu

 - Train set: https://bit.ly/aicv115m-final-public-train
 - Mô tả chi tiết metadata kèm theo: https://bit.ly/aicv115m-final-data-desc
 - Dữ liệu bổ sung: https://bit.ly/aicv115m_extra_public_train_1235samples
 - Warm up: https://bit.ly/aicv115m-final-public-train
 - Private Test: https://bit.ly/aicv115m-final-private-test

# Phương pháp

<img src = 'https://i.imgur.com/JgfOy19.jpg'>

 ## 1.	Bộ lọc tiếng ho:
   Khi kiểm tra dữ liệu private_test có cùng phân phối với tập train hay không (tôi cho rằng các feature sau khi trích xuất sẽ nằm trong khoảng giá trị trung bình +/- 3 lần độ lệch chuẩn của tập train). Sau khi nghe bằng tai 57 file âm thanh có số lượng feature nằm ngoài phân phối >=173, tôi phát hiện ra nhiều âm thanh của tập private_test không phải là tiếng ho. Tôi nghĩ cần một bộ lọc tiếng ho trước khi trích xuất các fearture. Tôi thực hiện bằng cách:
-	Cắt bỏ khoảng lặng của âm thanh
-	Sử dụng học chuyển tiếp mô hình yamnet, loại bỏ với tiếng ho và tiếng nói ở ngưỡng phù hợp.
## 2.	Trích xuất feature qua thư viện Librosa:
### 2.1.	Feature là chuỗi, mảng:
-	Tôi trích xuất các feature là chuỗi, mảng như: mfcc (3 biến thể của mfcc), rms, centroid, rolloff, zero_croosing.
-	Các feature này tôi lấy 11 chỉ số quan trọng là : mean, std, median, max, min, q1, q3, iqr, rms, kurtosis, skewness,
### 2.2.	Các feature không phải là mảng, chuỗi:
-	Dộ dài âm thanh sau khi cắt bỏ khoảng lặng, tempo và  times_onset.
## 3.	Trích xuất feature qua Vggish:
-	Tôi chuyển âm thanh về rate 16000 Hz, sau đó sử dụng mô hình Vggish. Tôi reduce về giá trị trung bình và độ lệch chuẩn của kết quả sau khi áp dụng mô hình.

File âm thanh sau khi trích xuất feature sẽ được mã hóa thành 1 vecto 732 chiều (3 x13 x 11 + 4 x11 + 3+128 x 2). Tôi sử dụng Xgboost để dự đoán xác suất bị covid-19 của tiếng ho.

