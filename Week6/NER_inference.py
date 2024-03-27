import re
import pickle
import keras
import tensorflow as tf
import numpy as np

class CustomNonPaddingTokenLoss(keras.losses.Loss):
    def __init__(self, reduction=keras.losses.Reduction.AUTO, name="custom_ner_loss"):
        super().__init__(reduction=reduction, name=name)

    def call(self, y_true, y_pred):
        loss_fn = keras.losses.SparseCategoricalCrossentropy(
            from_logits=False, reduction=self.reduction
        )
        loss = loss_fn(y_true, y_pred)
        mask = tf.cast((y_true > 0), dtype=tf.float32)
        loss = loss * mask
        return tf.reduce_sum(loss) / tf.reduce_sum(mask)

def map_record_to_training_data(record):
    record = tf.strings.split(record, sep="\t")
    length = tf.strings.to_number(record[0], out_type=tf.int32)
    tokens = record[1 : length + 1]
    tags = record[length + 1 :]
    tags = tf.strings.to_number(tags, out_type=tf.int64)
    tags += 1
    return tokens, tags

def lookup(tokens):
    # Load the list from the file
    with open('/content/drive/MyDrive/NER/vocabulary.pkl', 'rb') as f:
        loaded_list = pickle.load(f)
    # The StringLookup class will convert tokens to token IDs
    lookup_layer = keras.layers.StringLookup(vocabulary=loaded_list)

    # No need to lowercase Vietnamese characters
    return lookup_layer(tokens)

def format_datatype(data):
    tokens =  [re.sub(r'[;,]', '', d) for d in data.split(' ')]
    #default is 0, since is for prediction
    ner_tags = [0 for d in data.split(' ')]

    #tab to separate
    string_input = str(len(tokens))+ "\t"+ "\t".join(tokens)+ "\t"+ "\t".join(map(str, ner_tags))
    string_input = tf.data.Dataset.from_tensor_slices([string_input])


    finalize_input = (string_input.map(map_record_to_training_data)
                      .map(lambda x, y: (lookup(x),  y))
                      .padded_batch(1)
                      )

    return finalize_input

def prediction(data):
    # Register the custom loss function with TensorFlow
    tf.keras.utils.get_custom_objects()['CustomNonPaddingTokenLoss'] = CustomNonPaddingTokenLoss
    # Load model
    loaded_model = tf.keras.models.load_model("/content/drive/MyDrive/NER/ner_model")

    all_predicted_tag_ids = []

    for x, _ in data:
        print("Input Tensor Info:")
        print("Data Type:", x.dtype)
        print("Shape:", x.shape)
        output = loaded_model(x, training=False)
        predictions = np.argmax(output, axis=-1)
        predictions = np.reshape(predictions, [-1])
        all_predicted_tag_ids.append(predictions)

    all_predicted_tag_ids = np.concatenate(all_predicted_tag_ids)

    ner_labels = ["[PAD]", "N", "M", "other"]
    mapping =  dict(zip(range(len(ner_labels)), ner_labels))
    predicted_tags = [mapping[tag] for tag in all_predicted_tag_ids]

    return predicted_tags

sample_input = "1/ Trần Văn T, sinh ngày 01 tháng 01 năm 1987 tại Quảng Nam; Nơi cư trú: thôn 04, xã TG, huyện Bắc Trà My, tỉnh Quảng Nam; nghề nghiệp: nông; trình độ văn hoá: 03/12; dân tộc: Cadong; giới tính: nam; tôn giáo: không; quốc tịch: Việt Nam; con ông Trần Văn Tiếu và bà Thanh Thị Liên; vợ tên Phạm Thị Hiếm và 02 con; tiền án, tiền sự: không; Bị cáo bị áp dụng biện pháp ngăn chặn: “Cấm đi khỏi nơi cư trú”, có mặt tại phiên tòa. 2/ Đinh Tấn M, sinh ngày 21 tháng 6 năm 1995 tại Quảng Nam; Nơi cư trú: thôn 04, xã TG, huyện Bắc Trà My, tỉnh Quảng Nam; nghề nghiệp: nông; trình độ"
#sample_input = "Hello world, my name is John, I live in New York, my birthday is 10/02/1990."
sample_input = "<Page:1>TÒA ÁN NHÂN DÂN CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM HUYỆN LỆ THỦY Độc lập - Tự do - Hạnh phúc TỈNH QUẢNG BÌNH Bản án số: 50/2020/HS-ST Ngày 30 - 9 - 2020 NHÂN DANH NƯỚC CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM TÒA ÁN NHÂN DÂN HUYỆN LỆ THUỶ, TỈNH QUẢNG BÌNH - Thành phần Hội đồng xét xử sơ thẩm gồm có: Chủ tọa phiên tòa: Ông Nguyễn Thanh Hải. Các Hội thẩm nhân dân: Ông Lê Ngọc Thành và ông Trương Hải Nam. - Thư ký Tòa án ghi biên bản phiên tòa: Bà Nguyễn Thị Hoài Thương - Thư ký Toà án nhân dân huyện Lệ Thuỷ, tỉnh Quảng Bình. - Đại diện Viện kiểm sát nhân dân huyện Lệ Thủy tham gia phiên tòa: Bà Nguyễn Thị Diệp - Kiểm sát viên. Trong ngày 30 tháng 9 năm 2020, tại trụ sở Toà án nhân dân huyện Lệ Thuỷ, tỉnh Quảng Bình xét xử sơ thẩm công khai vụ án hình sự sơ thẩm thụ lý số 50/TLST-HS ngày 04 tháng 9 năm 2020 theo Quyết định đưa vụ án ra xét xử số: 53/2020/QĐXXST-HS ngày 16 tháng 9 năm 2020. 1. Nguyễn Hải Q; Sinh ngày 20 tháng 2 năm 1990 tại Quảng Bình. Nơi cư trú: Thôn L, xã Tr, huyện L, tỉnh Quảng Bình; nghề nghiệp: Lao động tự do; trình độ học vấn: Lớp 12/12; dân tộc: Kinh; giới tính: Nam; tôn giáo: không; quốc tịch: Việt Nam; con ông Nguyễn Hữu D (đã chết) và bà Mai Thị H; có vợ Lê Thị K, sinh năm 1991 và có 01 con sinh năm 2014; tiền án, tiền sự: không; bị tạm giữ 09 ngày, từ ngày 13/6/2020 đến ngày 22/6/2020; hiện tại bị áp dụng biện pháp ngăn chặn cấm đi khỏi nơi cư trú, có mặt. 2. Võ Văn D; Sinh ngày 12 tháng 12 năm 1983 tại Quảng Bình; Nơi cư trú: Thôn X, xã M, huyện L, tỉnh Quảng Bình; nghề nghiệp: Lái máy công trình xây dựng; trình độ học vấn: Lớp 9/12; dân tộc: Kinh; giới tính: Nam; tôn giáo: không; quốc tịch: Việt Nam; con ông Võ Văn B và bà Trương Thị H; có vợ Nguyễn Thị Ngọc L, sinh năm 1985 và có 02 con, lớn sinh năm 2009, nhỏ sinh năm 2016; tiền án, tiền sự: không; bị tạm giữ 09 ngày, từ ngày 13/6/2020 đến ngày 22/6/2020; hiện tại bị áp dụng biện pháp ngăn chặn cấm đi khỏi nơi cư trú, có mặt. 3. Nguyễn Văn Th; Sinh ngày: 20 tháng 6 năm 1988 tại Quảng Bình. Nơi cư trú: Thôn L, xã M, huyện L, tỉnh Quảng Bình; nghề nghiệp: Lái xe; trình độ học vấn: Lớp 12/12; dân tộc: Kinh; giới tính: Nam; tôn giáo: không; quốc tịch: Việt Nam; con ông Nguyễn Văn M và bà Nguyễn Thị D; chưa có vợ, con; tiền án, tiền sự: không; bị tạm giữ 09 ngày, từ ngày 13/6/2020 đến ngày 22/6/2020; hiện tại bị áp dụng biện pháp ngăn chặn cấm đi khỏi nơi cư trú, có mặt. 4. Lê Trung Th; Sinh ngày 20 tháng 01 năm 1960 tại Quảng Bình.<Page:2>Nơi cư trú: Thôn L, xã M, huyện L, tỉnh Quảng Bình; nghề nghiệp: Lao động tự do; trình độ học vấn: Lớp 10/10; dân tộc: Kinh; giới tính: Nam; tôn giáo: không; quốc tịch: Việt Nam; con ông Lê Văn Ng và bà Hoàng Thị H (hiện hai ông bà đã chết); có vợ Trần Thị Th, sinh năm 1965 và có 05 con, lớn nhất sinh năm 1987 nhỏ nhất sinh năm 2003; tiền án, tiền sự: không; bị tạm giữ 09 ngày, từ ngày 13/6/2020 đến ngày 22/6/2020; hiện tại bị áp dụng biện pháp ngăn chặn cấm đi khỏi nơi cư trú, có mặt. * "
result = prediction(format_datatype(sample_input))
print(result)
print(sample_input.split(' '))
print(len(result))