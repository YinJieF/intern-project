import re
import pickle
import keras
import tensorflow as tf
import numpy as np
from data_preprocess import map_record_to_training_data
from modeling import CustomNonPaddingTokenLoss
    
def lookup(tokens):
    # Load the list from the file
    with open('./resources/vocabulary.pkl', 'rb') as f:
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
    # Load model
    tf.keras.utils.get_custom_objects()['CustomNonPaddingTokenLoss'] = CustomNonPaddingTokenLoss
    # Load model
    loaded_model = tf.keras.models.load_model("./resources/trained_model/ner_model.keras")

    print(loaded_model.summary())
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
result = prediction(format_datatype(sample_input))
print(result)
print(sample_input.split(' '))
print(len(result))