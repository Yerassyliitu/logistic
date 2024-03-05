from index.utils.connect_firebase import db


def change_order_status(track_id, status_admin):
    user_docs = db.collection("users").stream()

    # Iterate over each user document
    for user_doc in user_docs:
        # Get the reference to the users_op subcollection for the current user document
        users_op_ref = db.collection("users").document(user_doc.id).collection("users_op").stream()
        for user_op_doc in users_op_ref:
            # Convert the document to a dictionary
            user_op_data = user_op_doc.to_dict()
            print(track_id, user_op_data["barcode"])
            if track_id == user_op_data["barcode"]:
                # Update the status_admin field
                user_op_doc.reference.set({"status_admin": status_admin}, merge=True)
                return True



