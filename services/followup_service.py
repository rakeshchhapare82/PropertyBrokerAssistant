from repositories.followup_repository import FollowupRepository


class FollowupService:
    """
    Business logic layer for Follow-up operations.
    """



    # -------------------------------------------------
    # Add Follow-up
    # -------------------------------------------------

    @staticmethod
    def add(followup):


        if not followup.client_id:

            raise Exception(
                "Client is required."
            )


        if not followup.followup_date:

            raise Exception(
                "Follow-up date is required."
            )


        if not followup.followup_type:

            raise Exception(
                "Follow-up type is required."
            )


        FollowupRepository.insert(
            followup
        )



    # -------------------------------------------------
    # Update Follow-up
    # -------------------------------------------------

    @staticmethod
    def update(
            followup_id,
            followup
    ):


        existing = FollowupRepository.get(
            followup_id
        )


        if existing is None:

            raise Exception(
                "Follow-up not found."
            )



        if not followup.client_id:

            raise Exception(
                "Client is required."
            )



        if not followup.followup_date:

            raise Exception(
                "Follow-up date is required."
            )



        if not followup.followup_type:

            raise Exception(
                "Follow-up type is required."
            )



        FollowupRepository.update(
            followup_id,
            followup
        )



    # -------------------------------------------------
    # Get All Follow-ups
    # -------------------------------------------------

    @staticmethod
    def get_all():

        return FollowupRepository.get_all()



    # -------------------------------------------------
    # Get Follow-up By ID
    # -------------------------------------------------

    @staticmethod
    def get(followup_id):

        return FollowupRepository.get(
            followup_id
        )



    # -------------------------------------------------
    # Delete Follow-up
    # -------------------------------------------------

    @staticmethod
    def delete(
            followup_id
    ):


        existing = FollowupRepository.get(
            followup_id
        )


        if existing is None:

            raise Exception(
                "Follow-up not found."
            )



        FollowupRepository.delete(
            followup_id
        )



    # -------------------------------------------------
    # Mark Completed
    # -------------------------------------------------

    @staticmethod
    def mark_completed(
            followup_id
    ):


        existing = FollowupRepository.get(
            followup_id
        )


        if existing is None:

            raise Exception(
                "Follow-up not found."
            )



        FollowupRepository.mark_completed(
            followup_id
        )



    # -------------------------------------------------
    # Today's Follow-ups
    # -------------------------------------------------

    @staticmethod
    def get_today_followups():

        return FollowupRepository.get_today_followups()



    # -------------------------------------------------
    # Pending Follow-ups
    # -------------------------------------------------

    @staticmethod
    def get_pending_followups():

        return FollowupRepository.get_pending_followups()



    # -------------------------------------------------
    # Dashboard Counts
    # -------------------------------------------------

    @staticmethod
    def total_followups():

        return FollowupRepository.count_total()



    @staticmethod
    def total_pending_followups():

        return FollowupRepository.count_pending()



    @staticmethod
    def total_today_followups():

        return FollowupRepository.count_today()