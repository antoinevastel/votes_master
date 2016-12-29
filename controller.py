from flask import Flask, request, render_template
import MySQLdb as mdb
import hashlib

app = Flask(__name__)
con = mdb.connect('localhost', 'root', 'bdd', 'votes_master')
cur = con.cursor(mdb.cursors.DictCursor)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/add_poster', methods=['GET', 'POST'])
def add_poster():
    if request.method == 'POST':
        poster_title = request.form["titre_poster"]
        poster_number = request.form["id_poster"]
        poster_description = request.form["description_poster"]
        cur.execute(
            'select * from poster where numero = '+poster_number
        )
        nb_res = len(cur.fetchall())
        if nb_res > 0:
            error = True
        else:
            error = False

        if not error:
            sql = "INSERT INTO poster (numero, titre, description) VALUES (%s, %s, %s)"
            cur.execute(sql, (poster_number, poster_title, poster_description))
            con.commit()

        poster_added = not(error)
    else:
        error = False
        poster_added = False

    cur.execute(
        'select * from poster order by numero'
    )
    posters = cur.fetchall()
    return render_template('add_poster.html', poster_added=poster_added, error=error, posters = posters)


@app.route('/delete_poster/<id>')
def delete_poster(id):
    cur.execute(
        'DELETE from poster where numero = ' + id
    )
    con.commit()
    cur.execute(
        'select * from poster order by numero'
    )
    posters = cur.fetchall()
    return render_template('add_poster.html', poster_added=False, error=False, posters = posters, poster_deleted=True)


@app.route('/add_demo', methods=['GET', 'POST'])
def add_demo():
    if request.method == 'POST':
        demo_title = request.form["titre_demo"]
        demo_number = request.form["id_demo"]
        demo_description = request.form["description_demo"]

        cur.execute(
            'select * from demo where numero = '+demo_number
        )

        nb_res = len(cur.fetchall())

        if nb_res > 0:
            error = True
        else:
            error = False

        if not error:
            sql = "INSERT INTO demo (numero, titre, description) VALUES (%s, %s, %s)"
            cur.execute(sql, (demo_number, demo_title, demo_description))
            con.commit()

        demo_added = not(error)
    else:
        error = False
        demo_added = False

    cur.execute(
        'select * from demo order by numero'
    )

    demos = cur.fetchall()

    return render_template('add_demo.html', demo_added=demo_added, error=error, demos = demos)


@app.route('/delete_demo/<id>')
def delete_demo(id):
    cur.execute(
        'DELETE from demo where numero = ' + id
    )

    con.commit()

    cur.execute(
        'select * from demo order by numero'
    )

    demos = cur.fetchall()
    return render_template('add_demo.html', demo_added=False, error=False, demos = demos, demo_deleted=True)


@app.route('/vote_poster', methods=["GET", "POST"])
def vote_poster():
    #detect if user has already voted

    if request.method == 'GET':
        cur.execute(
            'select * from poster order by numero'
        )
        posters = cur.fetchall()
        return render_template('vote_poster.html', posters= posters)
    else:
        #add http headers
        id_utilisateur = request.form.get('hash')
        numero_poster = request.form.get('poster')
        cookie_user_id = request.form.get("user_id")

        if id_utilisateur == None or numero_poster == None:
            error = True
        else:
            if cookie_user_id != "no_id":
                id_utilisateur = cookie_user_id
            else:
                id_utilisateur += request.headers.get('Accept')
                id_utilisateur += request.headers.get('Accept-Encoding')
                id_utilisateur += request.headers.get('Accept-Language')
                id_utilisateur += request.headers.get('Connection')

                id_utilisateur = hashlib.sha224(id_utilisateur.encode("UTF-8")).hexdigest()

            cur.execute(
                'select * from utilisateur where hash_fp="' + id_utilisateur + '"'
            )

            if len(cur.fetchall()) == 0:
                sql = 'INSERT INTO utilisateur (hash_fp) VALUES ("'+id_utilisateur+'")'
                cur.execute(sql)
                con.commit()

            cur.execute(
                'select * from vote_poster where id_utilisateur ="'+id_utilisateur+'"'
            )

            res = cur.fetchall()
            if len(res) > 0:
                #user has already voted, we update his previous vote
                sql = "UPDATE vote_poster SET numero_poster = %s WHERE id_utilisateur = %s"
                cur.execute(sql, (numero_poster, id_utilisateur))
                con.commit()
            else:
                sql = "INSERT INTO vote_poster (id_utilisateur, numero_poster) VALUES (%s, %s)"
                cur.execute(sql, (id_utilisateur, numero_poster))
                con.commit()

            return id_utilisateur

@app.route('/vote_succeed')
def vote_succeed():
    return render_template('vote_suceed.html')


@app.route('/vote_demo', methods=["GET", "POST"])
def vote_demo():
    if request.method == 'GET':
        cur.execute(
            'select * from demo order by numero'
        )
        demos = cur.fetchall()
        return render_template('vote_demo.html', demos= demos)
    else:
        #add http headers
        id_utilisateur = request.form.get('hash')
        numero_demo = request.form.get('demo')
        cookie_user_id = request.form.get("user_id")

        if id_utilisateur == None or numero_demo == None:
            error = True
        else:
            if cookie_user_id != "no_id":
                id_utilisateur = cookie_user_id
            else:
                id_utilisateur += request.headers.get('Accept')
                id_utilisateur += request.headers.get('Accept-Encoding')
                id_utilisateur += request.headers.get('Accept-Language')
                id_utilisateur += request.headers.get('Connection')

                id_utilisateur = hashlib.sha224(id_utilisateur.encode("UTF-8")).hexdigest()

            cur.execute(
                'select * from utilisateur where hash_fp="' + id_utilisateur + '"'
            )

            if len(cur.fetchall()) == 0:
                sql = 'INSERT INTO utilisateur (hash_fp) VALUES ("'+id_utilisateur+'")'
                cur.execute(sql)
                con.commit()

            cur.execute(
                'select * from vote_demo where id_utilisateur ="'+id_utilisateur+'"'
            )

            res = cur.fetchall()
            if len(res) > 0:
                #user has already voted, we update his previous vote
                sql = "UPDATE vote_demo SET numero_demo = %s WHERE id_utilisateur = %s"
                cur.execute(sql, (numero_demo, id_utilisateur))
                con.commit()
            else:
                sql = "INSERT INTO vote_demo (id_utilisateur, numero_demo) VALUES (%s, %s)"
                cur.execute(sql, (id_utilisateur, numero_demo))
                con.commit()

            return id_utilisateur

@app.route('/ranking')
def ranking():
    cur.execute(
        'select numero, titre, count(*) as nb_votes from demo d JOIN vote_demo vd  ON d.numero = vd.numero_demo GROUP BY numero ORDER BY count(*) desc'
    )

    demos = cur.fetchall()

    cur.execute(
        'select numero, titre, count(*) as nb_votes from poster p JOIN vote_poster vp  ON p.numero = vp.numero_poster GROUP BY numero ORDER BY count(*) desc'
    )

    posters = cur.fetchall()

    return render_template('ranking.html', demos=demos, posters=posters)