
import requests
from flask import Flask, render_template, request, session, redirect, url_for,jsonify
import numpy as np
import mysql.connector
import joblib
from datetime import date
app = Flask(__name__)
app.secret_key = 'mysecretkey'
# MySQL database connection
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="root",
	database="mydb"
)
model = joblib.load('model/model.pkl')
# Flask route for the registration form
@app.route('/home')
def home1():
    return render_template('admin_dash.html')
@app.route('/predict', methods=['POST'])
def predict():
    crops = {
    'RICE': 'Rice is a staple crop known for its versatility and high nutritional value. With an average yield of around 4 to 6 tons per hectare, it is a highly productive crop that adapts well to different climates and soil conditions.',
    'MAIZE': 'Maize, also known as corn, is a widely cultivated crop used for various purposes including human consumption, animal feed, and industrial applications. With an average yield of 4 to 10 tons per hectare, maize is known for its resilience and adaptability to diverse environments.',
    'CHICKPEA': 'Chickpea, a legume crop, is valued for its protein-rich seeds and is commonly used in various culinary dishes. It typically yields around 1 to 2 tons per hectare, depending on the variety and growing conditions.',
    'KIDNEY BEANS': 'Kidney beans are a popular choice in many cuisines for their distinctive shape and flavor. With an average yield of 1 to 1.5 tons per hectare, they are known for their protein content and dietary fiber.',
    'PIGEON BEANS': 'Pigeon beans, also known as red gram or tur, are an important pulse crop in many regions. They yield around 1.5 to 2 tons per hectare and are known for their rich protein content and ability to fix nitrogen in the soil.',
    'MOTH BEANS': 'Moth beans are drought-tolerant legumes that are highly valued for their nutritional benefits. With an average yield of 0.5 to 1 ton per hectare, they are an important crop in arid and semi-arid regions.',
    'MUNG BEANS': 'Mung beans are small, green legumes commonly used in Asian cuisine. They yield around 0.8 to 1.5 tons per hectare and are known for their high protein content and versatility in cooking.',
    'BLACK GRAM': 'Black gram, also known as urad bean, is a popular pulse crop with a rich flavor. It typically yields around 0.8 to 1.5 tons per hectare and is known for its high protein and iron content.',
    'LENTIL': 'Lentils are highly nutritious pulses that come in various colors and sizes. They yield around 0.8 to 1.5 tons per hectare and are valued for their protein content, dietary fiber, and versatility in cooking.',
    'POMEGRANATE': 'Pomegranate is a fruit-bearing shrub known for its juicy arils and antioxidant properties. The average yield per hectare can range from 8 to 15 tons, depending on the variety and growing conditions.',
    'BANANA': 'Banana is a popular fruit crop with a high demand worldwide. Depending on the variety, it can yield around 30 to 50 tons per hectare, making it one of the most productive fruit crops.',
    'MANGO': 'Mango is a tropical fruit tree renowned for its delicious taste and aroma. With an average yield of 10 to 20 tons per hectare, it is a highly valued fruit crop in many countries.',
    'GRAPES': 'Grapes are widely cultivated for fresh consumption, winemaking, and raisin production. The average yield per hectare can range from 6 to 20 tons, depending on the variety and growing conditions.',
    'WATERMELON': 'Watermelon is a refreshing fruit that is popular during the summer season. With an average yield of 30 to 40 tons per hectare, it is a productive crop valued for its sweet and juicy flesh.',
    'MUSKMELON': 'Muskmelon, also known as cantaloupe, is a sweet and aromatic fruit crop. It typically yields around 20 to 30 tons per hectare and is favored for its distinct flavor and high water content.',
    'APPLE': 'Apples are widely grown and consumed fruits with numerous varieties. The average yield per hectare can range from 15 to 40 tons, depending on the variety and growing conditions.',
    'ORANGE': 'Oranges are citrus fruits known for their refreshing taste and high vitamin C content. With an average yield of 10 to 25 tons per hectare, they are a popular fruit crop in many regions.',
    'PAPAYA': 'Papaya is a tropical fruit tree known for its sweet and vibrant-colored flesh. It typically yields around 20 to 30 tons per hectare and is valued for its high nutritional value and medicinal properties.',
    'COCONUT': 'Coconuts are widely cultivated for their versatile uses, including coconut water, oil, and flesh. Depending on the variety and growing conditions, coconut trees can yield around 40 to 80 coconuts per tree per year.',
    'COTTON': 'Cotton is an important fiber crop used in the textile industry. The average yield per hectare can range from 1.5 to 3 tons of raw cotton, depending on the variety and cultivation practices.',
    'JUTE': 'Jute is a natural fiber crop used for making various products like sacks, ropes, and textiles. It typically yields around 2 to 3 tons of fiber per hectare and is known for its strength and durability.',
    'COFFEE': 'Coffee is a popular beverage crop cultivated for its aromatic beans. The average yield per hectare can range from 1 to 3 tons, depending on the variety and growing conditions. It is valued for its distinct flavor and stimulating properties.'
}
    data = request.get_json()
    n = data['n']
    p = data['p']
    k = data['k']
    t = data['t']
    h = data['h']
    ph =data['ph']
    rf =data['rf']
    i1 = np.array([[n,p,k,t,h,ph,rf]])
    print(i1)
    res = model.predict(i1)[0]
    crop_name = res
    user_id = data['u']
    recommendation_date = date.today()
    cursor = mydb.cursor()
    sql = "INSERT INTO recommendations (crop_name, user_id, recommendation_date) VALUES (%s, %s, %s)"
    values = (crop_name, user_id, recommendation_date)
    cursor.execute(sql, values)
    res = get_crop_details(crop_name)
    print("this is the place**********")
    print(res)
    if(crop_name=='kidneybeans'):
         res['URL']='https://samsgardenstore.com/wp-content/uploads/2023/04/WhatsApp-Image-2022-07-06-at-7.05.22-PM.jpeg'
    res['Crop_details'] = crops[res['CropName'].upper()]
    result={'image':res['URL'],'Crop':crop_name,'details':res['Crop_details']}
    mydb.commit()
    cursor.close()
    print(res)
    return jsonify(result)
@app.route('/crop_form',methods=['post'])
def redir():
      user_id1 = request.form['user_id']
      return render_template('crop_form.html',user_id = user_id1)
@app.route("/past-recommendations")
def get_past_recommendations():
    try:
        user = session.get('user')
        user_id = user[0]
        print(user_id)
        # Connect t0o the database
        cursor = mydb.cursor()
       
        # Fetch past recommendations from the database
        query = "SELECT recommendation_id, crop_name, recommendation_date FROM recommendations where user_id = %s"%user_id
        
        cursor.execute(query)
        past_recommendations = cursor.fetchall()

        # Format the past recommendations data
        recommendations_data = [
            {
                "recommendation_id": recommendation[0],
                "crop_name": recommendation[1],
                "date": recommendation[2],
            }
            for recommendation in past_recommendations
        ]

        return jsonify(recommendations_data)

    except Exception as e:
        print("Error fetching past recommendations:", e)

    finally:
        # Close the database connection
        if cursor:
            cursor.close()
@app.route("/user-recommendations")
def get_user_recommendations():
    cursor = mydb.cursor()
    try:
        # Con
        # Fetch past recommendations from the database
        query = "SELECT * FROM recommendations "
        cursor.execute(query)
        past_recommendations = cursor.fetchall()

        # Format the past recommendations data
        recommendations_data = [
            {
                "user_id" : recommendation[1],
                "recommendation_id": recommendation[0],
                "crop_name": recommendation[2],
                "date": recommendation[3],
            }
            for recommendation in past_recommendations
        ]

        return jsonify(recommendations_data)

    except Exception as e:
        print("Error fetching past recommendations:", e)

    finally:
        # Close the database connection
        if cursor:
            cursor.close()
               
@app.route('/')
def page():
	return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		# Get form data
		name = request.form['name']
		user_id = request.form['user_id']
		password = request.form['password']
		# Insert data into MySQL database
		mycursor = mydb.cursor()
		sql = "INSERT INTO users (name, user_id, password,date) VALUES (%s, %s, %s,%s)"
		val = (name, user_id, password,date.today())
		try:
			mycursor.execute(sql, val)
			mydb.commit()
		
		except:
			return render_template("register.html")
		# Return success message
		return render_template('login.html')
		
	# Return registration form
@app.route('/ad_login')
def ad_login():
    return render_template('admin_login.html')
@app.route('/login1')
def render_login():
    return render_template('login.html')
@app.route('/u_register')
def reg():
      return render_template('register.html')
@app.route('/user_render')
def user_render():
    cursor = mydb.cursor()
    query = """
            SELECT u.user_id, u.name, COUNT(r.user_id) AS num_recommendations
            FROM users AS u
            LEFT JOIN recommendations AS r ON u.user_id = r.user_id
            GROUP BY u.user_id, u.name
            """
    cursor.execute(query)
    users = cursor.fetchall()
  #  users = jsonify(users)
    return render_template('users.html',users=users)
@app.route('/admin_login', methods=['POST'])
def admin_login():
    data = get_graph_data()
    data1 = get_recdata()
    data = {'data':data}
    try:
        if(session['username']):
            return render_template('admin_dash.html',data=data,data1=data1)
    except:
        username = request.form['username']
        password = request.form['password']
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='mydb'
        )
    
    
        cursor = db.cursor()
        query = "SELECT * FROM admin_users WHERE username = %s AND pass = %s"
        values = (username, password)
        cursor.execute(query, values)
        user = cursor.fetchone()
        # close database connection
        cursor.close()
        db.close()
        if user is not None:
            # store user_id in session
            session['username'] = username
            # redirect to dashboard
            return render_template('admin_dash.html',data=data,data1=data1)
        # return redirect('admin_dash.html')
        else:
            # if user does not exist, show error message
            return render_template('admin_login.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        if session['user']:
            return render_template('dashboard.html',user=session['user'])
    except:
         
        user_id = request.form['user_id']
        password = request.form['password']

        # connect to MySQL database
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
         database='mydb'
        )
        cursor = db.cursor()

        # retrieve user data from MySQL database
        query = "SELECT * FROM users WHERE user_id = %s AND password = %s"
        values = (user_id, password)
        cursor.execute(query, values)
        user = cursor.fetchone()    
        # close database connection
        cursor.close()
       # db.close()

        # check if user exists in database
        if user is not None:
            # store user_id in session
            session['user'] = user
            # redirect to dashboard
            return render_template('dashboard.html',user=user)
        else:
            # if user does not exist, show error message
            return render_template('login.html')

@app.route('/delete-users',methods= ['post'])
def del_user():
    selected_users = request.form.getlist('selectedUsers')

    # Connect to the database
    cursor = mydb.cursor()
    print(selected_users)
    # Delete selected users from the database
    if selected_users:
        selected_users_str = ','.join(selected_users)
        delete_query = "DELETE FROM users WHERE user_id IN ({})".format(selected_users_str)
        cursor.execute(delete_query)

    # Fetch the remaining users from the database
    cursor = mydb.cursor()
    query = """
            SELECT u.user_id, u.name, COUNT(r.user_id) AS num_recommendations
            FROM users AS u
            LEFT JOIN recommendations AS r ON u.user_id = r.user_id
            GROUP BY u.user_id, u.name
            """
    cursor.execute(query)
    users = cursor.fetchall()
    # Commit the changes and close the database connection
    mydb.commit()
    cursor.close()
    return render_template("users.html",users=users)

    #cursor = mydb.cursor()
    
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    
    # Redirect the user to the login page
    return redirect('/')

@app.route('/crop_details')
def get_crop_details(crop_name):
    # Set your Trefle API token
    print(crop_name)
    api_token = 'P-siRAfbU6fS_vHgM07pj2dmx158DGtYxM1Bh5JZb1A'
    base_url = "https://trefle.io/api/v1/plants/search"
    params = {
        'token': api_token,
        'q': crop_name  # Query for crop name
    }
    
    # Make the request to the Trefle API
    
    # API endpoint for plant search
   # endpoint = f"https://trefle.io/api/v1/plants/search?token={api_token}&q={crop_name}"

    try:
        # Send GET request to the API
       # response = requests.get(endpoint)
        response = requests.get(base_url, params=params)
        print(response)
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Extract crop details from the response
            if data['data']:
                crop = data['data'][0]  # Assuming the first result is the desired crop
            #    crop_name = crop['common_name']
                family = crop['family']
                scientific_name = crop['scientific_name']
                image_url = crop['image_url']
                
                id = crop['id']
                # Extract any other desired details from the crop object
                print(id)
                # Return the crop details
                return {
                    'CropName': crop_name,
                    'Family': family,
                    'Scientific Name': scientific_name,
                    'URL'   : image_url,
                    
                    # Add more fields as needed
                }
            else:
                return {'error': 'Crop not found'}
        else:
            return {'error': 'Request failed'}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
@app.route('/users-data')
def get_graph_data():
    # Connect to the database
    cursor = mydb.cursor()
    # Retrieve data for number of users over time
    users_query = "SELECT date, COUNT(*) FROM users GROUP BY date"
    cursor.execute(users_query)
    users_data = cursor.fetchall()
    # Retrieve data for number of recommendations over time
  #  recommendations_query = "SELECT recommendation_date, COUNT(*) FROM recommendation GROUP BY recommendation_date"
  #  cursor.execute(recommendations_query)
#    recommendations_data = cursor.fetchall()
    # Close the database connection
    cursor.close()
    # Format the data for the graph
    formatted_users_data = [{'date': str(date), 'numUsers': count} for date, count in users_data]
    #formatted_recommendations_data = [{'date': str(date), 'count': count} for date, count in recommendations_data]
    # Return the data as JSON response
    #return jsonify({'usersData': formatted_users_data, 'recommendationsData': formatted_recommendations_data})
    print(formatted_users_data)
    return jsonify(formatted_users_data)
@app.route('/rec-data')
def get_recdata():
    cursor = mydb.cursor()
    recommendations_query = "SELECT recommendation_date, COUNT(*) FROM recommendations GROUP BY recommendation_date"
    cursor.execute(recommendations_query)
    recommendations_data = cursor.fetchall()
    formatted_recommendations_data = [{'date': str(date), 'count': count} for date, count in recommendations_data]
    return jsonify(formatted_recommendations_data)
@app.route('/rec')
def get_rec():
    cursor = mydb.cursor()
    query = "SELECT recommendation_id, crop_name,user_id, recommendation_date FROM recommendations"
    cursor.execute(query)
    past_recommendations = cursor.fetchall()
    return render_template('recommendation.html',recommendation=past_recommendations)
@app.route('/show_users',methods=['POST'])
def show_users1():
    user_id = request.form['user_id']
    cursor = mydb.cursor()
       
        # Fetch past recommendations from the database
    query = "SELECT recommendation_id, crop_name, recommendation_date FROM recommendations where user_id = %s"%user_id
    cursor.execute(query)
    data = cursor.fetchall()
       # Format the past recommendations data
    return render_template('user_render.html',recommendations_data = data)

if __name__ == '__main__':
	app.run(debug=True)