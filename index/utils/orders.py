from datetime import datetime

from index.utils.connect_firebase import db, order_collection_path, to_receiving_country, history_status_collection_path


async def add_order(data):
    track_id = data["track_id"]
    if await check_if_order_exists(track_id):
        order_id = await get_order_id_by_track_id(track_id)
        return await replace_order_status(order_id, to_receiving_country)
    else:
        doc_ref = await db.collection(order_collection_path).add(data)
        return doc_ref.id if doc_ref.id else False


async def check_if_order_exists(track_id):
    query = db.collection(order_collection_path).where("track_id", "==", track_id).limit(1)
    async for _ in query.stream():
        return True
    return False


async def get_order_id_by_track_id(track_id):
    query = db.collection(order_collection_path).where("track_id", "==", track_id).limit(1)
    async for doc in query.stream():
        return doc.id
    return None


async def replace_order_status(order_id, new_status_reference):
    order_ref = db.collection(order_collection_path).document(order_id)

    order_snapshot = await order_ref.get()
    order_data = order_snapshot.to_dict()
    old_status_reference = order_data.get('status')

    if old_status_reference == new_status_reference:
        return f"Order {order_id} already has status {new_status_reference.id}"

    await order_ref.update({"status": new_status_reference})

    history_data = {
        "old_status": old_status_reference,
        "new_status": new_status_reference,
        "datetime": datetime.now(),
        "order": order_ref
    }
    await db.collection(history_status_collection_path).add(history_data)

    return f"Order {order_id} status updated to {new_status_reference.id}"