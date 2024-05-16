from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os
import pandas as pd
from final_insta_post_scrape_comment import scraping_comments_insta_post

import pandas as pd
from final_insta_post_scrape_comment import scraping_comments_insta_post
from four import make_the_four
from server_info import send_server


app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",
    'http://127.0.0.1:5501',
    'http://127.0.0.1:5502',
    'http://127.0.0.1:5500',
    

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


#uvicorn main:app --reload
#python -m uvicorn os_scarper_fastapi:app --reload
class Scraping_URL_Page(BaseModel):
    url: str
    




@app.post("/scarper/")
async def predict_diabetes(data: Scraping_URL_Page):
    try:
        print(type(data))
        url = data.url
       

        print("Data before ETL:", url)
        print("_________")

        scraping_df,list_post_info = scraping_comments_insta_post(url)
        df_posts,df_comments,df_users,df_freq = make_the_four(scraping_df,list_post_info)
        df_users.drop_duplicates(inplace=True)
        send_server(df_posts,df_users,df_comments,df_freq)


        positive = float("{:.2f}".format(list(scraping_df["Predict"]).count(1) / len(scraping_df)))

        negative = float("{:.2f}".format(list(scraping_df["Predict"]).count(0) / len(scraping_df)))




        print("_________")
        print(scraping_df)
        
  

        return {"scraping_json": "http://127.0.0.1:8000/test_insta.csv" , "positive":positive , "negative":negative}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.get("/test_insta.csv")
async def get_csv_file():
    file_path = "test_insta.csv"

    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/csv")
    else:
        raise HTTPException(status_code=404, detail="CSV file not found")