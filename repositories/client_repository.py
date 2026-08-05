from database import execute_query, fetch_all, fetch_one


class ClientRepository:
    """
    Repository layer for Client database operations.
    """

    # -------------------------------------------------
    # Add New Client
    # -------------------------------------------------

    @staticmethod
    def insert(client):

        query = """
        INSERT INTO clients
        (
            full_name,
            mobile,
            alternate_mobile,
            email,
            city,
            property_type,
            location_preferred,
            budget_min,
            budget_max,
            source,
            status,
            priority,
            remarks
        )

        VALUES
        (
            :full_name,
            :mobile,
            :alternate_mobile,
            :email,
            :city,
            :property_type,
            :location_preferred,
            :budget_min,
            :budget_max,
            :source,
            :status,
            :priority,
            :remarks
        )
        """

        execute_query(
            query,
            client.__dict__
        )


    # -------------------------------------------------
    # Get All Clients
    # -------------------------------------------------

    @staticmethod
    def get_all():

        query = """
        SELECT *
        FROM clients
        ORDER BY client_id DESC
        """

        return fetch_all(query)


    # -------------------------------------------------
    # Get Client By ID
    # -------------------------------------------------

    @staticmethod
    def get(client_id):

        query = """
        SELECT *
        FROM clients
        WHERE client_id = :client_id
        """

        return fetch_one(
            query,
            {
                "client_id": client_id
            }
        )


    # -------------------------------------------------
    # Check Duplicate Mobile
    # -------------------------------------------------

    @staticmethod
    def exists(mobile):

        query = """
        SELECT client_id
        FROM clients
        WHERE mobile = :mobile
        """

        result = fetch_one(
            query,
            {
                "mobile": mobile
            }
        )

        return result is not None


    # -------------------------------------------------
    # Check Duplicate Mobile During Edit
    # Ignore Current Client
    # -------------------------------------------------

    @staticmethod
    def mobile_exists_for_other(
            client_id,
            mobile
    ):

        query = """
        SELECT client_id
        FROM clients
        WHERE mobile = :mobile
        AND client_id <> :client_id
        """

        result = fetch_one(
            query,
            {
                "client_id": client_id,
                "mobile": mobile
            }
        )

        return result is not None



    # -------------------------------------------------
    # Update Existing Client
    # -------------------------------------------------

    @staticmethod
    def update(
            client_id,
            client
    ):

        query = """
        UPDATE clients

        SET

            full_name = :full_name,

            mobile = :mobile,

            alternate_mobile = :alternate_mobile,

            email = :email,

            city = :city,

            property_type = :property_type,

            location_preferred = :location_preferred,

            budget_min = :budget_min,

            budget_max = :budget_max,

            source = :source,

            status = :status,

            priority = :priority,

            remarks = :remarks


        WHERE client_id = :client_id
        """


        params = client.__dict__.copy()

        params["client_id"] = client_id


        execute_query(
            query,
            params
        )



    # -------------------------------------------------
    # Delete Client
    # -------------------------------------------------

    @staticmethod
    def delete(client_id):

        query = """
        DELETE
        FROM clients
        WHERE client_id = :client_id
        """

        execute_query(
            query,
            {
                "client_id": client_id
            }
        )


    # -------------------------------------------------
    # Search Client
    # -------------------------------------------------

    @staticmethod
    def search(search_text):

        query = """
        SELECT *

        FROM clients

        WHERE
            full_name ILIKE :search
            OR mobile ILIKE :search
            OR city ILIKE :search

        ORDER BY client_id DESC
        """


        return fetch_all(
            query,
            {
                "search": f"%{search_text}%"
            }
        )