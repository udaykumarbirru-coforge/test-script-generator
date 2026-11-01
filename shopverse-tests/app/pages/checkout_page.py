from playwright.sync_api import Page

from framework.core.actions import PlaywrightActions


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.actions = PlaywrightActions(page)
        self.grocery_link = self.page.get_by_role("link", name="Grocery")
        self.beauty_profile_link = self.page.get_by_role("link", name="Beauty profile")
        self.home_delivery_button = self.page.get_by_role("button", name="Home delivery")
        self.upi_button = self.page.get_by_role("button", name="UPI")
        self.about_us_link = self.page.get_by_role("link", name="About us")
        self.customer_service_chat_link = self.page.locator("app-footer").get_by_role("link", name="Customer service chat")
        self.we_belong_to_something_beautiful = self.page.get_by_role("heading", name="We belong to something beautiful")
        self.india_english_link = self.page.get_by_role("link", name="India \u00b7 English")
        self.order_overview = self.page.get_by_role("heading", name="Order overview")
        self.rewards_link = self.page.get_by_role("link", name="Rewards")
        self.shopverse_link = self.page.get_by_role("link", name="Shopverse home")
        self.input_field = self.page.get_by_placeholder("Email address")
        self.accessibility_link = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.beauty_link = self.page.get_by_role("link", name="Beauty")
        self.orders_link = self.page.get_by_role("link", name="Orders")
        self.mobiles_link = self.page.get_by_role("link", name="Mobiles")
        self.card_expiry_input = self.page.get_by_placeholder("MM/YY")
        self.deals_link = self.page.get_by_role("link", name="Deals")
        self.input_field_3 = self.page.get_by_placeholder("Mobile phone number")
        self.cart_1_link = self.page.get_by_role("link", name="Cart (1)")
        self.shipping_link = self.page.get_by_role("link", name="Shipping")
        self.saved_addresses_link = self.page.get_by_role("link", name="Saved addresses")
        self.terms_of_use_link = self.page.get_by_role("link", name="Terms of Use")
        self.customer_service_chat_link_2 = self.page.locator("app-footer").get_by_role("link", name="Customer service chat")
        self.card_number_input = self.page.get_by_placeholder("4111 1111 1111 1111")
        self.sustainability_link = self.page.get_by_role("link", name="Sustainability")
        self.get_the_app_link = self.page.locator("app-footer").get_by_role("link", name="Get the app")
        self.accessibility_link_2 = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.track_your_order_link = self.page.locator("app-footer").get_by_role("link", name="Track your order")
        self.new_arrivals_link = self.page.get_by_role("link", name="New Arrivals")
        self.place_order_button = self.page.get_by_role("button", name="Place order")
        self.affiliate_program_link = self.page.get_by_role("link", name="Affiliate program")
        self.united_states_english_link = self.page.get_by_role("link", name="United States \u00b7 English")
        self.returns_link = self.page.get_by_role("link", name="Returns")
        self.card_cvv_input = self.page.get_by_placeholder("123")
        self.furniture_link = self.page.get_by_role("link", name="Furniture")
        self.payment_methods_link = self.page.get_by_role("link", name="Payment methods")
        self.privacy_policy_link = self.page.get_by_role("link", name="Privacy Policy")
        self.sneha_my_account_link = self.page.get_by_role("link", name="Sneha My account")
        self.delivery_or_store_pickup_payment = self.page.get_by_role("heading", name="Delivery or store pickup & payment")
        self.track_your_order_link_2 = self.page.locator("app-footer").get_by_role("link", name="Track your order")
        self.find_a_store_link = self.page.locator("app-footer").get_by_role("link", name="Find a store")
        self.orders_track_purchases_link = self.page.get_by_role("link", name="Orders Track purchases")
        self.shop_all_browse_categories_link = self.page.get_by_role("link", name="Shop All Browse categories")
        self.search_button = self.page.get_by_role("button", name="Search products")
        self.pick_up_from_store_button = self.page.get_by_role("button", name="Pick up from store")
        self.sign_up_button = self.page.get_by_role("button", name="Sign up")
        self.kitchen_link = self.page.get_by_role("link", name="Kitchen")
        self.help = self.page.get_by_role("heading", name="Help")
        self.wishlist_link = self.page.get_by_role("link", name="Wishlist")
        self.electronics_link = self.page.get_by_role("link", name="Electronics")
        self.middle_east_english_link = self.page.get_by_role("link", name="Middle East \u00b7 English")
        self.careers_link = self.page.get_by_role("link", name="Careers")
        self.contact_us_link = self.page.get_by_role("link", name="Contact us")
        self.stores_link = self.page.get_by_role("link", name="Stores")
        self.footwear_link = self.page.get_by_role("link", name="Footwear")
        self.find_a_store_link_2 = self.page.locator("app-footer").get_by_role("link", name="Find a store")
        self.continue_button = self.page.get_by_role("button", name="Continue")
        self.card_button = self.page.get_by_role("button", name="Card")
        self.input_field_6 = self.page.get_by_placeholder("Add gate instructions, preferred call note, or landmark.")
        self.manage_addresses_link = self.page.get_by_role("link", name="Manage addresses")
        self.sitemap_link = self.page.get_by_role("link", name="Sitemap")
        self.radio = self.page.get_by_role("radio", name="Sneha Reddy \u2022 9988776655 Default Villa 22, Green Meadows, Gachibowli Near Financial District Hyderabad, Telangana - 500032 India")
        self.saved_address_radio_buttons = self.page.get_by_role("radio")
        self.get_the_app_link_2 = self.page.locator("app-footer").get_by_role("link", name="Get the app")
        self.logout_button = self.page.get_by_role("button", name="Logout")
        self.cash_on_delivery_pickup_button = self.page.get_by_role("button", name="Cash on delivery / pickup")
        self.track_your_order_link_3 = self.page.locator("app-footer").get_by_role("link", name="Track your order")
        self.cardholder_name_input = self.page.get_by_placeholder("Name on card")
        self.smart_home_link = self.page.get_by_role("link", name="Smart Home")
        self.canada_english_link = self.page.get_by_role("link", name="Canada \u00b7 English")
        self.about_shopverse = self.page.get_by_role("heading", name="About Shopverse")
        self.fashion_link = self.page.get_by_role("link", name="Fashion")
        self.home_appliances_link = self.page.get_by_role("link", name="Home Appliances")
        self.input_field_8 = self.page.get_by_role("textbox", name="Search products")

    def enter_card_number(self, card_number: str):
        """
        Enter the card number for payment during checkout. Use when a test requires inputting the 16-digit number from the front of the payment card. The card_number input should match the number as it appears on the card. Use this method when a manual test step requires input payment card.

        Args:
            card_number: The 16-digit card number displayed on the payment card.
        """
        return self.actions.fill(self.card_number_input, card_number)

    def enter_card_expiry(self, expiry_date: str):
        """
        Enter the expiry date for the payment card in MM/YY format during checkout. Use this method to provide the card expiration as requested in test instructions. The expiry_date parameter should be in the expected MM/YY format. Use this method when a manual test step requires input payment card.

        Args:
            expiry_date: Expiration date of the payment card, in MM/YY format.
        """
        return self.actions.fill(self.card_expiry_input, expiry_date)

    def enter_card_cvv(self, cvv: str):
        """
        Enter the CVV security code for the card during checkout. Use when a security code is required for payment authorization. The cvv parameter is the three-digit (or four-digit, for some cards) code typically found on the back of the card. Use this method when a manual test step requires input payment card.

        Args:
            cvv: Card Verification Value, usually a three-digit code from the back of the card.
        """
        return self.actions.fill(self.card_cvv_input, cvv)

    def enter_cardholder_name(self, cardholder_name: str):
        """
        Enter the name of the cardholder during payment in checkout. Use if the test scenario instructs to provide the exact name as printed on the payment card. The cardholder_name input should reflect the card's displayed name precisely. Use this method when a manual test step requires input payment card.

        Args:
            cardholder_name: Full name as displayed on the payment card.
        """
        return self.actions.fill(self.cardholder_name_input, cardholder_name)

    def select_card_payment(self):
        if self.card_button.get_attribute("aria-pressed") != "true":
            self.actions.click(self.card_button)

    def place_order(self):
        """
        Submit the checkout form and place the order. Use this after all payment and delivery details are provided and the test step instructs to complete the purchase. The expected outcome is that the order is submitted and the user is navigated to the Orders page. Use this method when a manual test step requires commit order.
        """
        return self.actions.click(self.place_order_button)

    def verify_we_belong_to_something_beautiful_heading(self):
        """
        Verify the heading on PAGE_350093949dc3d881 using the observed expected value/text 'We belong to something beautiful'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: We belong to something beautiful
        """
        return self.actions.expect_visible(self.we_belong_to_something_beautiful)
    def verify_help_heading(self):
        """
        Verify the heading on PAGE_350093949dc3d881 using the observed expected value/text 'Help'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Help
        """
        return self.actions.expect_visible(self.help)
    def verify_order_overview_heading(self):
        """
        Verify the heading on PAGE_350093949dc3d881 using the observed expected value/text 'Order overview'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Order overview
        """
        return self.actions.expect_visible(self.order_overview)
    def verify_about_shopverse_heading(self):
        """
        Verify the heading on PAGE_350093949dc3d881 using the observed expected value/text 'About Shopverse'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: About Shopverse
        """
        return self.actions.expect_visible(self.about_shopverse)
    def verify_delivery_or_store_pickup_payment_heading(self):
        """
        Verify the heading on PAGE_350093949dc3d881 using the observed expected value/text 'Delivery or store pickup & payment'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Delivery or store pickup & payment
        """
        return self.actions.expect_visible(self.delivery_or_store_pickup_payment)

    # Generated deterministically from synchronized M2A Application Knowledge evidence.
