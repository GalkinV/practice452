from flask import Flask
from flask import render_template
from flask import request
from pyproj import Geod
from osgeo import ogr


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/calc', methods=['GET', 'POST'])
def parse_request():
    wktP1 = request.args.get('param1')
    wktP2 = request.args.get('param2')
    pointNum = request.args.get('param3')
    point1 = ogr.CreateGeometryFromWkt(wktP1)
    point2 = ogr.CreateGeometryFromWkt(wktP2)

    # print ("%d,%d" % (point1.GetX(), point1.GetY()))
    geoid = Geod(ellps="WGS84")
    extra_points = geoid.npts(point1.GetX(), point1.GetY(), point2.GetX(), point2.GetY(), int(pointNum))
    list_of_lists = [list(elem) for elem in extra_points]
    # К extra_points надо добавить первую и последнюю точки, а то их там нет
    list_of_lists.insert(0, [point1.GetX(), point1.GetY()]);
    list_of_lists.append([point2.GetX(), point2.GetY()]);
    print (list_of_lists)

    return str(list_of_lists)

if __name__ == '__main__':
    app.run()
