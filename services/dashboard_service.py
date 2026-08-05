from repositories.dashboard_repository import DashboardRepository


class DashboardService:
    """
    Business logic for Dashboard.
    """

    @staticmethod
    def get_dashboard_summary():
        """
        Returns dashboard KPI summary.
        """

        return {
            "total_clients": DashboardRepository.get_total_clients(),
            "interested_clients": DashboardRepository.get_interested_clients(),
            "pending_followups": DashboardRepository.get_pending_followups(),
            "today_followups": DashboardRepository.get_today_followups()
        }

    @staticmethod
    def get_today_followups():
        """
        Returns today's follow-up list.
        """

        return DashboardRepository.get_today_followup_list()

    @staticmethod
    def get_pending_followups():
        """
        Returns pending follow-up list.
        """

        return DashboardRepository.get_pending_followup_list()

    @staticmethod
    def get_recent_clients(limit=10):
        """
        Returns recently added clients.
        """

        return DashboardRepository.get_recent_clients(limit)

    @staticmethod
    def get_recent_followups(limit=10):
        """
        Returns recent follow-up activity.
        """

        return DashboardRepository.get_recent_followups(limit)