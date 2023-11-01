def save_to_file(file_name, jobs):
    file = open(f"{file_name}.csv", "w") # "open("파일명","파일모드"): creates a file of which name is 파일명  and  mode is 파일모드"

    file.write("Position,Company,Location,URL\n")

    for job in jobs:
        file.write(f"{job['position']}, {job['company']}, {job['location']}, {job['link']}\n")

    file.close() # a file must be closed in the end