from flask import Blueprint, request, jsonify
from .tools import token_to_user, org_schema
from math import ceil
from .postgres import db_close, db_open


bp = Blueprint("org_get", __name__)


@bp.get("/organization/<key>")
def get(key):
    con, cur = db_open()

    cur.execute("""
        SELECT *
        FROM organization
        WHERE slug = %s OR key = %s;
    """, (key, key))
    org = cur.fetchone()

    if not org:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "organization": org_schema(org)
    })


@bp.get("/organizations")
def get_many():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "organization:view" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    order_by = {
        'name (a-z)': 'name',
        'name (z-a)': 'name'
    }

    order_dir = {
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    order = list(order_by.keys())[0]
    status = "live"
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
        FROM organization
        WHERE
            (
                %s = '' OR status = %s
            ) AND (
                %s = ''
                OR CONCAT_WS(', ', key, name, email
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
    orgs = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "organizations": [org_schema(x) for x in orgs],
        "order_by": list(order_by.keys()),
        "_status": ['live', 'draft'],
        "total_page": ceil(orgs[0]["_count"] / page_size) if orgs else 0
    })


@bp.get("/organizations/2")
def get_micro():
    con, cur = db_open()

    cur.execute("SELECT key as value, name as key FROM organization;")
    orgs = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "organizations": orgs
    })
