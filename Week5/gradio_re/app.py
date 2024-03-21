import gradio as gr
from name_birth_identify import named_entity_recognition, find_elements, combination

def extract(input_text):
    # Extract names and birthdates from the input text
    ner_sentence = named_entity_recognition(input_text)
    names, sinh, dates = find_elements(ner_sentence)
    result = combination(names, sinh, dates)
    
    # If names and birthdates are found, highlight them in the input text
    if result:
        name_highlighted = "<span style='color:blue'>{}</span>".format(result[0])
        birthdate_highlighted = "<span style='color:green'>{}</span>".format(result[1])
        
        # Highlight name and birthdate in the input text
        input_text_highlighted = input_text.replace(result[0], "<span style='background-color:blue;color:white'>{}</span>".format(result[0]), 1)
        
        # Highlight birthdate in the input text
        dates = result[1].split('/')
        for date in dates:
            input_text_highlighted = input_text_highlighted.replace(date, "<span style='background-color:green;color:white'>{}</span>".format(date))
    else:
        name = "No name found"
        birthdate = "No birthdate found"
        input_text_highlighted = input_text
    return input_text_highlighted, result[0], result[1]

# Create a Gradio interface for the extraction function
demo = gr.Interface(fn=extract, inputs="text", outputs=["html", "text", "text"], title="Name and Birthdate Extractor")
demo.launch(share=True)