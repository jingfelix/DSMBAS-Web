import os
import datetime
import json

from flask import (
    request,
    render_template,
    redirect,
    jsonify,
    abort,
    send_from_directory,
)
from flask_login import login_required, current_user

from core import app, db
from core.models import Target, User
from core.template import finish_list_template, api_list_template, arg_list_template, api_dict, icon_html


@app.route("/e/gettask", methods=["GET", "POST"])
def gettask():

    key = request.form.get("key", None)
    if key == None or not key:
        return jsonify({"status": False, "msg": "wrong key"})

    unfinished = Target.query.filter_by(assigned=0).first()
    if unfinished == None:
        return jsonify({"status": False, "msg": "no task"})
    unfinished.assigned = 1
    db.session.commit()
    return jsonify({"status": True, "msg": "Task acquired.", "task": unfinished.id})


@app.route("/e/download", methods=["GET", "POST"])
def download():

    task_id = request.form.get("task", None)
    print(task_id)
    running_task = Target.query.filter_by(id=task_id).first()
    print(running_task.assigned)

    if running_task == None:
        abort(404)
    # 需要判断是否已经分配
    running_task.assigned = 2
    db.session.commit()

    print(os.path.join(app.root_path, "upload"))
    print(app.config["UPLOAD_FOLDER"] + "\\" + running_task.name + ".exe")

    return send_from_directory(
        directory="upload", path=running_task.name + ".exe", as_attachment=True
    )


@app.route("/e/report", methods=["GET", "POST"])
@login_required
def report():

    id = request.args.get("id", None)
    if id == None:
        redirect("/u/dashboard?msg=Wrong Access")

    task = Target.query.filter_by(id=id).first()

    print(task == None)
    if (task == None) or (task.user_id != current_user.id):
        return redirect("/u/dashboard?msg=Wrong Access")

    if task.assigned == 3:

        finished_list = Target.query.filter_by(
            user_id=current_user.id, status=True
        ).all()

        unfinished_list = Target.query.filter_by(
            user_id=current_user.id, status=False
        ).all()

        finished_list_html = ""
        unfinished_list_html = ""

        finished_list_html = finished_list_html.join(
            [
                finish_list_template.replace("[[NAME]]", item.name).replace(
                    "[[ID]]", str(item.id)
                )
                for item in finished_list
            ]
        )

        unfinished_list_html = unfinished_list_html.join(
            [
                finish_list_template.replace("[[NAME]]", item.name)
                for item in unfinished_list
            ]
        )

        # 将api list按照键值的数值排序
        api_list = sorted(json.loads(task.info).items(), key=lambda x: int(x[0]))
        print(api_list)
        args_list = []

        api_list_html = ""
        args_list_html = ""

        for api in api_list:
            args_list_html = ""

            num = api[0]
            details = api[1]

            api_name = details["api"]

            args_list = [
                [key, details.get(key, None)]
                for key in details.keys()
                if key != "api" and key != "id"
            ]

            for arg in args_list:
                args_list_html += arg_list_template.replace("[[KEY]]", arg[0]).replace(
                    "[[VALUE]]", arg[1]
                )

            if details.get("warning", None) != None:
                warning = api_dict.get(api_name, "default").get("warning", None)
                w_icon = '<i class="mdui-icon material-icons mdui-text-color-red-500">warning</i>'
            else:
                warning = ""
                w_icon = '<i class="mdui-icon material-icons mdui-text-color-green-500">check</i>'

            a_icon_dict = api_dict.get(api_name, None)
            a_icon = a_icon_dict.get("icon", "") if a_icon_dict != None else api_dict.get("default", "").get("icon", "")
            a_icon_html = icon_html.replace("[[ICON]]", a_icon)

            api_list_html += (
                api_list_template.replace("[[NUM]]", num)
                .replace("[[API]]", api_name)
                .replace("[[ARGS]]", args_list_html)
                .replace("[[WARNING]]", warning)
                .replace("[[W_ICON]]", w_icon)
                .replace("[[A_ICON]]", a_icon_html)
            )

        return render_template(
            "report.html",
            finished_list_html=finished_list_html,
            unfinished_list_html=unfinished_list_html,
            name=task.name,
            api_list_html=api_list_html,
        )
    else:
        return redirect("/u/dashboard?msg=Task Unfinished")


@app.route("/e/endtask", methods=["GET", "POST"])
def endtask():

    task_id = request.args.get("id", None)
    error = request.args.get("error", None)
    # 分离出name
    if task_id is None:
        abort(404)
    # print(name)
    task_id = task_id.split("@")[-1].replace(".exe", "")
    print(task_id)

    task = Target.query.filter_by(id=task_id).first()
    if task == None:
        abort(404)

    if task.assigned != 2:
        abort(403)

    print("id:", task.id)
    print("task:", task.name)

    task.error = 1 if error != None else 0

    task.assigned = 3
    task.finish_time = datetime.datetime.now()
    task.status = True

    user = User.query.filter_by(id=task.user_id).first()

    user.msg = "Task Done! Refresh to view"

    db.session.commit()

    return jsonify({"status": True, "msg": "Task ended."})


@app.route("/e/errortask", methods=["GET", "POST"])
def errortask():
    id = request.args.get("id", None)
    if id == None:
        abort(404)
    task = Target.query.filter_by(id=id).first()
    if task == None:
        abort(404)

    task.assigned = 0
    db.session.commit()
    return jsonify({"status": True, "msg": "Task restarted."})
