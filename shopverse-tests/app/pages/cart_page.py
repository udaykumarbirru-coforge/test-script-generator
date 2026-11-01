from playwright.sync_api import Page

from framework.core.actions import PlaywrightActions


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.actions = PlaywrightActions(page)
        self.sustainability_link = self.page.get_by_role("link", name="Sustainability")
        self.new_arrivals_link = self.page.get_by_role("link", name="New Arrivals")
        self.stores_link = self.page.get_by_role("link", name="Stores")
        self.remove_button = self.page.get_by_role("button", name="Remove")
        self.about_us_link = self.page.get_by_role("link", name="About us")
        self.wishlist_link = self.page.get_by_role("link", name="Wishlist")
        self.shopverse_link = self.page.get_by_role("link", name="Shopverse home")
        self.input_field = self.page.get_by_role("textbox", name="Promo code")
        self.search_button = self.page.get_by_role("button", name="Search products")
        self.logout_button = self.page.get_by_role("button", name="Logout")
        self.input_field_2 = self.page.get_by_placeholder("Mobile phone number")
        self.middle_east_english_link = self.page.get_by_role("link", name="Middle East \u00b7 English")
        self.sign_up_button = self.page.get_by_role("button", name="Sign up")
        self.find_a_store_link = self.page.get_by_role("link", name="Find a store")
        self.careers_link = self.page.get_by_role("link", name="Careers")
        self.smart_home_link = self.page.get_by_role("link", name="Smart Home")
        self.deals_link = self.page.get_by_role("link", name="Deals")
        self.proceed_to_checkout_link = self.page.get_by_role("link", name="Proceed to checkout")
        self.payment_methods_link = self.page.get_by_role("link", name="Payment methods")
        self.accessibility_link = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.spinbutton = self.page.locator("[data-pc-extend=\"inputtext\"]")
        self.sneha_my_account_link = self.page.get_by_role("link", name="Sneha My account")
        self.contact_us_link = self.page.get_by_role("link", name="Contact us")
        self.rewards_link = self.page.get_by_role("link", name="Rewards")
        self.input_field_3 = self.page.get_by_placeholder("Email address")
        self.kitchen_link = self.page.get_by_role("link", name="Kitchen")
        self.sitemap_link = self.page.get_by_role("link", name="Sitemap")
        self.orders_link = self.page.get_by_role("link", name="Orders")
        self.continue_button = self.page.get_by_role("button", name="Continue")
        self.india_english_link = self.page.get_by_role("link", name="India \u00b7 English")
        self.affiliate_program_link = self.page.get_by_role("link", name="Affiliate program")
        self.region_language = self.page.get_by_role("heading", name="Region & language")
        self.shopping_cart = self.page.get_by_role("heading", name="Shopping cart")
        self.men_go_walk_arch_fit_hands_free_link = self.page.get_by_role("link", name="Men \u00b7 GO WALK ARCH FIT - HANDS FREE")
        self.shipping_link = self.page.get_by_role("link", name="Shipping")
        self.footwear_link = self.page.get_by_role("link", name="Footwear")
        self.shop_all_browse_categories_link = self.page.get_by_role("link", name="Shop All Browse categories")
        self.terms_of_use_link = self.page.get_by_role("link", name="Terms of Use")
        self.customer_service_chat_link = self.page.get_by_role("link", name="Customer service chat")
        self.accessibility_link_2 = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.grocery_link = self.page.get_by_role("link", name="Grocery")
        self.orders_track_purchases_link = self.page.get_by_role("link", name="Orders Track purchases")
        self.returns_link = self.page.get_by_role("link", name="Returns")
        self.we_belong_to_something_beautiful = self.page.get_by_role("heading", name="We belong to something beautiful")
        self.continue_shopping_link = self.page.get_by_role("link", name="Continue shopping")
        self.electronics_link = self.page.get_by_role("link", name="Electronics")
        self.home_appliances_link = self.page.get_by_role("link", name="Home Appliances")
        self.cart_link = self.page.get_by_role("link", name="Cart (1)")
        self.input_field_4 = self.page.get_by_role("textbox", name="Search products")
        self.canada_english_link = self.page.get_by_role("link", name="Canada \u00b7 English")
        self.track_your_order_link = self.page.get_by_role("link", name="Track your order")
        self.add_more_items_link = self.page.get_by_role("link", name="Add more items")
        self.beauty_link = self.page.get_by_role("link", name="Beauty")
        self.apply_button = self.page.get_by_role("button", name="Apply")
        self.saved_addresses_link = self.page.get_by_role("link", name="Saved addresses")
        self.beauty_profile_link = self.page.get_by_role("link", name="Beauty profile")
        self.mobiles_link = self.page.get_by_role("link", name="Mobiles")
        self.fashion_link = self.page.get_by_role("link", name="Fashion")
        self.my_account = self.page.get_by_role("heading", name="My account")
        self.subtotal = self.page.get_by_role("heading", name="Subtotal")
        self.get_the_app_link = self.page.get_by_role("link", name="Get the app")
        self.privacy_policy_link = self.page.get_by_role("link", name="Privacy Policy")
        self.furniture_link = self.page.get_by_role("link", name="Furniture")
        self.united_states_english_link = self.page.get_by_role("link", name="United States \u00b7 English")

    def open_shopping_cart(self):
        """
        Navigate to and view the shopping cart page. Use this method when a manual test step asks to view the cart, access cart contents, or check items currently in the cart. The expected outcome is that the shopping cart page becomes visible to the user. Use this method when a manual test step requires navigating to shopping cart.
        """
        return self.actions.click(self.cart_link)

    def proceed_to_checkout(self):
        """
        Initiate the checkout process from the shopping cart. Use this method when a manual step requires the user to begin placing an order, start checkout, or move from the cart to the checkout process. The expected outcome is navigation from the cart to the checkout page. Use this method when a manual test step requires commit shopping cart.
        """
        return self.actions.click(self.proceed_to_checkout_link)

    def verify_region_language_heading(self):
        """
        Verify the heading on PAGE_01654344747a5c4e using the observed expected value/text 'Region & language'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Region & language
        """
        return self.actions.expect_visible(self.region_language)
    def verify_we_belong_to_something_beautiful_heading(self):
        """
        Verify the heading on PAGE_01654344747a5c4e using the observed expected value/text 'We belong to something beautiful'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: We belong to something beautiful
        """
        return self.actions.expect_visible(self.we_belong_to_something_beautiful)
    def verify_subtotal_heading(self):
        """
        Verify the heading on PAGE_01654344747a5c4e using the observed expected value/text 'Subtotal'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Subtotal
        """
        return self.actions.expect_visible(self.subtotal)
    def verify_shopping_cart_heading(self):
        """
        Verify the heading on PAGE_01654344747a5c4e using the observed expected value/text 'Shopping cart'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Shopping cart
        """
        return self.actions.expect_visible(self.shopping_cart)
    def verify_my_account_heading(self):
        """
        Verify the heading on PAGE_01654344747a5c4e using the observed expected value/text 'My account'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: My account
        """
        return self.actions.expect_visible(self.my_account)

    # Generated deterministically from synchronized M2A Application Knowledge evidence.
