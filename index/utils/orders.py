from index.utils.connect_firebase import db
from datetime import datetime


def change_order_status(array, status_admin):
    # Load all documents from the "users_op" collection group
    users_op_ref = db.collection_group("users_op").stream()
    user_op_data_dict = {}

    # Collect data into a local data structure
    for user_op_doc in users_op_ref:
        user_op_data = user_op_doc.to_dict()
        barcode = user_op_data.get("barcode")
        if barcode:
            user_op_data_dict[barcode] = {
                "user_doc_id": user_op_doc.reference.parent.parent.id,
                "user_op_doc_ref": user_op_doc.reference,
                "exactly_weight": user_op_data.get("exactly_weight", 0)  # Default weight to 0 if not present
            }

    filtered_array = []
    # Update statuses in Firebase database and local data structure
    for track_id in array:
        try:
            track_id = int(track_id)
        except ValueError:
            track_id = str(track_id)
        track_id = str(track_id)
        if track_id in user_op_data_dict:
            print("FOUND TRACK ID", track_id)
            # Default op_data with status_admin update
            op_data = {
                "op_check": False,
                "op_created": False,
                "op_stock": False,
                "op_otw": False,
                "op_kz": False,
                "op_received": False,
                "status_admin": status_admin,
                "admin_note": user_op_data_dict[track_id].get("admin_note", ""),
                # Set exactly_weight only if not already set, or modify this logic as needed
                "exactly_weight": user_op_data_dict[track_id].get("exactly_weight", 0)
            }

            # Conditionally updating op_data based on status_admin
            if status_admin == "На складе в Китае":
                op_data["op_stock"] = True
                op_data["op_stock_time"] = datetime.now()
            elif status_admin == "В пути":
                op_data["op_otw"] = True
                op_data["op_otw_time"] = datetime.now()
            elif status_admin == "В пункте выдачи":
                op_data["op_kz"] = True
                op_data["op_kz_time"] = datetime.now()
            # Add any additional statuses or logic as needed

            # Update document in Firestore
            user_op_data_dict[track_id]["user_op_doc_ref"].set(op_data, merge=True)
            del user_op_data_dict[track_id]
        else:
            filtered_array.append(track_id)

    print(filtered_array)
    return filtered_array

