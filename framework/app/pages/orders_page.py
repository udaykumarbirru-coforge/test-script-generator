import re

from playwright.sync_api import Page

from framework.core.actions import PlaywrightActions


class OrdersPage:
    def __init__(self, page: Page):
        self.page = page
        self.actions = PlaywrightActions(page)
        self.mobiles_link = self.page.get_by_role("link", name="Mobiles")
        self.deals_link = self.page.get_by_role("link", name="Deals")
        self.furniture_link = self.page.get_by_role("link", name="Furniture")
        self.my_orders = self.page.get_by_role("heading", name="My orders")
        self.grocery_link = self.page.get_by_role("link", name="Grocery")
        self.shop_all_browse_categories_link = self.page.get_by_role("link", name="Shop All Browse categories")
        self.beauty_link = self.page.get_by_role("link", name="Beauty")
        self.home_delivery = self.page.get_by_text("HOME DELIVERY")
        self.orders_track_purchases_link = self.page.get_by_role("link", name="Orders Track purchases")
        self.footwear_link = self.page.get_by_role("link", name="Footwear")
        self.logout_button = self.page.get_by_role("button", name="Logout")
        self.smart_home_link = self.page.get_by_role("link", name="Smart Home")
        self.kitchen_link = self.page.get_by_role("link", name="Kitchen")
        self.sneha_my_account_link = self.page.get_by_role("link", name="Sneha My account")
        self.card_success = self.page.get_by_text("CARD / SUCCESS")
        self.search_button = self.page.get_by_role("button", name="Search products")
        self.home_appliances_link = self.page.get_by_role("link", name="Home Appliances")
        self.shopverse_link = self.page.get_by_role("link", name="Shopverse home")
        self.fashion_link = self.page.get_by_role("link", name="Fashion")
        self.cart_0_link = self.page.get_by_role("link", name="Cart (0)")
        self.cart_link = self.page.get_by_role(
            "link", name=re.compile(r"Cart \(\d+\)")
        )
        self.electronics_link = self.page.get_by_role("link", name="Electronics")
        self.home_delivery_2 = self.page.get_by_text("HOME DELIVERY")
        self.new_arrivals_link = self.page.get_by_role("link", name="New Arrivals")
        self.input_field = self.page.get_by_role("textbox", name="Search products")
        self.store_pickup = self.page.get_by_text("STORE PICKUP")

    def open_shopping_cart(self):
        return self.actions.click(self.cart_link)

    def logout(self):
        """
        Logs the user out of their account and redirects from the Orders Page to the Home Page. Use this method when a test step specifies user logout, session end, or signing out. The expected outcome is that the user's session is ended and they are returned to the landing or home page. Use this method when a manual test step requires signing out of user session.
        """
        return self.actions.click(self.logout_button)

    def verify_home_delivery_visible(self):
        """
        Verify the text on PAGE_e43fced2d541405e using the observed expected value/text 'HOME DELIVERY'. Use this method when a manual test step needs to validate ui text (text). It confirms that the expected UI evidence is visible.

        Expected evidence: HOME DELIVERY
        """
        return self.actions.expect_visible(self.home_delivery)
    def verify_success_message(self):
        """
        Verify the success message on PAGE_e43fced2d541405e using the observed expected value/text 'CARD / SUCCESS'. Use this method when a manual test step needs to validate success message (success message). It confirms that the expected UI evidence is visible.

        Expected evidence: CARD / SUCCESS
        """
        return self.actions.expect_visible(self.card_success)
    def verify_my_orders_heading(self):
        """
        Verify the heading on PAGE_e43fced2d541405e using the observed expected value/text 'My orders'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: My orders
        """
        return self.actions.expect_visible(self.my_orders)
    def verify_store_pickup_visible(self):
        """
        Verify the text on PAGE_e43fced2d541405e using the observed expected value/text 'STORE PICKUP'. Use this method when a manual test step needs to validate ui text (text). It confirms that the expected UI evidence is visible.

        Expected evidence: STORE PICKUP
        """
        return self.actions.expect_visible(self.store_pickup)

    # Generated deterministically from synchronized M2A Application Knowledge evidence.
