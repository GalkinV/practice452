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
    extra_points = geoid.npts(point1.GetX(), point1.GetY(), point2.GetX(), point2.GetY(),  int(pointNum))


    line = ogr.Geometry(ogr.wkbLineString)
    for lng, lat in extra_points:
        line.AddPoint(lng, lat)

    return line.ExportToJson()

if __name__ == '__main__':
    app.run()
