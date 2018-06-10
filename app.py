from flask import Flask, render_template, jsonify, request
from web_setting import DB_URL, DB_USER, DB_PASSWORD, DB_SCHEMA
import pymysql
import simplejson as json
from math import sqrt, pow

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('location.html')

@app.route('/predict')
def predict():

    return render_template('predict.html')

#x,y좌표를 입력받아 필요한 데이터를 가져오고, 처리하는 부분
@app.route('/predictProcess')
def predict_procee():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    #explanation data
    nearest_dong = ""
    nearest_station = ""

    #regression variables
    average_age = 999999
    work_density = 999999
    station_distance = 999999
    rental_distance = 999999

    get_dong_info_sql = "select average_age, work_density, dong_name, sqrt(pow(lat-"+lat+",2)+pow(lng-"+lng+",2)) 'distance' from dong_info order by distance limit 1"
    get_station_distance_sql = "select *, sqrt(pow(stat_lat-"+lat+",2)+pow(stat_lng-"+lng+",2)) 'distance' from station_info order by distance limit 1"
    get_rent_distance_sql = "select *, sqrt(pow(rent_lat-"+lat+",2)+pow(rent_lng-"+lng+",2)) 'distance' from rental_center_info order by distance limit 1"
    
    result = ""
    try:
        conn = pymysql.connect(host=DB_URL,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             db=DB_SCHEMA,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        with conn.cursor() as cursor:
            cursor.execute(get_dong_info_sql)
            result = cursor.fetchall()
            average_age = result[0]["average_age"]
            work_density = result[0]["work_density"]
            nearest_dong = result[0]["dong_name"]
            cursor.execute(get_station_distance_sql)
            result = cursor.fetchall()
            station_distance = result[0]["distance"]
            nearest_station = result[0]["station_name"]
            cursor.execute(get_rent_distance_sql)
            result = cursor.fetchall()
            rental_distance = result[0]["distance"]

    finally:
        conn.close()
    
    predicted_value = 147.780739-0.026132*float(rental_distance*1000)-1.099247*float(average_age) -  0.024414*sqrt(work_density) - 0.99423*station_distance*1000
    
    result_data = {"average_age":average_age, "work_density":work_density, "station_distance":station_distance, "rental_distance":rental_distance, 
    "nearest_dong":nearest_dong, "nearest_station":nearest_station, "predicted_value":round(predicted_value*predicted_value)}
    
    return jsonify(result_data)

@app.route('/latlng')
def get_latlng():
     #get all latlng
     #later, using parameter to get few locations
    result = ""
    try:
        conn = pymysql.connect(host=DB_URL,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             db=DB_SCHEMA,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        with conn.cursor() as cursor:
            sql = 'SELECT office_name, latitude, longitude FROM rental_office_info'
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        conn.close()
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)