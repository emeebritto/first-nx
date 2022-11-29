from utils.managers import Room_Managet
room_Managet = Room_Managet()


def create_key(svars, nexa, res):
	label = svars.get("LABEL")
	sender_id = svars.get("SENDER_ID")
	try:
		obj_key = room_Managet.create_key(label=f"{sender_id}::{label}")
		print("created key", obj_key)
		res.sendText(f"your key ({label}) was created")
		res.appendText(f"key: {obj_key['key']}")
	except Exception as e:
		print(e)
		return res.appendText(str(e))


def list_keys(svars, nexa, res):
	sender_id = svars.get("SENDER_ID")
	matches = room_Managet.search_matches(sender_id)
	if not len(matches): return res.appendText("You don't have keys yet")
	for match in matches:
		key_label = match["label"].split("::")[1]
		res.appendText(f"label: {key_label},\nkey: {match['key']}")
	return res


def del_key(svars, nexa, res):
	label = svars.get("LABEL")
	sender_id = svars.get("SENDER_ID")
	deleted_key = room_Managet.del_key_by_label(f"{sender_id}::{label}")
	if deleted_key:
		key_label = deleted_key["label"].split("::")[1]
		key = deleted_key["key"]
		return res.appendText(f"the key ({key_label} - {key}) was deleted")
	else:
		return res.appendText("key wasn't deleted, maybe it's not exists")
