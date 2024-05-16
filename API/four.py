from pre_class import BuildFreqs,ProcessTweets,ExtractFeatuers
import pandas as pd
import numpy as np
def freqs_all(freqs):


    list_of_pos_neg_total = []

    of = set([i[0] for i in list(freqs)])


    for tup in of:

        list_of_pos_neg_total.append([tup, freqs.get((tup,1.0),0),freqs.get((tup,0.0),0) , freqs.get((tup,1.0),0)+freqs.get((tup,0.0),0)] )


        

    df_of_pos_neg_total = pd.DataFrame(list_of_pos_neg_total, columns = ["word" , "pos_freq" , "neg_freq" , "total_freq"]).sort_values(by="total_freq" , ascending=False).drop_duplicates()
    return df_of_pos_neg_total


def make_the_four(df,l):
    df["User_Comment_Pre"] = ProcessTweets().fit_transform(df["User_Comment"])


    Freqs_Pre = BuildFreqs().fit_transform(df["User_Comment_Pre"],df["Predict"])
    freqs_Pre_table = freqs_all(Freqs_Pre)
    freqs_Pre_table.reset_index(drop="first",inplace=True)
    freqs_Pre_table["post_link"] = [df["post_link"][0]] * len(freqs_Pre_table)
    
    df_freqs_Pre_table = freqs_Pre_table

    

    df_comments = pd.concat([df,pd.DataFrame(np.array(ExtractFeatuers().fit_transform(df["User_Comment_Pre"],Freqs_Pre)), columns=["bias","pos","neg"])],axis= 1).drop(columns=["bias"])

    df_users = df_comments[["User_Name","Profile_Link"]]





    df_comments.drop(columns= ["Profile_Link"],inplace=True)

    df_posts = pd.DataFrame(l,columns = ["post_link","post_owner_name","post_owner_link","post_num_like","post_num_comment","post_datetime"])
    df_comments.columns = ["user_name","user_comment","comment_datetime","comment_pred","post_link","comment_pred_cat","user_comment_pre","comment_pos","comment_neg"]
    df_posts["pos"] = list(df_comments["comment_pred_cat"]).count("Positive") / len(df_comments)
    df_posts["neg"] = list(df_comments["comment_pred_cat"]).count("Negative") / len(df_comments)
    df_users.columns = ["user_name","user_profile_link"]

   

    return df_posts,df_comments,df_users,df_freqs_Pre_table








