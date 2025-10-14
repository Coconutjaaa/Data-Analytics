import pandas as pd
import networkx as nx

sum_sheet = 'sum_data.xlsx'
df = pd.read_excel(sum_sheet, header=0)

print("Data loaded successfully")

subject_codes = df.columns.tolist()
print(f"Number of subjects: {len(subject_codes)}")

subjects_dict = {}

subject_codes = df.columns.tolist()
print(subject_codes)
for subject in subject_codes:
    students = df[subject].dropna().astype(str).str.strip().tolist()
    subjects_dict[subject] = students

print(len(subjects_dict.keys()))

G = nx.Graph()

# Add subjects as nodes
for subject in subjects_dict.keys():
    G.add_node(subject)

# Add edges between subjects that share students
for subj1 in subjects_dict:
    for subj2 in subjects_dict:
        if subj1 != subj2 and set(subjects_dict[subj1]) & set(subjects_dict[subj2])!=set():  # Check if they share students
            # '&' is the set intersection operator, so it returns the students that are common to both subjects
            G.add_edge(subj1, subj2)

# Use graph coloring to find a valid schedule
coloring = nx.coloring.greedy_color(G, strategy="largest_first")  # Assign time slots (largest first is used to assign from the largest subgraph -> subjects that share the same student)


schedule = {}
for subject, time_slot in coloring.items():
    if time_slot not in schedule:
        schedule[time_slot] = []
    schedule[time_slot].append(subject)

print(schedule)
print(type(schedule[11]))
check_unique = {}
for i in [618432, 618445]:
    for subj in subjects_dict.keys():
        if set(subjects_dict[i])&set(subjects_dict[subj])==set():
            if i not in check_unique:
                check_unique[i] = []
            check_unique[i].append(subj)

print("Subject that can take with time slot 11,12")
for sub in check_unique.keys():
    print(f"subject = {sub}, can go with...")
    print(check_unique[sub])

df = pd.DataFrame.from_dict(check_unique, orient='index')
df = df.transpose()  # Adjust format for Excel

# Save as an Excel file
df.to_excel("check_unique.xlsx", index=False)

for time in schedule.keys():
    print(f"time series = {time}")
    for subj in schedule[time]:
        print(f"subject id = {subj} -> no. of student = {len(subjects_dict[subj])}")

# write to excel
output_file = "schedule_result.xlsx"
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    row_offset = 0  # keep track of where to write next table
    
    for time in schedule.keys():
        # Prepare data for this time series
        data = []
        for subj in schedule[time]:
            data.append({
                "subject id": subj,
                "no. of student": len(subjects_dict[subj])
            })
        
        # Create dataframe for this time series
        df = pd.DataFrame(data)
        
        # Write the "time series" title
        worksheet = writer.book.add_worksheet(f"time_{time}")
        worksheet.write(0, 0, f"time series {time}")
        
        # Write dataframe starting from row 1
        df.to_excel(writer, sheet_name=f"time_{time}", startrow=1, index=False)


df = pd.DataFrame.from_dict(schedule, orient='index')
df = df.transpose()  # Adjust format for Excel

# Save as an Excel file
df.to_excel("scheduledata2.xlsx", index=False)

# check
flag = 0
for time in schedule.keys():
    for s1 in schedule[time]:
        for s2 in schedule[time]:
            if s1!=s2:
                if (set(subjects_dict[s1]) & set(subjects_dict[s2]))==set():
                    pass
                else:
                    flag = 1 
if flag==0:
    print("ok")
else:
    print("fail")
