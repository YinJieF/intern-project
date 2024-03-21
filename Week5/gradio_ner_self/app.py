from ner import format_datatype, prediction
import gradio as gr

# Define a function to predict named entities using your custom model
def predict_ner(text):
    # Format the input text according to your data format
    data = format_datatype(text)
    # Use your NER model to predict named entities
    predicted_entities = prediction(data)

    formatted_output = []
    texts = text.split(' ')
    start_index = 0
    for i in range(len(predicted_entities)):
        if predicted_entities[i] != 'other':
            print(texts[i], predicted_entities[i], i)
            entity_info = {'entity': predicted_entities[i],  
                           'score': 1, 
                           'index': i, 
                           'word': texts[i],
                           'start': start_index,
                           'end': start_index + len(texts[i]) 
                            }
            formatted_output.append(entity_info)
        start_index += len(texts[i]) + 1
    # Return a properly formatted JSON object
    return {"text": text, "entities": formatted_output}

# Example inputs for the Gradio interface
sample_input = ['1/ Trần Văn T, sinh ngày 01 tháng 01 năm 1987 tại Quảng Nam; Nơi cư trú: thôn 04, xã TG, huyện Bắc Trà My, tỉnh Quảng Nam; nghề nghiệp: nông; trình độ văn hoá: 03/12; dân tộc: Cadong; giới tính: nam; tôn giáo: không; quốc tịch: Việt Nam; con ông Trần Văn Tiếu và bà Thanh Thị Liên; vợ tên Phạm Thị Hiếm và 02 con; tiền án, tiền sự: không; Bị cáo bị áp dụng biện pháp ngăn chặn: “Cấm đi khỏi nơi cư trú”, có mặt tại phiên tòa. 2/ Đinh Tấn M, sinh ngày 21 tháng 6 năm 1995 tại Quảng Nam; Nơi cư trú: thôn 04, xã TG, huyện Bắc Trà My, tỉnh Quảng Nam; nghề nghiệp: nông; trình độ']
                
# Create a Gradio interface
demo = gr.Interface(
    predict_ner,
    gr.Textbox(placeholder="Enter sentence here..."), 
    gr.HighlightedText(),
    title="Named Entity Recognition",
    examples=sample_input
)

if __name__ == "__main__":
    demo.launch(server_port=8888)