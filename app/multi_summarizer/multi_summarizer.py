import os, logging, json, re
from fastapi import HTTPException
import concurrent.futures
import openai

from app.multi_summarizer.prompts_and_keys import *
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


count_headers_updated = lambda text: len(re.findall(r'\b([^:]+):', text))

remove_headers_at_first = lambda segment_text: '. '.join([re.sub(r"^\s*[^:]+:\s*", "", line) if i == 0 else line for i, line in enumerate(segment_text.split('. '))])

def get_extracted_data_string(extracted_data_dict_list, key_list_to_parse):
    background_section_string_list = []
    for ml_extracted_fields_dict in extracted_data_dict_list:
        background_list = []
        not_predict_list = ["", "none", "None", "unknown", "not found", "Not found", "not provided", "not mentioned", "N/A", "null", "nonamed"]

        es_primary_author = ml_extracted_fields_dict[es_field_mapping["primary_author"]]
        primary_author = json.loads(es_primary_author).get("sentence", '') if es_primary_author != "" and es_primary_author.find("{") != -1 else ''

        es_publication_year = ml_extracted_fields_dict[es_field_mapping["publication_year"]]
        publication_year = json.loads(es_publication_year).get("sentence", '') if es_publication_year != "" and es_publication_year.find("{") != -1 else ''

        if primary_author != '':
            background_list.append(f"{es_field_mapping['primary_author']} : {primary_author}")
        if publication_year != '':
            background_list.append(f"{es_field_mapping['publication_year']} : {publication_year}")

        for key in ml_extracted_fields_dict.keys():
            if key in key_list_to_parse and ml_extracted_fields_dict[key] != "" and  ml_extracted_fields_dict[key].find("{") != -1:
                if "element_list" not in ml_extracted_fields_dict[key]:
                    sentence = json.loads(ml_extracted_fields_dict[key])['sentence']
                    background_list.append(f"{key} : {sentence}")
                else:
                    ml_extracted_field_dict_list = json.loads(ml_extracted_fields_dict[key])
                    for ml_extracted_field_dict in ml_extracted_field_dict_list["element_list"]:
                        if ml_extracted_field_dict not in not_predict_list:
                            sentence = ml_extracted_field_dict_list['sentence'][ml_extracted_field_dict]
                            background_list.append(f"{key} : {ml_extracted_field_dict}")
                            background_list.append(f"sentence : {sentence}")
        background_section_string = ', '.join([str(element) for element in background_list])
        if len(background_section_string) > 5:
            background_section_string_list.append(background_section_string)
    return background_section_string_list


def get_articles_chunks(articles_list, n=8):
    if len(articles_list) == 0:
        return []
    elif len(articles_list) > n:
        splitted_list = [articles_list[i:i + n] if i + n <= len(articles_list) else articles_list[i:] for i in range(0, len(articles_list), n)]
        articles_strings = ["\n\n".join(lst) for lst in splitted_list]
    elif n >= len(articles_list):
        articles_strings = ["\n\n".join(articles_list)]
    return articles_strings


def text_generation(prompt, data):
    response = openai.ChatCompletion.create(
        engine=multi_article_summary_chat_open_ai_azure_openai_engine,
        messages=[
            {"role": "user", "content": prompt + "\n\n" + data}
        ],
        temperature=0,
        max_tokens=5000,
    )
    return response["choices"][0]["message"]["content"]


def get_single_prompt_section(extracted_data_dict_list, section_keys, prompts, index):
    if extracted_data_dict_list:
        data = ' '.join(get_extracted_data_string(extracted_data_dict_list, section_keys))
    else:
        data = section_keys
    first_prompt_data = text_generation(prompts[0], data).replace("\n\n"," ").replace("\n", " ").replace("\\","")
    removed_headers_at_first = remove_headers_at_first(first_prompt_data)

    count = count_headers_updated(removed_headers_at_first)
    steps = 3
    while count > 0 and steps > 0:
        get_single_prompt_data = get_single_prompt_section([], data, prompts, data)["data"]
        removed_headers_at_first = remove_headers_at_first(get_single_prompt_data)
        count = count_headers_updated(removed_headers_at_first)
        steps -= 1

    return {"data": removed_headers_at_first, "id": index}


def get_two_prompt_section(extracted_data_dict_list, section_keys, prompts, special_prompt, index):
    prompt_data = []
    data = get_extracted_data_string(extracted_data_dict_list, section_keys)
    article_strings = get_articles_chunks(data, n=5)
    if article_strings:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = [executor.submit(text_generation, *[prompts[0], chunk]) for chunk in article_strings]

            for future in concurrent.futures.as_completed(results):
                output = future.result()
                if future in results:
                    prompt_data.append(output)

    first_prompt_data = "\n".join(prompt_data)
    second_prompt_data = text_generation(prompts[1], first_prompt_data).replace("\n\n"," ").replace("\\","").replace("\n"," ")
    removed_headers_at_first = remove_headers_at_first(second_prompt_data)

    count = count_headers_updated(removed_headers_at_first)
    steps = 3
    while count > 0 and steps > 0:
        get_special_prompt_data = text_generation(special_prompt, removed_headers_at_first)
        removed_headers_at_first = remove_headers_at_first(get_special_prompt_data)
        count = count_headers_updated(removed_headers_at_first)
        steps -= 1

    return {"data": removed_headers_at_first, "id": index}


def get_three_prompt_section(extracted_data_dict_list, section_keys, prompts, special_prompt, index):
    prompt_data = []
    data = get_extracted_data_string(extracted_data_dict_list, section_keys)
    article_strings = get_articles_chunks(data, n=5)
    if article_strings:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = [executor.submit(text_generation, *[prompts[0], chunk]) for chunk in article_strings]

            for future in concurrent.futures.as_completed(results):
                output = future.result()
                if future in results:
                    prompt_data.append(output)

    first_prompt_data = "\n".join(prompt_data)
    second_prompt_data = text_generation(prompts[1], first_prompt_data).replace("\n\n"," ").replace("\\","").replace("\n", " ")
    third_prompt_data = text_generation(prompts[2], second_prompt_data).replace("\n\n"," ").replace("\n", " ")
    removed_headers_at_first = remove_headers_at_first(third_prompt_data)

    count = count_headers_updated(removed_headers_at_first)
    steps = 3
    while count > 0 and steps > 0:
        special_prompt_data = text_generation(special_prompt, removed_headers_at_first)
        removed_headers_at_first = remove_headers_at_first(special_prompt_data)
        count = count_headers_updated(removed_headers_at_first)
        steps -= 1

    return {"data": removed_headers_at_first, "id": index}


def generate_multi_summarizer(project_id):
    logger.info(f"Multi article summary generation started for project id : {project_id}")
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
        logger.error(f"Exception in get article ids from ES {e}, for project id : {project_id}")
        raise HTTPException(status_code=500, detail=f"Exception in get article ids from ES {e}, for project id : {project_id}")

    if not article_id_list:
        logger.error(f"Empty article_ids list in ES multi_article_summary index.")
        raise HTTPException(status_code=500, detail=f"Empty article_ids list in ES multi_article_summary index.")

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
            logger.error(f"Exception in get single article summary from ES {e}, for article id : {article_id} in project id : {project_id}")
            raise HTTPException(status_code=500, detail=f"Exception in get single article summary from ES {e}, for article id : {article_id} in project id : {project_id}")

    thread_task_list = [
        (get_single_prompt_section, [extracted_data_dict_list, objective_section_keys, objective_section_prompts, 0]),
        (get_three_prompt_section, [extracted_data_dict_list, intervention_section_keys, intervention_section_prompts, intervention_section_special_prompt, 1]),
        (get_three_prompt_section, [extracted_data_dict_list, efficacy_section_keys, efficacy_section_prompts, efficacy_section_special_prompt, 2]),
        (get_two_prompt_section, [extracted_data_dict_list, safety_section_keys, safety_section_prompts, safety_section_special_prompt, 3]),
        (get_single_prompt_section, [extracted_data_dict_list, conclusion_section_keys, conclusion_section_prompts, 4]),
    ]

    summary_list = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            results = [executor.submit(task, *args) for task, args in thread_task_list]
            for future in concurrent.futures.as_completed(results):
                output = future.result()
                if future in results:
                    summary_list.append(output)
    except Exception as e:
            if "exceeded token rate limit" in str(e):
                logger.error(f"Token Limit Reached. Try again after some time : {e} For project id : {project_id}")
                raise HTTPException(status_code=500, detail=f"Token Limit Reached. Try again after some time : {e}")
            logger.error(f"Exception in concurrent get_section : {e}, for project id : {project_id}")
            raise HTTPException(status_code=500, detail=f"Exception in concurrent get_section : {e}")                    

    multi_article_summary_string = '\n'.join([summary["data"] for summary in sorted(summary_list, key=lambda x: x['id'])])

    try:
        es.update(
                index = "multi_article_summary", 
                id = multi_article_summary_id, 
                body = {
                    "doc" : {
                        "summary" : multi_article_summary_string,
                        }
                    }
                )
    except Exception as e:
        logger.error(f"Exception in update multi article summary into ES {e}, for project id : {project_id}")
        raise HTTPException(status_code=500, detail=f"Exception in update multi article summary into ES {e}, for project id : {project_id}")
    logger.info(f"Multi article summary generation done for project id : {project_id}")
    es.transport.close()
    return project_id
