complaints = []
id_counter = 1000

def add_complaint(data):
    global id_counter
    id_counter += 1
    data["id"] = id_counter
    complaints.append(data)
    return id_counter


def get_complaints():
    return complaints