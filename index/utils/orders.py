from index.utils.connect_firebase import db


def change_order_status(array, status_admin):
    # Загрузить все документы из коллекции "users_op"
    users_op_ref = db.collection_group("users_op").stream()
    user_op_data_dict = {}

    # Собираем данные в локальную структуру данных
    for user_op_doc in users_op_ref:
        user_op_data = user_op_doc.to_dict()
        barcode = user_op_data.get("barcode")
        if barcode:
            user_op_data_dict[barcode] = {"user_doc_id": user_op_doc.reference.parent.parent.id, "user_op_doc_ref": user_op_doc.reference}
    filtered_array = []
    # Обновляем статусы в базе данных Firebase и в локальной структуре данных
    for track_id in array:
        try:
            track_id = int(track_id)
        except:
            track_id = str(track_id)
        track_id = str(track_id)
        if track_id in user_op_data_dict:
            print("FOUND TRACK ID", track_id)
            op_data = {"op_check": False, "op_created": False, "op_stock": False, "op_otw": False, "op_kz": False, "op_received": False, "status_admin": status_admin}
            if status_admin == "На складе в Китае":
                op_data["op_stock"] = True
            elif status_admin == "В пути":
                op_data["op_otw"] = True
            elif status_admin == "В пункте выдачи":
                op_data["op_kz"] = True
            else:
                pass
            user_op_data_dict[track_id]["user_op_doc_ref"].set(op_data, merge=True)
            del user_op_data_dict[track_id]
        else:
            filtered_array.append(track_id)
    print(filtered_array)
    return filtered_array

