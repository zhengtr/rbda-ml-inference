import pandas as pd

ques_header = ["Source", "YearOfCreation", "Id", "Score", "Body"]
ans_header = ["Source", "YearOfCreation", "ParentId", "Score", "Body"]

# df_ques = pd.read_csv("questions_part-r-00000.csv", names=ans_header)
# df_ques["unique_id"] = df_ques.index
# df_ques["unique_id"] = df_ques["unique_id"].apply(str)
# df_ques["Source"] = df_ques[["Source", "unique_id"]].apply("_".join, axis=1) 
# df_ques = df_ques.drop("unique_id", axis=1)
# df_ques.to_csv("answers_id_part-r-00000", index=False, header=False)

df_ans = pd.read_csv("answer_part-r-00000.csv", names=ques_header)
df_ans["unique_id"] = df_ans.index
df_ans["unique_id"] = df_ans["unique_id"].apply(str)
df_ans["Source"] = df_ans[["Source", "unique_id"]].apply("_".join, axis=1) 
df_ans = df_ans.drop("unique_id", axis=1)
df_ans.to_csv("answer_id_part-r-00000", index=False, header=False)