from flask import Flask,render_template,request
import pickle
import numpy as np

popular_books = pickle.load(open('popular.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))
Books = pickle.load(open('Books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))


app = Flask(__name__)

@app.route('/') 
def home():
    return render_template('home.html')

@app.route('/categories')
def categories():
    return render_template('categories.html',
                           book_name = list(popular_books['Book-Title'].values),
                           author=list(popular_books['Book-Author'].values),
                           image=list(popular_books['Image-URL-M'].values),
                           votes=list(popular_books['num_ratings'].values),
                           rating=list(popular_books['avg_rating'].astype(int).values)
                           )

@app.route('/recommendations',methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        index = np.where(df.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:10]

        data = []
        for i in similar_items:
            item = []
            temp_df = Books[Books['Book-Title'] == df.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        # print(data)

        return render_template('recommendations.html',data=data)

    else:
        return render_template('recommendations.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')  


@app.route('/contactus', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        username = request.form['name']
        useremail = request.form['email']
        usermessage = request.form['message']

        user_recieved_data = {
            "username": username,
            "useremail": useremail,
            "usermessage": usermessage
        }

        userData = f"{user_recieved_data}\n"
        with open("userData.txt", 'a') as file:
            file.write(userData)

        return render_template('contact.html', message="Your message has been sent!", data=user_recieved_data)

    return render_template('contact.html')

  

if __name__ == '__main__':
    app.run(debug=True)