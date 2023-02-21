from backend import app
import unittest

ENDPOINT = "http://127.0.0.1:5000"

class TestBackend(unittest.TestCase):

    #Check for OK Response on all of our routes
    def test_routes(self):
        tester = app.test_client(self)
        response = tester.get("/tickets")
        statuscode = response.status_code
        assert statuscode == 200
        pass
        print("Response code test completed with code: " + str(statuscode))

    #check for valid JSON return data
    def test_data_types(self):
        tester = app.test_client(self)
        response = tester.get("/tickets")
        self.assertEqual(response.content_type,"application/json")
        print("Datatype test completed with response: " + str(response))

    '''
    def test_mass_create(self):
        for x in range (1,200):
            payload = create_numbered_payload(x)
            create_ticket(payload,self)
    '''
    #Check ticket creation endpoint
    def test_create(self):
        payload = create_payload()
        create_response = create_ticket(payload,self)
        assert create_response.status_code == 200
        data = create_response.get_json()

        #get the id of ticket we just created to verify data
        ticket_id = data["id"]
        get_create_response = get_ticket(ticket_id,self)
        assert get_create_response.status_code == 200
        get_create_response = get_create_response.get_json()
        assert get_create_response["name"] == payload["name"]
        assert get_create_response["description"] == payload["description"]
        assert get_create_response["date"] == payload["date"]
        
        #delete the test ticket
        delete_ticket_response = delete_ticket(ticket_id,self)
        assert delete_ticket_response.status_code == 200

    def test_update_ticket(self):
        payload = create_payload()
        data = create_ticket(payload,self)
        ticket_id = data.get_json()["id"]

        #define a new payload to update the ticket with
        new_payload = {
            "name": "creationUnitTestUpdated",
            "description": "creationUnitTestDescUpdated",
            "date": "2023-01-01"
        }
        update_ticket_response = update_ticket(ticket_id,new_payload)
        assert update_ticket_response.status_code == 200
        update_ticket_data = update_ticket_response.get_json()

        #verify the updated ticket now matches the new payload
        assert update_ticket_data["description"] == new_payload["description"]
        assert update_ticket_data["name"] == new_payload["name"]

        #delete the test ticket
        delete_ticket_response = delete_ticket(ticket_id,self)
        assert delete_ticket_response.status_code == 200
        pass

def create_ticket(payload,obj):
    tester = app.test_client(obj)
    return tester.post('/ticket', json=payload)
    pass

def update_ticket(ticket_id,payload):
    tester = app.test_client()
    return tester.put('/ticket/' + f"{ticket_id}", json=payload)
    pass

def get_ticket(ticket_id,obj):
    tester = app.test_client(obj)
    return tester.get('/ticket/' + f"{ticket_id}")
    pass

def delete_ticket(ticket_id,obj):
    tester = app.test_client(obj)
    return tester.delete('/ticket/' + f"{ticket_id}")
    pass

def create_numbered_payload(num):
        payload = {
            "name": f'AutoGenEntry{num}',
            "description": f'AutoGenEntry{num} Description',
            "date": "2023-01-01"
        }
        return payload


def create_payload():
        payload = {
            "name": "creationUnitTest",
            "description": "creationUnitTestDesc",
            "date": "2023-01-01"
        }
        return payload

if __name__ == "__main__":
    unittest.main()