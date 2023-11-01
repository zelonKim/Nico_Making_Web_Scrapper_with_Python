
from requests import get
from bs4 import BeautifulSoup

def get_page_count(keyword):
  base_url = "https://kr.indeed.com/jobs?q="
  response = get(f"{base_url}{keyword}")

  if response.status_code != 200:
    print("Can not request")
  else:
    soup = BeautifulSoup(response.text, "html.parser")
    pagination = soup.find("ul", class_="pagination-list")

    if pagination == None:
      return 1

    pages = pagination.find_all("li", recursive=False)
    count = len(pages)
    if count >= 5:
      return 5
    else:
      return count



def extract_indeed_jobs(keyword):
  pages = get_page_count(keyword)
  print("Found", pages, "pages")
  results = []

  for page in range(pages):
    base_url = "https://kr.indeed.com/jobs"
    final_url = f"{base_url}?q={keyword}&start={page*10}"
    print("Requesting", final_url)

    response = get(final_url)

    if response.status_code != 200:
      print("Can not request")
    else:
      soup = BeautifulSoup(response.text, "html.parser")
      job_list = soup.find("ul", class_="jobsearch-ResultsList")
      jobs = job_list.find_all('li', recursive=False)  # ' recursive=False' finds the 'tag' by one depth
      for job in jobs:
        zone = job.find("div", class_="mosaic-zone")  # if .find() did not find anything, returns 'None' type
        if zone == None:
          anchor = job.select_one("h2 a")  # finds 'a' tag in 'h2' tag
          title = anchor['aria-label']
          link = anchor['href']
          company = job.find("span", class_="companyName")
          location = job.find("div", class_="companyLocation")
          job_data = {
              'link': f"https://kr.indeed.com{link}",
              'company': company.string.replace(",", ""),
              'location': location.string.replace(",", ""),
              'position': title.replace(",", "")
          }
          results.append(job_data)
  return results
   
