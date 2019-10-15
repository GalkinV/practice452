from flask import Flask
from flask import render_template
from flask import request
from flask import session
from datetime import timedelta
from pyproj import Geod
from osgeo import ogr


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/calc', methods=['GET', 'POST'])
def parse_request():
    # Чтение входных параметров
    wktP1 = request.args.get('param1')
    wktP2 = request.args.get('param2')
    pointNum = request.args.get('param3')
    point1 = ogr.CreateGeometryFromWkt(wktP1)
    point2 = ogr.CreateGeometryFromWkt(wktP2)
    # print ("%d,%d" % (point1.GetX(), point1.GetY()))

    # Вычисление координат для формирования ортодромии
    geoid = Geod(ellps="WGS84")
    extra_points = geoid.npts(point1.GetX(), point1.GetY(), point2.GetX(), point2.GetY(),  int(pointNum))

    # Формирование геометрии в формате ogr
    line = ogr.Geometry(ogr.wkbLineString)
    for lng, lat in extra_points:
        line.AddPoint(lng, lat)

    # Счетчик вызова функции (визитов) в сессии
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # чтение и обновление данных сессии
    else:
        session['visits'] = 1  # настройка данных сессии
    print(session['visits'])

    # Возвращаем Geo json
    return line.ExportToJson()

if __name__ == '__main__':
    app.run()

# Устанавливем время сохранения данных сессии (5 секунд)
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=5)


# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'