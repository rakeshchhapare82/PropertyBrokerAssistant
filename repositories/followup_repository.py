from database import execute_query, fetch_all, fetch_one


class FollowupRepository:
    """
    Repository layer for Follow-up database operations.
    """


    # -------------------------------------------------
    # Add Follow-up
    # -------------------------------------------------

    @staticmethod
    def insert(followup):

        query = """
        INSERT INTO followups
        (
            client_id,
            followup_date,
            followup_time,
            followup_type,
            discussion_notes,
            next_followup_date,
            reminder,
            status
        )

        VALUES
        (
            :client_id,
            :followup_date,
            :followup_time,
            :followup_type,
            :discussion_notes,
            :next_followup_date,
            :reminder,
            :status
        )
        """


        execute_query(
            query,
            followup.__dict__
        )



    # -------------------------------------------------
    # Get All Follow-ups
    # -------------------------------------------------

    @staticmethod
    def get_all():

        query = """
        SELECT
            f.*,
            c.full_name,
            c.mobile

        FROM followups f

        INNER JOIN clients c
            ON c.client_id = f.client_id

        ORDER BY
            f.followup_date DESC,
            f.followup_time DESC
        """


        return fetch_all(query)



    # -------------------------------------------------
    # Get Follow-up By ID
    # -------------------------------------------------

    @staticmethod
    def get(followup_id):

        query = """
        SELECT *

        FROM followups

        WHERE followup_id = :followup_id
        """


        return fetch_one(
            query,
            {
                "followup_id": followup_id
            }
        )



    # -------------------------------------------------
    # Update Follow-up
    # -------------------------------------------------

    @staticmethod
    def update(
            followup_id,
            followup
    ):


        query = """
        UPDATE followups

        SET

            client_id = :client_id,

            followup_date = :followup_date,

            followup_time = :followup_time,

            followup_type = :followup_type,

            discussion_notes = :discussion_notes,

            next_followup_date = :next_followup_date,

            reminder = :reminder,

            status = :status


        WHERE followup_id = :followup_id
        """



        params = followup.__dict__.copy()


        params["followup_id"] = followup_id



        execute_query(
            query,
            params
        )



    # -------------------------------------------------
    # Delete Follow-up
    # -------------------------------------------------

    @staticmethod
    def delete(followup_id):


        query = """
        DELETE

        FROM followups

        WHERE followup_id = :followup_id
        """


        execute_query(
            query,
            {
                "followup_id": followup_id
            }
        )



    # -------------------------------------------------
    # Mark Completed
    # -------------------------------------------------

    @staticmethod
    def mark_completed(
            followup_id
    ):


        query = """
        UPDATE followups

        SET status = 'Completed'

        WHERE followup_id = :followup_id
        """



        execute_query(
            query,
            {
                "followup_id": followup_id
            }
        )



    # -------------------------------------------------
    # Today's Follow-ups
    # -------------------------------------------------

    @staticmethod
    def get_today_followups():


        query = """
        SELECT

            f.*,

            c.full_name,

            c.mobile


        FROM followups f


        INNER JOIN clients c

            ON c.client_id = f.client_id


        WHERE f.followup_date = CURRENT_DATE


        ORDER BY f.followup_time
        """


        return fetch_all(query)



    # -------------------------------------------------
    # Pending Follow-ups
    # -------------------------------------------------

    @staticmethod
    def get_pending_followups():


        query = """
        SELECT

            f.*,

            c.full_name,

            c.mobile


        FROM followups f


        INNER JOIN clients c

            ON c.client_id = f.client_id


        WHERE f.status = 'Pending'


        ORDER BY
            f.followup_date,
            f.followup_time
        """



        return fetch_all(query)



    # -------------------------------------------------
    # Count Total Follow-ups
    # -------------------------------------------------

    @staticmethod
    def count_total():


        query = """
        SELECT COUNT(*) AS total

        FROM followups
        """

        result = fetch_one(query)


        return result["total"] if result else 0



    # -------------------------------------------------
    # Count Pending Follow-ups
    # -------------------------------------------------

    @staticmethod
    def count_pending():


        query = """
        SELECT COUNT(*) AS total

        FROM followups

        WHERE status='Pending'
        """


        result = fetch_one(query)


        return result["total"] if result else 0



    # -------------------------------------------------
    # Count Today's Follow-ups
    # -------------------------------------------------

    @staticmethod
    def count_today():


        query = """
        SELECT COUNT(*) AS total

        FROM followups

        WHERE followup_date = CURRENT_DATE
        """


        result = fetch_one(query)


        return result["total"] if result else 0