# ai- model for st21-jobzilla

##  Cover letter generation

## 1. model:simple without labels and metadata

Based on gpt-2-simple library from Max Woolf - https://minimaxir.com/2019/09/howto-gpt2/

### Test finetuning - execution:

1. Upload notebook file to Google colab
2. Set the runtime tipe as GPU 
3. Execute all cells from top to bottom


## 2. model: with Title labels 
Model was trained based on cover letters text bodies with job titles and skills as aditional metadata.


##  3. model: KWs (skills) - extraction
Based on SpyCy NEP with custom keywords matching (json - file with skills - attached). 
Extraction algorithm was used for job and cv analysis, as well for similarity matching. 


## API
Models were containerized (Docker), set up as API (FastAPI) and deployed on Google Cloud Plattform.
Endpoints:  https://jzl-search-api-v7otpcjevq-lz.a.run.app/docs

Cover letter generation: https://jzl-api-v7otpcjevq-lz.a.run.app/?length=500&temperature=0.7&prefix=

(For customized letter creation as prefx varibale should be used "~Job Titke~skill1, skill2, skill3")
