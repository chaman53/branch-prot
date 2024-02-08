from fastapi import HTTPException
import os, logging, json, re
import openai

from app.utils.es_utils import *

environ_logger = os.environ.get('LOGGER', "gunicorn.error")
logger = logging.getLogger(environ_logger)

try:
    elasticsearch_end_point = os.environ["ELASTICSEARCH_END_POINT"]
    elasticsearch_user_name = os.environ["ELASTICSEARCH_USER_NAME"]
    elasticsearch_password = os.environ["ELASTICSEARCH_PASSWORD"]

    openai.api_type = os.environ["MULTI_ARTICLE_SUMMARY_CHAT_OPEN_AI_AZURE_OPENAI_API_TYPE"]
    openai.api_base = os.environ["MULTI_ARTICLE_SUMMARY_CHAT_OPEN_AI_AZURE_OPENAI_API_BASE"]
    openai.api_version = os.environ["MULTI_ARTICLE_SUMMARY_CHAT_OPEN_AI_AZURE_OPENAI_API_VERSION"]
    openai.api_key = os.environ["MULTI_ARTICLE_SUMMARY_CHAT_OPEN_AI_AZURE_OPENAI_API_KEY"]
    multi_article_summary_chat_open_ai_azure_openai_engine = os.environ["MULTI_ARTICLE_SUMMARY_CHAT_OPEN_AI_AZURE_ENGINE"]
except Exception as e:
    logger.error(f"Environment variable not found: {e}")


def get_table_intro(paragraph, project_id, article_count):
    try:
        response = openai.ChatCompletion.create(
            engine=multi_article_summary_chat_open_ai_azure_openai_engine,
            messages=[
                {"role": "system", "content": "Take following data and write common objective for " + str(article_count) + """ articles in one sentence  with common disease and intervention mentioned in all studies given below.Make sure to include number of studies given in common objective sentence.Make sure not to mention author and publication year in common objective sentence. example given below:/n/n
            example-1: Table 1 presents a summary of 16 clinical studies and 1 pooled analysis of 7 clinical studies that support the use of miconazole nitrate cream in the treatment of skin infections due to dermatophytes or yeasts and other fungi.
            example-2: Table 1 presents a summary of 8 clinical studies that support the indication and dosage and administration of miconazole nitrate and hydrocortisone for the treatment of skin infections due to dermatophytes or Candida species.\n\nData elements for all studies given below\n\n""" + paragraph}],
            temperature=0,
            max_tokens=200
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        if "exceeded token rate limit" in str(e):
            logger.error(f"Token Limit Reached. Try again after some time : {e} For project id : {project_id}")
            raise HTTPException(status_code=500, detail=f"Token Limit Reached. Try again after some time : {e}")
        logger.error(f"Exception in get_table_intro : {e}, for project id : {project_id}")
        raise HTTPException(status_code=500, detail=f"Exception in get_table_intro : {e}")


def generate_table_title(prompt, data, project_id):
    try:
        response = openai.ChatCompletion.create(
            engine=multi_article_summary_chat_open_ai_azure_openai_engine,
            messages=[
                {"role": "user", "content": prompt + "\n\n" + data}],
            temperature=0,
            max_tokens=200,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        if "exceeded token rate limit" in str(e):
            logger.error(f"Token Limit Reached. Try again after some time : {e} For project id : {project_id}")
            raise HTTPException(status_code=500, detail=f"Token Limit Reached. Try again after some time : {e}")
        logger.error(f"Exception in get_table_title : {e}, for project id : {project_id}")
        raise HTTPException(status_code=500, detail=f"Exception in get_table_title : {e}")


def generate_table_summary_intro_and_title(project_id):
    logger.info(f"Table summary intro and title generation started for project id : {project_id}")
    es = connect_elasticsearch()
    try:
        search_body = {
            "query": {
                "bool": {
                    "must":
                        {
                        "match": {
                            "project_id": project_id
                            }
                        }
                    }
                }
            }
        response = es.search(index="multi_article_summary", body=search_body)

        article_id_list = response["hits"]["hits"][0]["_source"]["article_ids"]
        multi_article_summary_id = response["hits"]["hits"][0]["_id"]
    except Exception as e:
        logger.error(f"Exception in fetch article ids from ES {e}, for project id : {project_id}")
        raise HTTPException(status_code=500, detail=f"Exception in fetch article ids from ES {e}, for project id : {project_id}")

    extracted_data_dict_list = []
    for article_id in article_id_list:
        try:
            search_body = {
                "query": {
                    "match": {
                        "article_id": article_id
                        }
                    }
                }
            response = es.search(index="article_extraction_fields", body=search_body)
            ml_extracted_fields = response["hits"]["hits"][0]["_source"]["ml_extracted_fields"]
            extracted_data_dict_list.append(ml_extracted_fields)
        except Exception as e:
            logger.error(f"Exception in fetch single article summary from ES {e}, for article id : {article_id} in project id : {project_id}")
            raise HTTPException(status_code=500, detail=f"Exception in fetch single article summary from ES {e}, for article id : {article_id} in project id : {project_id}")

    background_section_string_list = []
    for ml_extracted_fields_dict in extracted_data_dict_list:
        background_list = []
        white_listed_keys = [
            es_field_mapping["aim"],
            es_field_mapping["diagnosis_of_interest"],
            es_field_mapping["diagnostic_criteria"],
            es_field_mapping["disease_condition"],
            es_field_mapping["country"],
            es_field_mapping["treatment"],
            es_field_mapping["control"],
        ]
        not_predict_list = ["", "none", "None", "unknown", "not found", "Not found", "not provided", "not mentioned", "N/A", "null", "nonamed"]
        es_sentence_data_field_list = [es_field_mapping["aim"]]
        
        es_primary_author = ml_extracted_fields_dict[es_field_mapping["primary_author"]]
        primary_author = json.loads(es_primary_author).get("sentence", '') if es_primary_author != "" and es_primary_author.find("{") != -1 else ''

        es_publication_year = ml_extracted_fields_dict[es_field_mapping["publication_year"]]
        publication_year = json.loads(es_publication_year).get("sentence", '') if es_publication_year != "" and es_publication_year.find("{") != -1 else ''

        if primary_author != '':
            background_list.append(f"{es_field_mapping['primary_author']} : {primary_author}")
        if publication_year != '':
            background_list.append(f"{es_field_mapping['publication_year']} : {publication_year}")

        for key in ml_extracted_fields_dict.keys():
            if key in white_listed_keys and ml_extracted_fields_dict[key] != "" and  ml_extracted_fields_dict[key].find("{") != -1:
                if key in es_sentence_data_field_list:
                    sentence = json.loads(ml_extracted_fields_dict[key])['sentence']
                    background_list.append(f"{key} : {sentence}")
                else:
                    ml_extracted_field_dict_list = json.loads(ml_extracted_fields_dict[key])
                    for ml_extracted_field_dict in ml_extracted_field_dict_list["element_list"]:
                        if ml_extracted_field_dict not in not_predict_list:
                            sentence = ml_extracted_field_dict_list['sentence'][ml_extracted_field_dict]
                            background_list.append(f"{key} : {ml_extracted_field_dict}")
                            background_list.append(f"sentence : {sentence}")

        background_section_string_list.append(', '.join([str(element) for element in background_list]))

    background_section_string = '\n'.join(background_section_string_list)

    intro_string = get_table_intro(background_section_string, project_id, len(article_id_list))
    intro_string = intro_string + " Each study is further described in detail below."

    first_prompt = """You are a Medical Article Research analyst.
            Please summarize a single title for the common intervention, control, disease condition and the main cause for the diseases from the articles. Important: This should be a brief consize title. Please include the cause of disease. Do not add numbers, newline, and symbols"""
    intervention = generate_table_title(first_prompt, background_section_string, project_id)
    intervention = re.sub(r'\d+\.', '', intervention).replace('\n', '').replace('"', '')

    table_title = f"Summary of Clinical Studies Supporting the Use of {intervention}."
    try:
        es.update(
                index = "multi_article_summary", 
                id = multi_article_summary_id, 
                body = {
                    "doc" : {
                        "table_description" : intro_string,
                        "table_title" : table_title,
                        }
                    }
                )
    except Exception as e:
        logger.error(f"Exception in update table summary intro and title into ES {e}, for project id : {project_id}")
        raise HTTPException(status_code=500, detail=f"Exception in update multi article summary into ES {e}, for project id : {project_id}")
    logger.info(f"Table summary intro and title generation done for project id : {project_id}")
    es.transport.close()
    return project_id
