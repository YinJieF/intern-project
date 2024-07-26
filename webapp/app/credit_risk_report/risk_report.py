# 1. get the name of the person
# 2. get the judgement_text of the person
# 3. prompt + name + judgement_text to llm

from app.Infra.judgement_bq import get_judgement_pdf
from app.Infra.llama_generate import process_text

def get_risk_report(name, jlr_link):
    judgement_pdf = get_judgement_pdf(jlr_link)
    risk_report = process_text(judgement_pdf)

    return risk_report

#print(get_risk_report("Nguyen Van A", "https://congbobanan.toaan.gov.vn/2ta827827t1cvn/chi-tiet-ban-an"))