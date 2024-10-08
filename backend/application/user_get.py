from flask import Blueprint, request, jsonify
from .tools import token_to_user, user_schema
from math import ceil
from .postgres import db_close, db_open
from .admin import access


bp = Blueprint("user_get", __name__)


@bp.get("/user/<key>")
def get(key):
    con, cur = db_open()

    cur.execute("""
        SELECT *
        FROM "user"
        WHERE slug = %s OR email = %s OR key = %s;
    """, (key, key, key))
    user = cur.fetchone()

    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.get("/users")
def get_many():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "user:view" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    order_by = {
        'name (a-z)': 'firstname',
        'name (z-a)': 'firstname'
    }

    order_dir = {
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    order = list(order_by.keys())[0]
    status = "confirmed"
    search = ""
    page_no = 1
    page_size = 24

    if "status" in request.args:
        status = request.args["status"]
    if "search" in request.args:
        search = request.args["search"].strip()
    if "order" in request.args:
        order = request.args["order"]
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "size" in request.args:
        page_size = int(request.args["size"])

    cur.execute("""
        SELECT
            *,
            COUNT(*) OVER() AS _count
        FROM "user"
        WHERE
            (
                %s = '' OR status = %s
            ) AND (
                %s = ''
                OR CONCAT_WS(', ', key, firstname, lastname, email
                ) ILIKE %s
            )
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        status, status,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "order_by": list(order_by.keys()),
        "_status": ['anonymous', 'confirmed'],
        "total_page": ceil(users[0]["_count"] / page_size) if users else 0
    })


@bp.get("/admin/user")
def get_admins():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "user:edit_access" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    order_by = {
        'name (a-z)': 'firstname',
        'name (z-a)': 'firstname'
    }

    order_dir = {
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    order = list(order_by.keys())[0]
    page_no = 1
    page_size = 24
    search = ":all:all"

    if "order" in request.args:
        order = request.args["order"]
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "size" in request.args:
        page_size = int(request.args["size"])
    if "search" in request.args:
        search = request.args["search"]
    search = search.split(":")
    if len(search) != 3:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid search"
        })
    user_key, _type, _action = search
    user_key = user_key.strip()

    cur.execute("""
        SELECT
            *,
            COUNT(*) OVER() AS _count
        FROM "user"
        WHERE
            array_length(access, 1) IS NOT NULL
            AND status = 'confirmed'
            AND (%s = ''
                OR CONCAT_WS(', ', key, firstname, lastname, email)
                ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING(access, ',')
                ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING(access, ',')
                ILIKE %s)
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        user_key, f"%{user_key}%",
        _type, f"%{_type}:%",
        _action, f"%{_type}:{_action}%",
        page_size, (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    asx = {
        "all": ['all']
    }
    for x in access:
        if x not in asx:
            asx[x] = ["all"]
            for y in access[x]:
                asx[x].append(y[0])

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "access": asx,
        "order_by": list(order_by.keys()),
        "total_page": ceil(users[0]["_count"] / page_size) if users else 0
    })
