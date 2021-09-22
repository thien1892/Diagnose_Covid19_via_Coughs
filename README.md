# Chẩn đoán covid19 qua tiếng ho

 Động lực: Tiếng ho cũng như tiếng nói của mỗi người đều có những âm sắc riêng, việc sử dụng AI sẽ giúp chúng ta thấy được những âm sắc mà con người không cảm nhận được. Đây là động lực để tôi cho rằng ta có thể chẩn đoán covid-19 thông qua tiếng ho chỉ với một chiếc điện thoại. Để đào tạo mô hình thực hiện điều này, tôi đã sử dụng dữ liệu từ 5733 tiếng ho khác nhau (1199 tiếng ho từ dữ liệu warm-up, 30 tiếng ho sample và 4504 tiếng ho giai đoạn 2). Phương pháp: Mỗi âm thanh sẽ được xử lý qua một bộ lọc để xác định tiếng ho, và sau đó trích xuất tính năng thông qua thư viện libsora và mô hình Vggish để tạo thành vecto đặc trưng 732 chiều. Mô hình AI sẽ dự được đào tạo để dự đoán xác suất nhiễm covid-19. Mô hình của tôi được đào tạo, xác thực trên 5733 tiếng ho, kiểm tra trên dữ liệu private_test 1627 file âm thanh. Kết quả: Với dữ liệu test_private mô hình cho kết quả AUC: 90.43%. Kết luận: AI có thể tạo ra một công cụ sàng lọc với quy mô lớn, miễn phí, và không cần can thiệp xâm lấn tới con người, và cho kết quả ngay theo thời gian thực.

 # Dữ liệu

 - Train set: https://bit.ly/aicv115m-final-public-train
 - Mô tả chi tiết metadata kèm theo: https://bit.ly/aicv115m-final-data-desc
 - Dữ liệu bổ sung: https://bit.ly/aicv115m_extra_public_train_1235samples
 - Warm up: https://bit.ly/aicv115m-final-public-train
 - Private Test: https://bit.ly/aicv115m-final-private-test

