from database import (
    execute_query,
    fetch_one,
    fetch_all
)


class WhatsAppRepository:
    """
    Repository for WhatsApp Campaign operations.
    """


    # ---------------------------------------------
    # Create Campaign
    # ---------------------------------------------

    @staticmethod
    def create_campaign(
            campaign_name,
            message_template,
            total_clients
    ):

        query = """
        INSERT INTO whatsapp_campaigns
        (
            campaign_name,
            message_template,
            total_clients
        )

        VALUES
        (
            :campaign_name,
            :message_template,
            :total_clients
        )

        RETURNING campaign_id
        """

        result = fetch_one(
            query,
            {
                "campaign_name": campaign_name,
                "message_template": message_template,
                "total_clients": total_clients
            }
        )

        return result["campaign_id"]


    # ---------------------------------------------
    # Save Client Message
    # ---------------------------------------------

    @staticmethod
    def save_campaign_detail(

            campaign_id,

            client_id,

            mobile,

            personalized_message,

            whatsapp_url,

            status="Pending"

    ):

        query = """
        INSERT INTO
        whatsapp_campaign_details
        (
            campaign_id,

            client_id,

            mobile,

            personalized_message,

            whatsapp_url,

            status
        )

        VALUES
        (
            :campaign_id,

            :client_id,

            :mobile,

            :personalized_message,

            :whatsapp_url,

            :status
        )
        """

        execute_query(
            query,
            {

                "campaign_id": campaign_id,

                "client_id": client_id,

                "mobile": mobile,

                "personalized_message":
                personalized_message,

                "whatsapp_url":
                whatsapp_url,

                "status":
                status

            }
        )


    # ---------------------------------------------
    # Update Status
    # ---------------------------------------------

    @staticmethod
    def update_status(
            detail_id,
            status
    ):

        query = """
        UPDATE whatsapp_campaign_details

        SET status=:status

        WHERE detail_id=:detail_id
        """

        execute_query(
            query,
            {

                "detail_id": detail_id,

                "status": status

            }
        )


    # ---------------------------------------------
    # Campaign List
    # ---------------------------------------------

    @staticmethod
    def get_campaigns():

        query = """
        SELECT *

        FROM whatsapp_campaigns

        ORDER BY created_on DESC
        """

        return fetch_all(query)


    # ---------------------------------------------
    # Campaign Details
    # ---------------------------------------------

    @staticmethod
    def get_campaign_details(
            campaign_id
    ):

        query = """
        SELECT

            d.*,

            c.full_name

        FROM
            whatsapp_campaign_details d

        INNER JOIN clients c

            ON c.client_id=d.client_id

        WHERE
            campaign_id=:campaign_id

        ORDER BY
            c.full_name
        """

        return fetch_all(
            query,
            {

                "campaign_id": campaign_id

            }
        )


    # ---------------------------------------------
    # Campaign By Id
    # ---------------------------------------------

    @staticmethod
    def get_campaign(
            campaign_id
    ):

        query = """
        SELECT *

        FROM whatsapp_campaigns

        WHERE campaign_id=:campaign_id
        """

        return fetch_one(
            query,
            {

                "campaign_id": campaign_id

            }
        )


    # ---------------------------------------------
    # Delete Campaign
    # ---------------------------------------------

    @staticmethod
    def delete_campaign(
            campaign_id
    ):

        query = """
        DELETE

        FROM whatsapp_campaigns

        WHERE campaign_id=:campaign_id
        """

        execute_query(
            query,
            {

                "campaign_id": campaign_id

            }
        )