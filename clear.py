import missingno as msno
msno.bar(datatmsp.sample(len(datatmsp)), figsize=(10, 4))


half_count = len(datatmsp)/2
datatmsp = datatmsp.dropna(thresh=half_count, axis=1)

datatmsp = datatmsp.drop_duplicates()
