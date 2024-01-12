from flask import Flask,render_template,request,jsonify
from bs4 import BeautifulSoup
import googleapiclient.discovery
import requests
import pandas as pd

app=Flask(__name__)

@app.route('/')
def show_data():
    return render_template('index.html')

@app.route('/result_data',methods=['POST','GET'])

def result():
    data=request.form.get('data').replace(" ", "+")
    platform=request.form.get('platform')

    if platform=='Youtube':
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey='AIzaSyBlalJonyRyl9vLwr5x_TjJY3IVRbCa76o')
        search_response = youtube.search().list(part="id",type='video',order="relevance",q=data,maxResults=50,fields="items(id(videoId))").execute()
        id=[]
        d=[]
        v=[]
        v=[]
        l=[]
        di=[]
        f=[]
        c=[]
        for item in search_response['items']:
            # Getting the id
            vidId = item['id']['videoId']
    # Getting stats of the video
            r = youtube.videos().list(
            part="statistics,contentDetails",
            id=vidId,
            fields="items(statistics," + \
                "contentDetails(duration))").execute()
        
            try:
                duration = r['items'][0]['contentDetails']['duration']
                views = r['items'][0]['statistics']['viewCount']
                likes = r['items'][0]['statistics']['likeCount']
                favorites = r['items'][0]['statistics']['favoriteCount']
                comments = r['items'][0]['statistics']['commentCount']
                id.append(vidId)
                d.append(duration)
                v.append(views)
                l.append(likes)
                f.append(favorites)
                c.append(comments)
            except:
                pass
        video_info = {'id':id,'duration':d,'views':v,'likes':l,'favorites':f,'comments':c}

        df = pd.DataFrame(video_info)
        df.to_csv('youtubevideo.csv', mode='a', index=False, header=False)
        return video_info
    elif platform=='Amazon':
        url=f"https://www.amazon.in/s?k={data}&crid=23NJ97MO2QCLZ&sprefix=oppo%2Caps%2C328&ref=nb_sb_noss_1"
        headers=({'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36','Accept-Language':'en-US,en;q=0.5'})
        webpage=requests.get(url,headers=headers)
        soup=BeautifulSoup(webpage.content,'html.parser')
        link=soup.find_all("a",attrs={"class":'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        product_link=[]
        c=0
        for i in link:
            if c<=15:
                l1=i.get('href')
                links="https://amazon.in"+l1
                product_link.append(links)
                c=c+1
        title=[]
        price=[]
        link=[]
        rating=[]
        l=len(product_link)
        i=0
        while (i<=l-1):
            new_res=requests.get(product_link[i],headers=headers)
            new_soup=BeautifulSoup(new_res.content,"html.parser")
            title1=new_soup.find("span",attrs={"id":"productTitle"})
            price1=new_soup.find("span",attrs={"class":"a-price-whole"})
            rating1=new_soup.find("span",attrs={"class":"a-size-base a-color-base"})
            if price1==None:
                i=i+1
            else:
                 s=title1.text
                 t=s.strip()
                 title.append(t)
                 link.append(product_link[i])
                 prices=price1.text.strip()
                 ratings=rating1.text.strip()
                 rating.append(ratings)
                 price.append(prices)
                 i=i+1
        data = {'Title': title,'Price': price,'Links': link,'Ratings': rating}
        df = pd.DataFrame(data)
        df.to_csv('amazofile.csv', mode='a', index=False, header=False)
        return data
        
    else:
       url=f"https://www.geeksforgeeks.org/{data}/"
       res=requests.get(url)
       content=BeautifulSoup(res.content,"html.parser")
       contentl=content.find_all("a")
       product_link=[]
       c=0
       for i in contentl:
        if c<=30:
            l1=i.get('href')
            links=l1
            product_link.append(links)
            c=c+1
       l=len(product_link)
       i=1
       course={}
       while i<=l-1:
        new_res=requests.get(product_link[i])
        new_content=BeautifulSoup(new_res.content,"html.parser")
        coursename1=new_content.find("h1",attrs={"class":"courseCard_ctitle__MaKnW"})
        if coursename1==None:
            i=i+1
        else:
            coursename=coursename1.string
            courseinstructor=new_content.find("div",attrs={"class":"courseOverview_container__SgWLp courseOverview_course_overview__UPEU0"}).get_text()
            course[coursename]=courseinstructor
            i=i+1
       return course

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8002)

