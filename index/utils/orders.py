from datetime import datetime

from index.utils.connect_firebase import db, order_collection_path, to_receiving_country, history_status_collection_path


def add_order(data):
    track_id = data["track_id"]
    if check_if_order_exists(track_id):
        order_id = get_order_id_by_track_id(track_id)
        return replace_order_status(order_id, to_receiving_country)
    else:
        doc_ref = db.collection(order_collection_path).add(data)
        return doc_ref[1].id if doc_ref[1].id else False


def check_if_order_exists(track_id):
    docs = db.collection(order_collection_path).where("track_id", "==", track_id).stream()
    return len(list(docs)) > 0


def get_order_id_by_track_id(track_id):
    docs = db.collection(order_collection_path).where("track_id", "==", track_id).stream()
    for doc in docs:
        return doc.id
    return None


def replace_order_status(order_id, new_status_reference):
    order_ref = db.collection(order_collection_path).document(order_id)

    # Получаем текущий статус заказа
    old_status_reference = order_ref.get().to_dict().get('status')
    if old_status_reference == new_status_reference:
        return f"Order {order_id} already has status {new_status_reference.id}"
    # Обновляем статус заказа
    order_ref.update({"status": new_status_reference})

    # Добавляем запись в историю изменений статуса заказа
    history_data = {
        "old_status": old_status_reference,
        "new_status": new_status_reference,
        "datetime": datetime.now(),
        "order": order_ref
    }
    db.collection(history_status_collection_path).add(history_data)

    return f"Order {order_id} status updated to {new_status_reference.id}"
