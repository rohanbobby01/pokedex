import pandas as pd


def data_clean(df):
    return df[["Main Option", "Enquiry", "Fares", "Resolved", "Others", "Res_Amenities_s",
               "Res_lost_found", "SUG & COMPLNT", "Suggestion", "Complaint", "Res_sug_complai",
               "Suggestion on fares", "Complaint on Fare", "Fare_suggestion/Complaint",
               "Survey", "Res_Station/train"]].copy().fillna("")


def preprocess(df):
    a = list(map(lambda x: "complaint_on_fare" if len(x) != 0 else "", df['Complaint on Fare']))
    df['Complaint on Fare'] = pd.Series([""] + a)
    a = list(map(lambda x: "suggestion_on_fare" if len(x) != 0 else "", df['Suggestion on fares']))
    df['Suggestion on fares'] = pd.Series([""] + a)

    final = []
    for j in range(len(df)):
        arr = []
        for item in df.iloc[j]:
            if item == "":
                continue
            arr.append(item.split(","))

        arr1 = []
        for i in range(5):
            sentence = ''
            for item in arr:
                if i > len(item) - 1:
                    continue
                if item[i] != "Others" and item[i] != "Go back to Main Menu" and item[
                    i] != "Go back to previous menu" and item[i] != "Yes" and item[i] != "No":
                    sentence += item[i] + " "
            if len(sentence) != 0:
                arr1.append(sentence.strip())
        final.append(arr1)

    return final


def classifier(arr, df):
  classified = []
  for i, item in enumerate(arr):
    item = "".join(item)
    if "complaint_on_fare" in item or df.iloc[i]["Fares - Email id"] == "Complaint":
      classified.append("Complaint")
    
    elif "suggestion_on_fare" in item:
      classified.append("Request")
    
    elif "Complaint" in item or "Compliant" in item:
      classified.append("Complaint")
      
    elif "Suggestion" in item or "Lost & Found" in item: #We can change the "lost and found" if we don't need it.
        classified.append("Request")
      
    elif "Celebration on Wheels" in item:
      classified.append("Compliment")
    else:   
      classified.append("Custom")

  return classified


def show_5(df,l,df_preprocess,preprocessed=False):
  length = len(df)
  if (l-1)*5 >= length:
    return "Out of Bounce"
  
  if (l-1)*5 + 4 >= length:
    if preprocessed == False:
      return df[(l-1)*5:length]
    else:
      return [df_preprocess[i-1] for i in df.index[(l-1)*5:length].to_list()]
  else:
    if preprocessed == False:
      return df[(l-1)*5:(l-1)*5+5]
    else:
      return [df_preprocess[i-1] for i in df.index[(l-1)*5:(l-1)*5+5].to_list()]
