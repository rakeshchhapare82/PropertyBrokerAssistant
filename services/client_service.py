from repositories.client_repository import ClientRepository


class ClientService:
    """
    Business logic layer for Client operations.
    """


    # -------------------------------------------------
    # Add Client
    # -------------------------------------------------

    @staticmethod
    def add(client):

        # Required validation

        if not client.full_name:
            raise Exception(
                "Client name is required."
            )


        if not client.mobile:
            raise Exception(
                "Mobile number is required."
            )


        # Duplicate mobile validation

        if ClientRepository.exists(
            client.mobile
        ):

            raise Exception(
                "Mobile number already exists."
            )


        # Budget validation

        if client.budget_max < client.budget_min:

            raise Exception(
                "Maximum budget cannot be less than minimum budget."
            )


        ClientRepository.insert(
            client
        )



    # -------------------------------------------------
    # Update Client
    # -------------------------------------------------

    @staticmethod
    def update(
            client_id,
            client
    ):


        existing = ClientRepository.get(
            client_id
        )


        if existing is None:

            raise Exception(
                "Client not found."
            )



        if not client.full_name:

            raise Exception(
                "Client name is required."
            )



        if not client.mobile:

            raise Exception(
                "Mobile number is required."
            )



        # Check duplicate mobile
        # except current client

        if ClientRepository.mobile_exists_for_other(
            client_id,
            client.mobile
        ):

            raise Exception(
                "Mobile number already exists for another client."
            )



        if client.budget_max < client.budget_min:

            raise Exception(
                "Maximum budget cannot be less than minimum budget."
            )



        ClientRepository.update(
            client_id,
            client
        )



    # -------------------------------------------------
    # Get All Clients
    # -------------------------------------------------

    @staticmethod
    def get_all():

        return ClientRepository.get_all()



    # -------------------------------------------------
    # Get Client By ID
    # -------------------------------------------------

    @staticmethod
    def get(client_id):

        return ClientRepository.get(
            client_id
        )



    # -------------------------------------------------
    # Delete Client
    # -------------------------------------------------

    @staticmethod
    def delete(client_id):


        existing = ClientRepository.get(
            client_id
        )


        if existing is None:

            raise Exception(
                "Client not found."
            )


        ClientRepository.delete(
            client_id
        )



    # -------------------------------------------------
    # Search Client
    # -------------------------------------------------

    @staticmethod
    def search(search_text):

        if not search_text:

            return ClientRepository.get_all()


        return ClientRepository.search(
            search_text
        )