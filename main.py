"""
websites = [
  "google.com",
  "airbnb.com",
  "twitter.com",
  "facebook.com",
  "tiktok.com"
]

for site in websites:
  print("This is", site)
"""

##########################

""" 
from requests import get

websites = (
  "google.com",
  "airbnb.com",
  "https://twitter.com",
  "facebook.com",
  "https://tiktok.com"
)

results = {}

for site in websites:
  if not site.startswith("https://"):
    site = f"https://{site}"
  response = get(site)
  if response.status_code == 200:
    results[site] = "OK"
  else:
    results[site] = "FAILED"


print(results) 
 """

############################


""" 
from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs

jobs = extract_wwr_jobs("python")

print(jobs) 
"""


############################

"""
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

keyword = input("What do you want to search for?")

indeed = extract_indeed_jobs(keyword)
wwr = extract_wwr_jobs(keyword)
jobs = indeed + wwr 

save_to_file(keyword, jobs) 
"""


############################


from flask import Flask, render_template, request, redirect, send_file
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

app = Flask("JobScrapper")

db={
    
}

@app.route("/") # If you enter '/' URL,  Executes the decorated function   and   Shows the returned value on Screen 
def home():
    return render_template("home.html", name="seongjin") 
          
@app.route("/search")
def search():
    # print(request.args) # ImmutableMultiDict([('keyword', 'python')])
    keyword = request.args.get("keyword")
    if keyword == None:
       return redirect("/")   
    
    if keyword in db:
        jobs = db[keyword]
    else:
      indeed = extract_indeed_jobs(keyword)
      wwr = extract_wwr_jobs(keyword)
      jobs = indeed + wwr
      db[keyword] = jobs

    return render_template("search.html", keyword=keyword, jobs=jobs) # render_template("파일명", 변수명=값): In 'templates' folder, Renders the file of which name is '파일명' and Sends '변수명=값' to '파일명'



@app.route("/export")
def export():
  keyword = request.args.get("keyword")
  
  if keyword == None:
    return redirect("/")
  
  if keyword not in db:
     return redirect(f"/search?keyword={keyword}")
  
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}.csv", as_attachment=True) # send_file("파일명", 옵션)   # 'as_attachment=True' triggers download



app.run("0.0.0.0") # run the Flask Server