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

# Đánh giá:
## 1.	Kết quả và tốc độ xử lý:
-	Tôi trích xuất các feature của file âm thanh của bộ dữ liệu train và private_test thành những file csv, và sử dụng google coblab để đào tạo mô hình.
-	Về cách chia dữ liệu train và xác thực: Dữ liệu xác thực, tôi lấy 20% dữ liệu tiếng ho của giai đoạn 2; những dữ liệu còn lại tôi để vào tập train.
-	Tôi sử dụng Xgboost và tập trung vào việc điều chỉnh các siêu tham số: max_depth, n_estimators, colsample_bytree và learning rate.
-	Tôi xây dựng mô hình theo 3 hướng: 1) Sử dụng dữ liệu thường, 2) Sử dụng dữ liệu có tăng cường để tránh overfit bằng cách thêm tiếng ồn, tăng giảm cao độ, thay đổi cường độ và tốc độ. 3) Normalize âm thanh về [-1, 1] và tăng cường dữ liệu. Kết quả của các mô hình và thời gian train:
<img src = 'https://i.imgur.com/3a7b96m.jpg'>

## 2. Fearture quan trọng

<img src = 'https://i.imgur.com/1tca6Gy.jpg'>

## 3.	Tiềm năng, phương án cải thiện và bước tiếp theo
### 3.1.	Dữ liệu
Bước đầu tiên mà tôi nghĩ để cải thiện mô hình là xem xét lại dữ liệu:
-	Khi áp dụng thực tế, tôi nghĩ nên yêu cầu người dùng cung cấp tiếng ho rõ ràng, hạn chế lẫn tạp âm  bộ lọc ho sẽ yêu cầu người dùng thảo mãn điều này.
-	Tôi đã thử trích xuất âm thanh tiếng ho (gồm 1 tiếng ho, âm thanh lấy lại hơi cổ họng và 1 tiếng ho tiếp theo) nhưng không cho kết quả khả quan. Tôi nghe lai một vài âm thanh không thể trích xuất theo các này, thấy đa số những tiếng ho này không tự nhiên, không thấy âm thanh lấy lại hơi cổ họng. Liệu có thể yêu cầu người dùng cung cấp tiếng ho tự nhiên hay không? (trên thực tế, tôi khó có thể ho một cách tự nhiên nếu mình không bị ho thật sự).
-	Tuổi tác và giới tính: Thực tế ta có thể yêu cầu người dùng cung cấp dữ liệu này mà ít có sai số (ta có thể dùng AI xác thực lại nếu cần). Ở phần warm-up, 2 feature này giúp tôi cải thiện mô hình thêm 2%-3%
-	Các triệu chứng: Việc khai báo bệnh nền có ý nghĩa rất quan trọng trong chữa trị covid-19. Các triệu chứng thường gặp của covid-19 là cách thủ công hữu hiệu chúng ta đang kiểm tra người dân, nhưng thực tế có nhiều người nhiễm bệnh mà không có triệu chứng. Nếu thêm các triệu chứng mà những feature này chiếm phần quan trọng lớn, liệu có xảy ra sai lệch thiên vị hay không? Tôi chưa xây dựng mô hình theo hướng này nhưng là đây cách mà tôi có thể cải thiện mô hình.
-	Các mô hình của tôi đều có độ nhạy chưa cao (tỷ lệ người bị covid thật được dự đoán là dương tính) --> cần thu thập thêm dữ liệu dương tính.
### 3.2.	Mô hình
-	Do nguồn lực có hạn nên việc tinh chỉnh siêu tham số của tôi mang tính chủ quan nhiều --> tiếp tục tinh chỉnh siêu tham số có thể cải thiện được mô hình.
-	Thường thì việc normalize và tăng cường dữ liệu đưa lại kết quả tốt hơn cho mô hình --> tôi cần xem xét lại cách mình thực hiện và nên tiếp tục theo hướng nào để gia tăng hiệu quả.

# Tham khảo
1. Exploring Automatic Diagnosis of COVID-19 from Crowdsourced Respiratory Sound Data: [click here](https://arxiv.org/abs/2006.05919)
2. Dữ liệu đã trích xuất: https://www.kaggle.com/thien1892/covid-732-na
3. Ví dụ dự đoán 1 file âm thanh: https://github.com/thien1892/Diagnose_Covid19_via_Coughs/blob/main/samples_notebook.ipynb