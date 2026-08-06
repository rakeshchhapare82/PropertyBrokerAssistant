import urllib.parse

from repositories.whatsapp_repository import WhatsAppRepository


class WhatsAppService:

    # -------------------------------------------------
    # Available Placeholders
    # -------------------------------------------------

    @staticmethod
    def available_placeholders():

        return [
            "{ClientName}",
            "{Mobile}",
            "{Email}",
            "{City}",
            "{PropertyType}",
            "{PreferredLocation}",
            "{BudgetMin}",
            "{BudgetMax}",
            "{Status}",
            "{Priority}"
        ]

    # -------------------------------------------------
    # Generate Personalized Message
    # -------------------------------------------------

    @staticmethod
    def generate_message(template, client):

        if not template:
            return ""

        message = template

        values = {

            "{ClientName}": client.get("full_name", ""),

            "{Mobile}": client.get("mobile", ""),

            "{Email}": client.get("email", ""),

            "{City}": client.get("city", ""),

            "{PropertyType}": client.get("property_type", ""),

            "{PreferredLocation}":
                client.get("location_preferred", ""),

            "{BudgetMin}":
                str(client.get("budget_min", "")),

            "{BudgetMax}":
                str(client.get("budget_max", "")),

            "{Status}":
                client.get("status", ""),

            "{Priority}":
                client.get("priority", "")
        }

        for key, value in values.items():
            message = message.replace(
                key,
                str(value if value else "")
            )

        return message

    # -------------------------------------------------
    # WhatsApp URL
    # -------------------------------------------------

    @staticmethod
    def generate_whatsapp_url(
            mobile,
            message
    ):

        mobile = (
            str(mobile)
            .replace("+", "")
            .replace(" ", "")
            .replace("-", "")
        )

        if not mobile.startswith("91"):
            mobile = "91" + mobile

        encoded = urllib.parse.quote(message)

        return f"https://wa.me/{mobile}?text={encoded}"

    # -------------------------------------------------
    # Preview Message
    # -------------------------------------------------

    @staticmethod
    def preview(template, client):

        return WhatsAppService.generate_message(
            template,
            client
        )

    # -------------------------------------------------
    # Create Campaign
    # -------------------------------------------------

    @staticmethod
    def create_campaign(
            campaign_name,
            template,
            selected_clients
    ):

        if not campaign_name.strip():
            raise Exception(
                "Campaign Name is required."
            )

        if not template.strip():
            raise Exception(
                "Message cannot be empty."
            )

        if len(selected_clients) == 0:
            raise Exception(
                "Please select at least one client."
            )

        campaign_id = WhatsAppRepository.create_campaign(

            campaign_name=campaign_name,

            message_template=template,

            total_clients=len(selected_clients)

        )

        for client in selected_clients:

            personalized = (
                WhatsAppService.generate_message(
                    template,
                    client
                )
            )

            url = (
                WhatsAppService.generate_whatsapp_url(
                    client["mobile"],
                    personalized
                )
            )

            WhatsAppRepository.save_campaign_detail(

                campaign_id=campaign_id,

                client_id=client["client_id"],

                mobile=client["mobile"],

                personalized_message=personalized,

                whatsapp_url=url,

                status="Pending"

            )

        return campaign_id

    # -------------------------------------------------
    # Campaign List
    # -------------------------------------------------

    @staticmethod
    def get_campaigns():

        return WhatsAppRepository.get_campaigns()

    # -------------------------------------------------
    # Campaign Details
    # -------------------------------------------------

    @staticmethod
    def get_campaign_details(
            campaign_id
    ):

        return WhatsAppRepository.get_campaign_details(
            campaign_id
        )

    # -------------------------------------------------
    # Update Status
    # -------------------------------------------------

    @staticmethod
    def update_status(
            detail_id,
            status
    ):

        WhatsAppRepository.update_status(
            detail_id,
            status
        )

    # -------------------------------------------------
    # Delete Campaign
    # -------------------------------------------------

    @staticmethod
    def delete_campaign(
            campaign_id
    ):

        WhatsAppRepository.delete_campaign(
            campaign_id
        )

    # -------------------------------------------------
    # Campaign By Id
    # -------------------------------------------------

    @staticmethod
    def get_campaign(
            campaign_id
    ):

        return WhatsAppRepository.get_campaign(
            campaign_id
        )