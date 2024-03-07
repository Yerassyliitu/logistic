from index.utils.connect_firebase import db


def change_order_status(rows, status_admin, field_to_parse):
    # Загрузить все документы из коллекции "users_op"
    users_op_ref = db.collection_group("users_op").stream()
    user_op_data_dict = {}

    # Собираем данные в локальную структуру данных
    for user_op_doc in users_op_ref:
        user_op_data = user_op_doc.to_dict()
        barcode = user_op_data.get("barcode")
        if barcode:
            user_op_data_dict[barcode] = {"user_doc_id": user_op_doc.reference.parent.parent.id, "user_op_doc_ref": user_op_doc.reference}

    # Обрабатываем данные из rows
    array = []
    for row in rows:
        track_id = row[field_to_parse - 1]
        if track_id and track_id != 'None':
            array.append(track_id)
    filtered_array = []
    # Обновляем статусы в базе данных Firebase и в локальной структуре данных
    for track_id in array:
        if track_id in user_op_data_dict:
            user_op_data_dict[track_id]["user_op_doc_ref"].set({"status_admin": status_admin}, merge=True)
            del user_op_data_dict[track_id]  # Удаляем обработанный элемент из локальной структуры данных
        else:
            filtered_array.append(track_id)

    return filtered_array

