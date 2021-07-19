import os
import textract
from spacy.pipeline import EntityRuler
from spacy import displacy
import jsonlines
from spacy.lang.en import English
from spacy.tokens import Doc
import spacy
from fastapi import FastAPI, File, UploadFile
from PyPDF2 import PdfFileReader
import json, requests
import urllib.parse

# import gpt_2_simple as gpt2
# import tensorflow as tf
import uvicorn
import gc


app = FastAPI()


@app.get('/')
def get_root():return {'message': 'Welcome to Jobzilla API'}


nlp = spacy.load('en_core_web_sm')

skill_pattern_path = "jz_skill_patterns.jsonl"
with jsonlines.open("jz_skill_patterns.jsonl") as f:
    created_entities = [line['label'].upper() for line in f.iter()]

ruler = EntityRuler(nlp).from_disk(skill_pattern_path)

nlp.add_pipe(ruler, after='parser')

def get_skills(text):
    doc = nlp(text)
    myset = []
    subset = []
    for ent in doc.ents:
        if ent.label_=="SKILL":
            subset.append(ent.text)
    myset.append(subset)
    return subset


def extract_text_from_pdf(file):
    fileReader = PdfFileReader(file)
    page_count = fileReader.getNumPages()
    text = [fileReader.getPage(i).extractText() for i in range(page_count)]
    return str(text).replace("\\n", "")


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    cv_skills_list = get_skills(extract_text_from_pdf(file.file)) 
    cv_skills_list = list(dict.fromkeys(cv_skills_list))
    separator = ', '
    cv_skills = separator.join(cv_skills_list)
    return {'file': file.filename, "skills": cv_skills}


@app.get("/jobsearch/")
async def job_search(title, skills, city):
    title_e = urllib.parse.quote(title)
    skills_e = urllib.parse.quote(skills)
    city_e = urllib.parse.quote(city)
    url = 'https://api.adzuna.com/v1/api/jobs/de/search/10?app_id=b80e80f4&app_key=672a5604a37c08d4f1135673ccb80160&results_per_page=10&what_or={}&title_only={}&where={}&distance=500'.format(skills_e, title_e, city_e)    
    res = requests.get(url)
    data = json.loads(res.content.decode(res.encoding))
    return data


# sess = gpt2.start_tf_sess(threads=1)
# gpt2.load_gpt2(sess)

# generate_count = 0


# @app.post("/coverletter/")
# async def homepage(request):
    
#     params = await request.json()
#     text = gpt2.generate(sess,
#                          length=int(params.get('length', 1023)),
#                          temperature=float(params.get('temperature', 0.7)),
#                          top_k=int(params.get('top_k', 0)),
#                          top_p=float(params.get('top_p', 0)),
#                          prefix=params.get('prefix', '')[:500],
#                          truncate=params.get('truncate', None),
#                          include_prefix=str(params.get(
#                              'include_prefix', True)).lower() == 'true',
#                          return_as_list=True
#                          )[0]

#     generate_count += 1
#     if generate_count == 8:
#         # Reload model to prevent Graph/Session from going OOM
#         tf.reset_default_graph()
#         sess.close()
#         sess = gpt2.start_tf_sess(threads=1)
#         gpt2.load_gpt2(sess)
#         generate_count = 0

#     gc.collect()
#     return {'text': text}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))





