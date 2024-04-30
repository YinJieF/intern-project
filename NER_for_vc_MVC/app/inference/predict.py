import pickle
import keras
import tensorflow as tf
import numpy as np
from keras import layers
from app.train.modeling import TransformerBlock, TokenAndPositionEmbedding 
from underthesea import word_tokenize

@keras.utils.register_keras_serializable(package="CustomModels")
class NERModel(keras.Model):
    def __init__(
        self, num_tags, vocab_size, maxlen=512, embed_dim=32, num_heads=2, ff_dim=32, **kwargs
    ):
        super().__init__()
        self.num_tags = num_tags
        self.vocab_size = vocab_size
        self.maxlen = maxlen
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim

        self.embedding_layer = TokenAndPositionEmbedding(maxlen, vocab_size, embed_dim)
        self.transformer_block = TransformerBlock(embed_dim, num_heads, ff_dim)
        self.dropout1 = layers.Dropout(0.1)
        self.ff = layers.Dense(ff_dim, activation="relu")
        self.dropout2 = layers.Dropout(0.1)
        self.ff_final = layers.Dense(num_tags, activation="softmax")

    def call(self, inputs, training=False):
        x = self.embedding_layer(inputs)
        x = self.transformer_block(x)
        x = self.dropout1(x, training=training)
        x = self.ff(x)
        x = self.dropout2(x, training=training)
        x = self.ff_final(x)
        return x
    
    def get_config(self):
        config = {
            'num_tags': self.num_tags,
            'vocab_size': self.vocab_size,
            'maxlen': self.maxlen,
            'embed_dim': self.embed_dim,
            'num_heads': self.num_heads,
            'ff_dim': self.ff_dim,
        }
        base_config = super(NERModel, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class CustomNonPaddingTokenLoss(keras.losses.Loss):
    def __init__(self, reduction='sum', name="custom_ner_loss"):
        super().__init__(reduction='sum', name=name)

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
    with open('app/inference/model_for_predict/vocabulary.pkl', 'rb') as f:
        loaded_list = pickle.load(f)
    # The StringLookup class will convert tokens to token IDs
    lookup_layer = keras.layers.StringLookup(vocabulary=loaded_list)

    # No need to lowercase Vietnamese characters
    return lookup_layer(tokens)

def format_datatype(data):
    tokens = word_tokenize(data)
    #tokens =  [re.sub(r'[;,]', '', d) for d in data.split(' ')]
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
    data = format_datatype(data)
    # Register the custom loss function with TensorFlow
    tf.keras.utils.get_custom_objects()['CustomNonPaddingTokenLoss'] = CustomNonPaddingTokenLoss
    # Load mode
    loaded_model = tf.keras.models.load_model("./app/inference/model_for_predict/ner_model.keras")

    all_predicted_tag_ids = []

    for x, _ in data:
        output = loaded_model(x, training=False)
        predictions = np.argmax(output, axis=-1)
        predictions = np.reshape(predictions, [-1])
        all_predicted_tag_ids.append(predictions)

    all_predicted_tag_ids = np.concatenate(all_predicted_tag_ids)

    ner_labels = ["[PAD]", "N", "M","B-PER","I-PER", "other"]
    mapping =  dict(zip(range(len(ner_labels)), ner_labels))
    predicted_tags = [mapping[tag] for tag in all_predicted_tag_ids]

    return predicted_tags

# sample_input = "1/ Trần Văn T, sinh ngày 01 tháng 01 năm 1987 tại Quảng Nam; Nơi cư trú: thôn 04, xã TG, huyện Bắc Trà My, tỉnh Quảng Nam; nghề nghiệp: nông; trình độ văn hoá: 03/12; dân tộc: Cadong; giới tính: nam; tôn giáo: không; quốc tịch: Việt Nam; con ông Trần Văn Tiếu và bà Thanh Thị Liên; vợ tên Phạm Thị Hiếm và 02 con; tiền án, tiền sự: không; Bị cáo bị áp dụng biện pháp ngăn chặn: “Cấm đi khỏi nơi cư trú”, có mặt tại phiên tòa. 2/ Đinh Tấn M, sinh ngày 21 tháng 6 năm 1995 tại Quảng Nam; Nơi cư trú: thôn 04, xã TG, huyện Bắc Trà My, tỉnh Quảng Nam; nghề nghiệp: nông; trình độ"
# sample_input = "Nguyễn Quốc H, tên gọi khác: Không; sinh ngày 27 tháng 3 năm 1997 tại Đà Nẵng. Nơi ĐKHKTT: Thôn Q, xã H, huyện H, thành phố Đà Nẵng. Chỗ ở: Tổ 5 thôn Q, xã H, huyện H, thành phố Đà Nẵng; Nghề nghiệp: Không; trình độ văn hoá (học vấn): 12/12; dân tộc: Kinh; giới tính: Nam; tôn giáo: Phật giáo; quốc tịch: Việt Nam; con ông Nguyễn C, sinh năm: 1967 và bà Võ Thị L (chết); vợ Nguyễn Thị Thanh H, sinh năm 1997, có 01 con sinh năm 2020; gia đình có 03 anh em, bị cáo là con thứ nhất. Tiền án, tiền sự: Không; Nhân thân: Ngày 28/9/2015, bị Tòa án nhân dân thành phố Đà Nẵng xử phạt 04 năm tù giam về tội “Vận chuyển trái phép chất ma túy” theo bản án số 212/2015/HSPT. Chấp hành án xong ngày 15/7/2018, đã nộp tiền án phí. Bị cáo bị tạm giữ tại Nhà tạm giữ Công an quận Hải Châu từ ngày 18/5/2021, có mặt tại phiên tòa. "
# result = prediction(sample_input)
# wt = word_tokenize(sample_input)
# for i in range(len(result)):
#     if result[i] != 'other' and len(wt[i].split(' ')) > 1 and wt[i] not in ",/:;":
#         print(result[i], wt[i])