

class Component:

    def __init__(self, client):
        self.client = client

    def get_all_components(self):

        COMPONENTS_QUALIFIERS = ('TRK')
        return self.client.get_components(
            qualifiers=COMPONENTS_QUALIFIERS)
