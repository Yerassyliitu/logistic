from index.utils.connect_firebase import db
from datetime import datetime


def change_order_status(array, status_admin, editor_Ref):

    # Load all documents from the "users_op" collection group
    users_op_ref = db.collection_group("users_op").stream()
    user_op_data_dict = {}

    # Collect data into a local data structure
    for user_op_doc in users_op_ref:
        user_op_data = user_op_doc.to_dict()
        barcode = user_op_data.get("barcode")
        if barcode:
            try:
                user_op_data_dict[barcode] = {
                    "user_doc_id": user_op_doc.reference.parent.parent.id,
                    "user_op_doc_ref": user_op_doc.reference,
                    "exactly_weight": user_op_data.get("exactly_weight", 0)  # Default weight to 0 if not present
                }
            except:
                continue
    user_doc_id = None
    company_op = None
    try:
        user_ref = db.collection("users").where("uid", "==", editor_Ref).get()

        for doc in user_ref:
            if doc.exists:
                user_doc_id = doc.id
                user_data = doc.to_dict()
                company_op = user_data.get("company")
                break
    except:
        print("User with editorRef not found")

    filtered_array = []
    # Update statuses in Firebase database and local data structure
    for track_id in array:
        try:
            track_id = int(track_id)
        except ValueError:
            track_id = str(track_id)
        track_id = str(track_id)

        # company_op = 'qlpZ3NiOIYiSMTDROmeV'
        if track_id in user_op_data_dict:
            user_op_doc_ref = user_op_data_dict[track_id]["user_op_doc_ref"]
            user_op_doc = user_op_doc_ref.get()
            user_op_data = user_op_doc.to_dict()
            op_data = {
                "op_check": False,
                "op_created": False,
                "op_stock": False,
                "op_otw": False,
                "op_kz": False,
                "op_received": False,
                "status_admin": status_admin,
                "exactly_weight":user_op_data.get("exactly_weight", 0)
            }

            if status_admin == "На складе в Китае" and not user_op_data.get('op_stock') and not user_op_data.get('op_otw') and not user_op_data.get('op_kz') and not user_op_data.get('op_received'):
                op_data["op_stock"] = True
                op_data["op_stock_time"] = datetime.now()
                user_op_data_dict[track_id]["user_op_doc_ref"].set(op_data, merge=True)
                del user_op_data_dict[track_id]
            elif status_admin == "В пути" and not user_op_data.get('op_otw') and not user_op_data.get('op_kz') and not user_op_data.get('op_received'):
                op_data["op_otw"] = True
                op_data["op_otw_time"] = datetime.now()
                user_op_data_dict[track_id]["user_op_doc_ref"].set(op_data, merge=True)
                del user_op_data_dict[track_id]
            elif status_admin == "В пункте выдачи" and not user_op_data.get('op_kz') and not user_op_data.get('op_received'):
                op_data["op_kz"] = True
                op_data["op_kz_time"] = datetime.now()
                user_op_data_dict[track_id]["user_op_doc_ref"].set(op_data, merge=True)
                del user_op_data_dict[track_id]
            # Add any additional statuses or logic as needed

            # Update document in Firestore

        else:
            if company_op and user_doc_id:
                new_op_data = {
                    "barcode": track_id,
                    "CompanyOp": company_op,
                    "date_create": datetime.now(),
                    "op_created": False,
                    "op_stock": True,
                    "op_stick_time": datetime.now(),
                    "op_created_time": datetime.now(),
                    "count": 0,
                    'status_admin': 'На складе в Китае',
                    "name": '',
                    "withoutUser": True,
                }
                user_ref = db.collection('users').document(user_doc_id).collection('users_op').document()
                user_ref.set(new_op_data)
                print("Created new user_op with track ID and CompanyOp:", track_id, company_op)
            filtered_array.append(track_id)

    print(filtered_array)
    return filtered_array

