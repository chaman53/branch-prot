from fastapi import HTTPException
from elasticsearch import Elasticsearch
import os, logging

environ_logger = os.environ.get('LOGGER', "gunicorn.error")
logger = logging.getLogger(environ_logger)

try:
    elasticsearch_end_point = os.environ["ELASTICSEARCH_END_POINT"]
    elasticsearch_user_name = os.environ["ELASTICSEARCH_USER_NAME"]
    elasticsearch_password = os.environ["ELASTICSEARCH_PASSWORD"]
except Exception as e:
    logger.error(f"Environment variable not found: {e}")


es_field_mapping = {
    # Fields for extracted data
    "study_design" : "Study Design",
    "randomization_method" : "Randomization Method",
    "control" : "Control",
    "blinding" : "Blinding",
    "population" : "Population",
    "diagnosis_of_interest" : "Diagnosis of Interest",
    "diagnostic_criteria" : "Diagnostic Criteria",
    "age" : "Age",
    "sex" : "Sex",
    "treatment" : "Treatment",
    "bytreatment" : "#by Treatment",
    "dose" : "Dose",
    "dosage_form" : "Dosage Form",
    "dose_frequency" : "Dose Frequency",
    "mode_of_administration" : "Mode of Administration",
    "efficacy_endpoints" : "Efficacy Endpoints",
    "safety_endpoints" : "Safety Endpoints",
    "enrolled" : "#Enrolled",
    "analyzed_total" : "#Analyzed Total",
    "analyzed_efficacy" : "#Analyzed Efficacy",
    "analyzed_safety" : "#Analyzed Safety",
    "auther": "Author",
    "treatment_duration" : "Treatment Duration",
    "by_treatment" : "#by Treatment",
    "disease_condition" : "Disease/Condition",
    "aim" : "Aim",
    "country" : "Country",
    "efficacy_results" : "Efficacy Results",
    "safety_results" : "Safety Results",
    "conclusion" : "Conclusion",
    "publication_year" : "Year of publication",
    "primary_author" : "Author",
    "cite_information" : "cite_information",
    # Fields for sections and summary
    "pdf_tables" : "pdf_tables",
    "title" : "title",
    "abstract" : "abstract",
    "table_summary" : "table_summary",
    "single_article_summary" : "single_article_summary",
    "method_section": "method_section",
    "result_section": "result_section",
    "conclusion_section": "conclusion_section",
    "ocr_full_text": "ocr_full_text",
    "report_name": "Report Name",
    "report_type": "Report Type",
    "serial_number": "Serial Number"
}

meta_data_es_field_mapping = {
    # field for meta_data
    "title" : "title",
    "abstract" : "abstract",
    "publication_year" : "publicationYear",
    "publication_date" : "publishDate",
    "first_author" : "firstAuthor",
    "author" : "author",
    "abbrev_title": "abbreviatedTitle",
    "issn": "issn",
    "publisher": "publisher",
    "volume": "volume",
    "issue": "issue",
    "page_from": "pageFrom",
    "page_to": "pageTo",
}


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch(
        elasticsearch_end_point,
        basic_auth=(
            elasticsearch_user_name, 
            elasticsearch_password
        )
    )
    if _es.ping():
        logger.info('Elasticsearch connected.')
    else:
        logger.error('Elasticsearch not connected.')
        raise HTTPException(status_code=404, detail='Elasticsearch not connected.')
    return _es


def retrieve_record(es_object, index, _id):
    is_retrieved = True
    try:
        outcome = es_object.get(index=index, id=_id)
    except Exception as e:
        logger.error(f'Exception in retrieving data from ES : {str(e)}')
        is_retrieved = False
        outcome = None
        raise HTTPException(status_code=404, detail=f'Exception in retrieving data from ES : {str(e)}')
    finally:
        return is_retrieved, outcome
