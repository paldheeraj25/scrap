import pandas as pd
import os
import requests
# load the csv in the folder
df_original = pd.read_csv('puma-shoe-collection.csv')
df = df_original.copy()

for index, row in df.iterrows():

    # create the directory
    try:
        # Create target Directory
        os.mkdir('./puma/'+row['shoe'])
        print("Directory ", './puma/'+row['shoe'],  " Created ")
    except FileExistsError:
        print("Directory ", './puma/' +
              row['shoe'],  " already exists***********")

    # save the images in the directory
    img_index = 0
    for url in df.loc[index, 'pic_1':]:

        if not pd.isna(url):
            # change image size to 256 by 256
            url = url.replace("128/128", "256/256")
            # downloading the image
            img_data = requests.get(url).content
            with open(os.path.join('./puma', row['shoe'], str(index)+'-'+str(img_index)+'.jpg'), 'wb') as handler:
                # save the image in the corresponsing directory
                handler.write(img_data)

        img_index += 1
