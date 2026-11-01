from playwright.sync_api import Page

from framework.core.actions import PlaywrightActions


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.actions = PlaywrightActions(page)
        self.about_us_link = self.page.get_by_role("link", name="About us")
        self.privacy_policy_link = self.page.get_by_role("link", name="Privacy Policy")
        self.get_the_app_link = self.page.get_by_role("link", name="Get the app")
        self.sign_in_access_your_account_link = self.page.get_by_role("link", name="Sign In Access your account")
        self.beauty_profile_link = self.page.get_by_role("link", name="Beauty profile")
        self.wishlist_link = self.page.get_by_role("link", name="Wishlist")
        self.shipping_link = self.page.get_by_role("link", name="Shipping")
        self.accessibility_link = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.search_button = self.page.get_by_role("button", name="Search products")
        self.find_a_store_link = self.page.get_by_role("link", name="Find a store")
        self.home_appliances_link = self.page.get_by_role("link", name="Home Appliances")
        self.login_button = self.page.get_by_role("button", name="Login")
        self.sitemap_link = self.page.get_by_role("link", name="Sitemap")
        self.smart_home_link = self.page.get_by_role("link", name="Smart Home")
        self.shop_all_browse_categories_link = self.page.get_by_role("link", name="Shop All Browse categories")
        self.canada_english_link = self.page.get_by_role("link", name="Canada \u00b7 English")
        self.password_input = self.page.locator("[data-pc-extend=\"inputtext\"]")
        self.sign_in_to_continue_shopping = self.page.get_by_role("heading", name="Sign in to continue shopping")
        self.india_english_link = self.page.get_by_role("link", name="India \u00b7 English")
        self.returns_link = self.page.get_by_role("link", name="Returns")
        self.saved_addresses_link = self.page.get_by_role("link", name="Saved addresses")
        self.deals_link = self.page.get_by_role("link", name="Deals")
        self.my_account = self.page.get_by_role("heading", name="My account")
        self.new_user_create_an_account_link = self.page.get_by_role("link", name="New user? Create an account")
        self.stores_link = self.page.get_by_role("link", name="Stores")
        self.united_states_english_link = self.page.get_by_role("link", name="United States \u00b7 English")
        self.electronics_link = self.page.get_by_role("link", name="Electronics")
        self.fashion_link = self.page.get_by_role("link", name="Fashion")
        self.orders_link = self.page.get_by_role("link", name="Orders")
        self.sign_up_button = self.page.get_by_role("button", name="Sign up")
        self.sustainability_link = self.page.get_by_role("link", name="Sustainability")
        self.input_field_2 = self.page.get_by_placeholder("Mobile phone number")
        self.email_input = self.page.get_by_placeholder("Enter email address")
        self.rewards_link = self.page.get_by_role("link", name="Rewards")
        self.contact_us_link = self.page.get_by_role("link", name="Contact us")
        self.input_field_4 = self.page.get_by_placeholder("Email address")
        self.cart_0_link = self.page.get_by_role("link", name="Cart (0)")
        self.affiliate_program_link = self.page.get_by_role("link", name="Affiliate program")
        self.help = self.page.get_by_role("heading", name="Help")
        self.input_field_5 = self.page.get_by_role("textbox", name="Search products")
        self.continue_button = self.page.get_by_role("button", name="Continue")
        self.careers_link = self.page.get_by_role("link", name="Careers")
        self.accessibility_link_2 = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.payment_methods_link = self.page.get_by_role("link", name="Payment methods")
        self.customer_service_chat_link = self.page.get_by_role("link", name="Customer service chat")
        self.furniture_link = self.page.get_by_role("link", name="Furniture")
        self.region_language = self.page.get_by_role("heading", name="Region & language")
        self.terms_of_use_link = self.page.get_by_role("link", name="Terms of Use")
        self.shopverse_link = self.page.get_by_role("link", name="Shopverse home")
        self.kitchen_link = self.page.get_by_role("link", name="Kitchen")
        self.beauty_link = self.page.get_by_role("link", name="Beauty")
        self.mobiles_link = self.page.get_by_role("link", name="Mobiles")
        self.we_belong_to_something_beautiful = self.page.get_by_role("heading", name="We belong to something beautiful")
        self.new_arrivals_link = self.page.get_by_role("link", name="New Arrivals")
        self.middle_east_english_link = self.page.get_by_role("link", name="Middle East \u00b7 English")
        self.footwear_link = self.page.get_by_role("link", name="Footwear")
        self.grocery_link = self.page.get_by_role("link", name="Grocery")
        self.track_your_order_link = self.page.get_by_role("link", name="Track your order")

    def login_with_email_and_password(self, email_address: str, password: str):
        """
        Authenticate a user by entering the supplied email address and password, then submit the login form. Use this method when a manual step asks to log in or sign in with credentials. It completes the full login sequence and transitions to a logged-in state (e.g., home page) upon successful authentication. Use this method when a manual test step requires authenticating user session. It completes the related multi-control interaction as one reusable business operation.

        Args:
            email_address: The user's email address used for authentication.
            password: The password associated with the email address.
        """
        self.actions.fill(self.email_input, email_address)
        self.actions.fill(self.password_input, password)
        return self.actions.click(self.login_button)

    def verify_help_heading(self):
        """
        Verify the heading on PAGE_ba8152c293558793 using the observed expected value/text 'Help'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Help
        """
        return self.actions.expect_visible(self.help)
    def verify_my_account_heading(self):
        """
        Verify the heading on PAGE_ba8152c293558793 using the observed expected value/text 'My account'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: My account
        """
        return self.actions.expect_visible(self.my_account)
    def verify_region_language_heading(self):
        """
        Verify the heading on PAGE_ba8152c293558793 using the observed expected value/text 'Region & language'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Region & language
        """
        return self.actions.expect_visible(self.region_language)
    def verify_sign_in_to_continue_shopping_heading(self):
        """
        Verify the heading on PAGE_ba8152c293558793 using the observed expected value/text 'Sign in to continue shopping'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Sign in to continue shopping
        """
        return self.actions.expect_visible(self.sign_in_to_continue_shopping)
    def verify_we_belong_to_something_beautiful_heading(self):
        """
        Verify the heading on PAGE_ba8152c293558793 using the observed expected value/text 'We belong to something beautiful'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: We belong to something beautiful
        """
        return self.actions.expect_visible(self.we_belong_to_something_beautiful)

    # Generated deterministically from synchronized M2A Application Knowledge evidence.
