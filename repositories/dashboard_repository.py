from database import fetch_all, fetch_one


class DashboardRepository:
    """
    Repository class for Dashboard data.
    """

    @staticmethod
    def get_total_clients():
        query = """
        SELECT COUNT(*) AS total
        FROM clients
        """

        result = fetch_one(query)

        return result["total"] if result else 0

    @staticmethod
    def get_interested_clients():
        query = """
        SELECT COUNT(*) AS total
        FROM clients
        WHERE status='Interested'
        """

        result = fetch_one(query)

        return result["total"] if result else 0

    @staticmethod
    def get_pending_followups():
        query = """
        SELECT COUNT(*) AS total
        FROM followups
        WHERE status='Pending'
        """

        result = fetch_one(query)

        return result["total"] if result else 0

    @staticmethod
    def get_today_followups():
        query = """
        SELECT COUNT(*) AS total
        FROM followups
        WHERE followup_date = CURRENT_DATE
        """

        result = fetch_one(query)

        return result["total"] if result else 0

    @staticmethod
    def get_today_followup_list():
        query = """
        SELECT
            c.full_name,
            c.mobile,
            f.followup_date,
            f.followup_time,
            f.followup_type,
            f.status
        FROM followups f
        INNER JOIN clients c
            ON c.client_id = f.client_id
        WHERE f.followup_date = CURRENT_DATE
        ORDER BY f.followup_time
        """

        return fetch_all(query)

    @staticmethod
    def get_pending_followup_list():
        query = """
        SELECT
            c.full_name,
            c.mobile,
            f.followup_date,
            f.followup_time,
            f.followup_type,
            f.status
        FROM followups f
        INNER JOIN clients c
            ON c.client_id = f.client_id
        WHERE f.status='Pending'
        ORDER BY f.followup_date, f.followup_time
        """

        return fetch_all(query)

    @staticmethod
    def get_recent_clients(limit=10):
        query = """
        SELECT
            full_name,
            mobile,
            city,
            status,
            created_on
        FROM clients
        ORDER BY created_on DESC
        LIMIT :limit
        """

        return fetch_all(
            query,
            {"limit": limit}
        )

    @staticmethod
    def get_recent_followups(limit=10):
        query = """
        SELECT
            c.full_name,
            c.mobile,
            f.followup_date,
            f.followup_type,
            f.status
        FROM followups f
        INNER JOIN clients c
            ON c.client_id = f.client_id
        ORDER BY f.followup_date DESC
        LIMIT :limit
        """

        return fetch_all(
            query,
            {"limit": limit}
        )