import os

from flask import request, render_template, redirect
from flask_login import login_required, current_user

from core import app, db
from core.models import Target
from core.template import finish_list_template, finish_card_template, chip_error_html


@app.route("/u/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    finished_list = Target.query.filter_by(user_id=current_user.id, status=True).all()

    unfinished_list = Target.query.filter_by(
        user_id=current_user.id, status=False
    ).all()

    finished_list_html = ""
    unfinished_list_html = ""

    finished_list_html = finished_list_html.join(
        [finish_list_template.replace("[[NAME]]", item.name)
        .replace("[[ID]]", str(item.id))
        for item in finished_list]
    )

    unfinished_list_html = unfinished_list_html.join(
        [
            finish_list_template.replace("[[NAME]]", item.name)
            for item in unfinished_list
        ]
    )

    card_list = finished_list + unfinished_list
    card_list_html = ""
    for card in card_list:

        name = card.name
        time = "Undone" if card.finish_time is None else str(card.finish_time)
        warning = str(card.warning)
        icon = "check" if card.status else "check_box_outline_blank"
        disabled = "disabled" if not card.status else ""
        color = "red-700" if card.status else "grey"
        error = "" if not card.error else chip_error_html

        card_list_html += (
            finish_card_template.replace("[[NAME]]", name)
            .replace("[[TIME]]", time)
            .replace("[[WARNING]]", warning)
            .replace("[[ICON]]", icon)
            .replace("[[DISABLED]]", disabled)
            .replace("[[ID]]", str(card.id))
            .replace("[[API_COUNT]]", str(card.api_count))
            .replace("[[COLOR]]", color)
            .replace("[[ERROR]]", error)
        )

    return render_template(
        "dashboard.html",
        msg=request.args.get("msg", ""),
        finished_list_html=finished_list_html,
        unfinished_list_html=unfinished_list_html,
        card_list_html=card_list_html,
    )


@app.route("/u/upload", methods=["GET", "POST"])
@login_required
def upload():

    file = request.files.get("file")
    print(request.form)
    name = request.form.get("name", default=None)
    args = request.form.get("args", default=None)

    # print(name, args)

    if (not file) or (not name):
        return redirect("/u/dashboard?msg=Upload error!")
    file.save(os.path.join(app.root_path, "upload", name + ".exe"))
    

    target = Target(
        name=name,
        user_id=current_user.id,
        status=False,
        args=args,
    )
    db.session.add(target)
    db.session.commit()

    return redirect("/u/dashboard?msg=Upload success!")

@app.route("/u/msg", methods=["GET", "POST"])
@login_required
def msg():

    msg = current_user.msg
    current_user.msg = "None"
    db.session.commit()

    return msg