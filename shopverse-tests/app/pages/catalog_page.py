import re

from playwright.sync_api import Locator, Page

from framework.core.actions import PlaywrightActions


class CatalogPage:
    def __init__(self, page: Page):
        self.page = page
        self.actions = PlaywrightActions(page)
        self.get_the_app_link = self.page.get_by_role("link", name="Get the app")
        self.logout_button = self.page.get_by_role("button", name="Logout")
        self.sign_up_button = self.page.get_by_role("button", name="Sign up")
        self.united_states_english_link = self.page.get_by_role("link", name="United States \u00b7 English")
        self.beauty_link = self.page.get_by_role("link", name="Beauty")
        self.about_us_link = self.page.get_by_role("link", name="About us")
        self.we_belong_to_something_beautiful_heading = self.page.get_by_role("heading", name="We belong to something beautiful")
        self.search_button = self.page.get_by_role("button", name="Search products")
        self.sitemap_link = self.page.get_by_role("link", name="Sitemap")
        self.footwear_link = self.page.get_by_role("link", name="Footwear")
        self.shipping_link = self.page.get_by_role("link", name="Shipping")
        self.back_to_home_link = self.page.get_by_role("link", name="Back to home")
        self.careers_link = self.page.get_by_role("link", name="Careers")
        self.cart_link = self.page.get_by_role("link", name="Cart (0)")
        self.deals_link = self.page.get_by_role("link", name="Deals")
        self.affiliate_program_link = self.page.get_by_role("link", name="Affiliate program")
        self.electronics_link = self.page.get_by_role("link", name="Electronics")
        self.beauty_profile_link = self.page.get_by_role("link", name="Beauty profile")
        self.grocery_link = self.page.get_by_role("link", name="Grocery")
        self.continue_button = self.page.get_by_role("button", name="Continue")
        self.accessibility_link = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.stores_link = self.page.get_by_role("link", name="Stores")
        self.sustainability_link = self.page.get_by_role("link", name="Sustainability")
        self.fashion_link = self.page.get_by_role("link", name="Fashion")
        self.skechers_shoes_heading = self.page.get_by_role("heading", name="Skechers shoes")
        self.mobile_phone_input = self.page.get_by_placeholder("Mobile phone number")
        self.orders_link = self.page.get_by_role("link", name="Orders")
        self.new_arrivals_link = self.page.get_by_role("link", name="New Arrivals")
        self.payment_methods_link = self.page.get_by_role("link", name="Payment methods")
        self.customer_service_chat_link = self.page.get_by_role("link", name="Customer service chat")
        self.my_account_link = self.page.get_by_role("link", name="Sneha My account")
        self.find_a_store_link = self.page.get_by_role("link", name="Find a store")
        self.region_language_heading = self.page.get_by_role("heading", name="Region & language")
        self.saved_addresses_link = self.page.get_by_role("link", name="Saved addresses")
        self.home_appliances_link = self.page.get_by_role("link", name="Home Appliances")
        self.email_input = self.page.get_by_placeholder("Email address")
        self.middle_east_english_link = self.page.get_by_role("link", name="Middle East \u00b7 English")
        self.furniture_link = self.page.get_by_role("link", name="Furniture")
        self.contact_us_link = self.page.get_by_role("link", name="Contact us")
        self.india_english_link = self.page.get_by_role("link", name="India \u00b7 English")
        self.orders_track_purchases_link = self.page.get_by_role("link", name="Orders Track purchases")
        self.no_products_found_heading = self.page.get_by_role("heading", name="No products found")
        self.terms_of_use_link = self.page.get_by_role("link", name="Terms of Use")
        self.mobiles_link = self.page.get_by_role("link", name="Mobiles")
        self.returns_link = self.page.get_by_role("link", name="Returns")
        self.my_account_heading = self.page.get_by_role("heading", name="My account")
        self.wishlist_link = self.page.get_by_role("link", name="Wishlist")
        self.canada_english_link = self.page.get_by_role("link", name="Canada \u00b7 English")
        self.kitchen_link = self.page.get_by_role("link", name="Kitchen")
        self.smart_home_link = self.page.get_by_role("link", name="Smart Home")
        self.privacy_policy_link = self.page.get_by_role("link", name="Privacy Policy")
        self.product_search_input = self.page.get_by_role("textbox", name="Search products")
        self.product_cards = self.page.locator("app-product-card")
        self.rewards_link = self.page.get_by_role("link", name="Rewards")
        self.shop_all_browse_categories_link = self.page.get_by_role("link", name="Shop All Browse categories")
        self.shopverse_link = self.page.get_by_role("link", name="Shopverse home")
        self.track_your_order_link = self.page.get_by_role("link", name="Track your order")
        self.accessibility_link_2 = self.page.locator("app-footer").get_by_role("link", name="Accessibility")

    def open_cart(self):
        """
        Open the shopping cart page. Use this method when a manual step asks to view the user cart, with the expected outcome that the cart view is opened to display current cart items. Use this method when a manual test step requires opening shopping cart.
        """
        return self.actions.click(self.cart_link)

    def logout(self):
        """
        Log out the current user session. Use this method when a manual step requests to sign out, with the expected result that the user session ends and guest or login state is restored. Use this method when a manual test step requires signing out of session.
        """
        return self.actions.click(self.logout_button)

   
  
    def select_product(self, product_name: str):
        """
        Select a pro*uct from the catalog and open its *etails page.
        """
        product_locator = self.page.locator(
            f"a.product-media:has(img[alt*='{product_name}'])"
        )
        self.actions.click(product_locator)

    def open_my_account(self):
        """
        Open the user account overview. Use this method to navigate to the logged-in user's account dashboard, typically to view profile or account options. Use this method when a manual test step requires opening user account.
        """
        return self.actions.click(self.my_account_link)

    def open_orders(self):
        """
        Navigate to the user's orders or order tracking page. Use this method when a manual test step requires reviewing placed orders or tracking purchase status. Use this method when a manual test step requires opening order history.
        """
        return self.actions.click(self.orders_track_purchases_link)

    def search_products(self, query: str):
        """
        Search for products by entering a query and submitting the search. Use this method when a manual test step asks to search the catalog with specific keywords. The 'query' input is submitted using the visible product search field and its associated search button; the expected outcome is that search results matching the query are displayed. Use this method when a manual test step requires searching for product. It completes the related multi-control interaction as one reusable business operation.

        Args:
            query: Text used to search for products.
        """
        self.actions.fill(self.product_search_input, query)
        return self.actions.click(self.search_button)

    def product_card_for(self, product_name: str) -> Locator:
        return self.product_cards.filter(has_text=product_name)

    def open_product_details(self, product_name: str):
        product_link = self.product_card_for(product_name).locator("a.product-title")
        return self.actions.click(product_link)

    def add_product_to_cart_from_results(self, product_name: str):
        add_to_cart_button = self.product_card_for(product_name).get_by_role(
            "button", name=re.compile(r"Add(?: .+)? to cart", re.IGNORECASE)
        )
        return self.actions.click(add_to_cart_button)

    def verify_my_account_heading(self):
        """
        Verify the heading on PAGE_78f9223d6ed3d264 using the observed expected value/text 'My account'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: My account
        """
        return self.actions.expect_visible(self.my_account_heading)
    def verify_we_belong_to_something_beautiful_heading(self):
        """
        Verify the heading on PAGE_78f9223d6ed3d264 using the observed expected value/text 'We belong to something beautiful'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: We belong to something beautiful
        """
        return self.actions.expect_visible(self.we_belong_to_something_beautiful_heading)
    def verify_region_language_heading(self):
        """
        Verify the heading on PAGE_78f9223d6ed3d264 using the observed expected value/text 'Region & language'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Region & language
        """
        return self.actions.expect_visible(self.region_language_heading)
    def verify_skechers_shoes_heading(self):
        """
        Verify the heading on PAGE_78f9223d6ed3d264 using the observed expected value/text 'Skechers shoes'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Skechers shoes
        """
        return self.actions.expect_visible(self.skechers_shoes_heading)
    def verify_no_products_found_heading(self):
        """
        Verify the heading on PAGE_78f9223d6ed3d264 using the observed expected value/text 'No products found'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: No products found
        """
        return self.actions.expect_visible(self.no_products_found_heading)

    # Generated deterministically from synchronized M2A Application Knowledge evidence.
