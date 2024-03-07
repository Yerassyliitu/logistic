from index.utils.connect_firebase import db


def change_order_status(rows, status_admin, field_to_parse):
    user_docs = db.collection("users").stream()
    array = []
    for row in rows:
        track_id = row[field_to_parse - 1]
        if track_id == None or track_id == '' or track_id == 'None':
            continue
        try:
            track_id = int(track_id)
        except:
            track_id = track_id
        # print(track_id)
        array.append(track_id)
    count = 0
    for user_doc in user_docs:
        users_op_ref = db.collection("users").document(user_doc.id).collection("users_op").stream()
        for user_op_doc in users_op_ref:
            user_op_data = user_op_doc.to_dict()
            for track_id in array:
                if track_id == user_op_data["barcode"]:
                    print(track_id)
                    user_op_doc.reference.set({"status_admin": status_admin}, merge=True)
                    array.remove(track_id)
                    break

    return array


