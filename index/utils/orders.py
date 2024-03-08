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
        track_id = str(track_id)
        if track_id in user_op_data_dict:
            user_op_data_dict[track_id]["user_op_doc_ref"].set({"status_admin": status_admin}, merge=True)
            print(track_id)
            del user_op_data_dict[track_id]
        else:
            filtered_array.append(track_id)
    print(filtered_array)
    return filtered_array

