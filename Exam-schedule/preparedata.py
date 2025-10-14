import pandas as pd
import networkx as nx

file_path = "data_exam.xlsx"
xls = pd.ExcelFile(file_path)
data_sheet = pd.read_excel(xls, sheet_name="Sheet3")

print("Data loaded successfully")

subject_codes = data_sheet.columns.tolist()
print(f"Number of subjects: {len(subject_codes)}")

# -------------------------
# Fixed subjects
# -------------------------
fixed_subject = {
    511104: {"Day": 6, "Slot": 1},#saturn
    513257: {"Day": 6, "Slot": 2},
    511105: {"Day": 6, "Slot": 2},
    511115: {"Day": 6, "Slot": 2},
    511117: {"Day": 6, "Slot": 2},
    511106: {"Day": 7, "Slot": 1},#sun
    513231: {"Day": 7, "Slot": 2},
    616311: {"Day": 8, "Slot": 1},#mon
    616333: {"Day": 8, "Slot": 1},
    616432: {"Day": 8, "Slot": 1},
    616221: {"Day": 8, "Slot": 2},
    616471: {"Day": 8, "Slot": 2},
    20101: {"Day": 9, "Slot": 1},#tue
    616201: {"Day": 9, "Slot": 1},
    616442: {"Day": 9, "Slot": 1},
    84101: {"Day": 9, "Slot": 2},
    115: {"Day": 9, "Slot": 2},
    518102: {"Day": 9, "Slot": 2},
    616312: {"Day": 9, "Slot": 2},
    514101: {"Day": 10, "Slot": 1},#wed
    616391: {"Day": 10, "Slot": 1},
    616401: {"Day": 10, "Slot": 1},
    514107: {"Day": 10, "Slot": 2},
    616331: {"Day": 10, "Slot": 2},
    61633202: {"Day": 10, "Slot": 2},
    20102: {"Day": 11, "Slot": 1},#thur
    514102: {"Day": 11, "Slot": 1},
    514110: {"Day": 11, "Slot": 1},
    514112: {"Day": 11, "Slot": 1},
    616211: {"Day": 11, "Slot": 1},
    513100: {"Day": 11, "Slot": 2},
    513110: {"Day": 11, "Slot": 2},
    616321: {"Day": 11, "Slot": 2},
    61643101: {"Day": 11, "Slot": 2},
    513101: {"Day": 12, "Slot": 1},#fri
    514114: {"Day": 12, "Slot": 1},
    616381: {"Day": 12, "Slot": 1},
    616411: {"Day": 12, "Slot": 1},
    61633201: {"Day": 12, "Slot": 2},
    61643102: {"Day": 12, "Slot": 2},
    513103: {"Day": 13, "Slot": 1},#sat
    513341: {"Day": 13, "Slot": 1},
    513105: {"Day": 13, "Slot": 2},
    513255: {"Day": 13, "Slot": 2},
    511103: {"Day": 14, "Slot": 1},#sun
    518101: {"Day": 14, "Slot": 1},
    513233: {"Day": 14, "Slot": 2}
}

def classify_subjects_by_time(fixed_subject):
    time_groups = {}
    for subject_id, schedule in fixed_subject.items():
        key = (schedule["Day"], schedule["Slot"])
        time_groups.setdefault(key, []).append(subject_id)
    sorted_keys = sorted(time_groups.keys())
    return [time_groups[key] for key in sorted_keys]

classified_subjects = classify_subjects_by_time(fixed_subject)
print("\nClassified fixed subjects:")
# for i, group in enumerate(classified_subjects):
#     print(f"Time slot {i}: {group}")

subjects_dict = {}
for subject in subject_codes:
    students = data_sheet[subject].dropna().astype(str).str.strip().tolist()
    subjects_dict[subject] = students

print(len(subjects_dict.keys()))

merge_fix = {}
# print(classified_subjects)
# print(len(classified_subjects))

for i in range(len(classified_subjects)):
    print(f"Time slot {i}: {classified_subjects[i]}")
    sum = 0
    for fs in classified_subjects[i]:
        sum += len(subjects_dict[fs])
    print(f"total student = {sum}")
    for tsubj in classified_subjects[i]:
        if i not in merge_fix.keys():
            merge_fix[i] = []
        merge_fix[i].extend(subjects_dict[tsubj])

print("merge subject length")
print(len(merge_fix.keys()))

# merge fix subj to excel
df_fix = pd.DataFrame.from_dict(merge_fix, orient='index')
df_fix = df_fix.transpose()  # Adjust format for Excel

# Save as an Excel file
df_fix.to_excel("mergefix.xlsx", index=False)

not_fix = subject_codes - fixed_subject.keys()

# after merge fix subject
subjects_dict_notfix = {}
for subject in not_fix:
    students = data_sheet[subject].dropna().astype(str).str.strip().tolist()
    subjects_dict_notfix[subject] = students

print("not fix subject length")
print(len(subjects_dict_notfix.keys()))

df_notfix = pd.DataFrame.from_dict(subjects_dict_notfix, orient='index')
df_notfix = df_notfix.transpose()
df_notfix.to_excel("notfix.xlsx", index=False)

if set(merge_fix.keys())&set(subjects_dict_notfix.keys()) == set():
    print("True")

