from app.utils.es_utils import *

objective_section_prompts = ["""Take the following data,Write common objective and motive of all studies given in a verbatim paragraph not more than 3 sentences alone and  wherever "Several studies","In a series of studies conducted" phrases will be added, replace those with alternative phrases of your choice.Make sure not to include author and publication year details.Make sure not to include headers,groups,number lists in the texts will be generated."""]

objective_section_keys = [
    es_field_mapping["aim"],
    es_field_mapping["diagnosis_of_interest"],
    es_field_mapping["diagnostic_criteria"],
    es_field_mapping["disease_condition"],
    es_field_mapping["treatment"],
]

intervention_section_prompts = ["""Take the following data and write down an brief segment related to study design,treatment,dose,dosage,dose form,mode of administration for all studies with author and publication year.Must not include findings of study.Must include author and publication year of all studies.Mention if unable to get data from study with Author and Publication Year.Data elements for number of studies given below""","""Take the following data and create paragraph by concatenate them with proper author and publication year.Its Mandatory to be brief as much as possible not to miss any informations and should be in Verbatim while concatenate.Must include segment of all studies with author and publication year.Must preserve study design while concatenating.Make sure not to give introduction sentence,conclusion sentence,summary sentence while concatenation.Make sure not to include any headers and groups with or without colon and semicolon in paragraph.Make sure not to add any number listings in paragraph.In the paragraph wherever "Multiple studies","Several studies","In a series of studies conducted" phrases will be presented, remove them.""","""Remake the data such a way more analytic,explorative and comparisons between them but preserve all minute details. Make sure no data leakage.Make sure to keep proper author and publication year details as how it was(Author et el (Year)) in output data.Make sure not to give introduction sentence,conclusion sentence,summary sentence while recreating.Make sure no headers, no groups,no number listing in output data."""]

intervention_section_keys = [
    es_field_mapping["study_design"],
    es_field_mapping["randomization_method"],
    es_field_mapping["control"],
    es_field_mapping["blinding"],
    es_field_mapping["age"],
    es_field_mapping["sex"],
    es_field_mapping["population"],
    es_field_mapping["enrolled"],
    es_field_mapping["dose"],
    es_field_mapping["dosage_form"],
    es_field_mapping["dose_frequency"],
    es_field_mapping["mode_of_administration"],
    es_field_mapping["treatment"],
    es_field_mapping["treatment_duration"],
    # es_field_mapping["exposures"],
]

intervention_section_special_prompt = "Take the following data and write a summary in paragraph with proper author and publication year.Make sure to keep proper author and publication year details as how it was(Author et el (Year)) in output data.Highly important to make sure not to give introduction sentence,conclusion sentence,summary sentence while recreating.Highly important to make sure not to include headers, groups and number listing in output data.Highly important to give output data in paragraph only"

efficacy_section_prompts = ["""Take following data and write down brief segment related subject analyzed,cure rate,efficacy results alone for all studies given with author and publication year.Must include author and publication year of all studies.Data elements for all studies given below.""", """Take the following data and create paragraph by concatenate them with proper author and publication year.Its Mandatory to be brief as much as possible not to miss any informations such as aubjects analyzed,cure rate and should be in Verbatim while concatenate.Must include segment of all studies with author and publication year.Make sure not to give introduction sentence,conclusion sentence,summary sentence while concatenation.Make sure not to include any headers and groups with or without colon and semicolon in paragraph.Make sure not to add any number listings in paragraph.In the paragraph wherever "Multiple studies","Several studies","In a series of studies conducted" phrases will be presented, remove them.""","""Take the following data and create paragraph by concatenate them with proper author and publication year.Its Mandatory to be brief as much as possible not to miss any informations and should be in Verbatim while concatenate.Must include segment of all studies with author and publication year.Make sure not to give introduction sentence,conclusion sentence,summary sentence while concatenation.Make sure not to include any headers and groups with or without colon and semicolon in paragraph.Make sure not to add any number listings in paragraph.In the paragraph wherever "Multiple studies","Several studies","In a series of studies conducted" phrases will be presented, remove them.""","""Remake the data such a way more analytic,explorative and comparisons between them but preserve all minute details. Make sure no data leakage.Make sure to keep proper author and publication year details as how it was(Author et el (Year)) in output data.Make sure not to give introduction sentence,conclusion sentence,summary sentence while recreating.Make sure no headers, no groups,no number listing in output data."""]

efficacy_section_keys = [
    es_field_mapping["analyzed_efficacy"],
    es_field_mapping["efficacy_endpoints"],
    es_field_mapping["efficacy_results"],
    es_field_mapping["by_treatment"],
    # es_field_mapping["outcomes"],
]

efficacy_section_special_prompt = "Take the following data and write a summary in paragraph with proper author and publication year.Make sure to keep proper author and publication year details as how it was(Author et el (Year)) in output data.Highly important to make sure not to give introduction sentence,conclusion sentence,summary sentence while recreating.Highly important to make sure not to include headers, groups and number listing in output data.Highly important to give output data in paragraph only"

safety_section_prompts = ["""Take the following data and write down segment related to safety results and adverse events reported alone for all studies given with proper author and publication year.Must include author and publication year of all studies.Mention if unable to get data from study with Author and Publication Year.Data elements for number of studies given below""", """Take the following data, Group the data into number of studies reporting adverse events with proper author and publication year.Generate factual verbatim paragraph on the data grouped with proper author and publication.Must include author and publication year of all studies in summary.Make sure to add number of adverse events if availbale.Make sure not to give introduction sentence,conclusion sentence,summary sentence in paragraph.Make sure not to include any headers and groups with or without colon and semicolon in a paragraph.Make sure not to add any number listings in a paragraph.In the Summary wherever "Multiple studies","Several studies","In a series of studies conducted" phrases will be presented,remove them."""]

safety_section_keys = [
    es_field_mapping["analyzed_safety"],
    es_field_mapping["safety_endpoints"],
    es_field_mapping["safety_results"],
]

safety_section_special_prompt = "Take the following data and write a summary in paragraph with proper author and publication year.Make sure to keep proper author and publication year details as how it was(Author et el (Year)) in output data.Highly important to make sure not to give introduction sentence,conclusion sentence,summary sentence while recreating.Highly important to make sure not to include headers, groups and number listing in output data.Highly important to give output data in paragraph only"

conclusion_section_prompts = ["""Write down comprehensive conclusion remarks,common Upsides and shortcomings as well as limitations about all studies given in a paragraph with out author and publication year not more than 6 sentences.Make it high level abstractive but factual also.Make sure not to add suggestions as further research,future work,further studies and recommendations.Make sure not to include headers and groups in paragraph.Data elements related to author/article conclusion for number of studies given below.Wherever in the summary "The Studies" presented must be replaced as "Studies" only"""]

conclusion_section_keys = [
    es_field_mapping["population"],
    es_field_mapping["enrolled"],
    es_field_mapping["analyzed_total"],
    es_field_mapping["analyzed_efficacy"],
    es_field_mapping["efficacy_endpoints"],
    es_field_mapping["efficacy_results"],
    es_field_mapping["analyzed_safety"],
    es_field_mapping["safety_endpoints"],
    es_field_mapping["safety_results"],
    es_field_mapping["by_treatment"],
    es_field_mapping["by_treatment"],
    es_field_mapping["conclusion"],
    # es_field_mapping["outcomes"],
]
