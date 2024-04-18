from flask import render_template, request, jsonify
from underthesea import word_tokenize
from app.inference.predict import prediction

def model_inference():
    if request.method == 'GET':
        sample = "Nguyễn Quốc H, tên gọi khác: Không; sinh ngày 27 tháng 3 năm 1997 tại Đà Nẵng. Nơi ĐKHKTT: Thôn Q, xã H, huyện H, thành phố Đà Nẵng. Chỗ ở: Tổ 5 thôn Q, xã H, huyện H, thành phố Đà Nẵng; Nghề nghiệp: Không; trình độ văn hoá (học vấn): 12/12; dân tộc: Kinh; giới tính: Nam; tôn giáo: Phật giáo; quốc tịch: Việt Nam; con ông Nguyễn C, sinh năm: 1967 và bà Võ Thị L (chết); vợ Nguyễn Thị Thanh H, sinh năm 1997, có 01 con sinh năm 2020; gia đình có 03 anh em, bị cáo là con thứ nhất. Tiền án, tiền sự: Không; Nhân thân: Ngày 28/9/2015, bị Tòa án nhân dân thành phố Đà Nẵng xử phạt 04 năm tù giam về tội “Vận chuyển trái phép chất ma túy” theo bản án số 212/2015/HSPT. Chấp hành án xong ngày 15/7/2018, đã nộp tiền án phí. Bị cáo bị tạm giữ tại Nhà tạm giữ Công an quận Hải Châu từ ngày 18/5/2021, có mặt tại phiên tòa. "
        tags = prediction(sample)
        token_tag_pairs = list(zip(word_tokenize(sample), tags))
        return render_template('predict.html', input_text=sample, token_tag_pairs=token_tag_pairs)
    
    elif request.method == 'POST':
        data =request.json
        input_text = data.get('input_text')
        tags = prediction(input_text)  # You need to implement the prediction function
        token_tag_pairs = list(zip(word_tokenize(input_text), tags))
        return jsonify(token_tag_pairs=token_tag_pairs)
    