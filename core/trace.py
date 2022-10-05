import json

from flask import jsonify, request, abort

from core import app, db
from core.models import Target

@app.route("/t", methods=["GET"])
def trace():
    
    info_dict = request.args

    id = info_dict.get("id", None).split("@")[-1].replace(".exe", "")
    print(id)
    task = Target.query.filter_by(id=id).first()
    if task == None:
        abort(404)

    if task.assigned != 2:
        abort(403)

    print(task.assigned)
    # if task.id != id:
    #    print("No such task.")
    #    return jsonify({"status": False, "msg": "No such task."})
    
    # 需要针对不同的api进行少量的适配
    
    # 这里需要读取该task，即target的info（存储时应为str，读取时应为dict）（用json转）
    old_info_obj = task.load_info()
    if old_info_obj == None:
        old_info_obj = {}
    # 加入新调用的win32api，然后再存储回去（需要对象再转字符串，同样用json转）
    # json 结构

    task.api_count  = task.api_count + 1

    new_api_hook = {
        str(task.api_count): info_dict
    }

    # 注意在合并前需要将更改的换行符处理掉
    old_info_obj.update(new_api_hook)

    print(old_info_obj)
    print(new_api_hook)

    warning = info_dict.get("warning", None)
    if warning != None:
        task.warning = task.warning + 1

    task.info = json.dumps(old_info_obj).replace("@", "/")
    db.session.commit()

    return jsonify({"msg": True})