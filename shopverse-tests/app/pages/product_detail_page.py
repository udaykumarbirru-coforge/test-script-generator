from playwright.sync_api import Page

from framework.core.actions import PlaywrightActions


class ProductDetailPage:
    def __init__(self, page: Page):
        self.page = page
        self.actions = PlaywrightActions(page)
        self.search_button = self.page.get_by_role("button", name="Search products")
        self.middle_east_english_link = self.page.get_by_role("link", name="Middle East \u00b7 English")
        self.sitemap_link = self.page.get_by_role("link", name="Sitemap")
        self.orders_link = self.page.get_by_role("link", name="Orders")
        self.careers_link = self.page.get_by_role("link", name="Careers")
        self.mobiles_link = self.page.get_by_role("link", name="Mobiles")
        self.customer_service_chat_link = self.page.get_by_role("link", name="Customer service chat")
        self.footwear_link = self.page.get_by_role("link", name="Footwear")
        self.shop_all_browse_categories_link = self.page.get_by_role("link", name="Shop All Browse categories")
        self.region_language = self.page.get_by_role("heading", name="Region & language")
        self.wishlist_link = self.page.get_by_role("link", name="Wishlist")
        self.about_shopverse = self.page.get_by_role("heading", name="About Shopverse")
        self.men_go_walk_arch_fit_hands_free = self.page.get_by_role("heading", name="Men \u00b7 GO WALK ARCH FIT - HANDS FREE")
        self.shipping_link = self.page.get_by_role("link", name="Shipping")
        self.input_field = self.page.get_by_placeholder("Mobile phone number")
        self.about_us_link = self.page.get_by_role("link", name="About us")
        self.affiliate_program_link = self.page.get_by_role("link", name="Affiliate program")
        self.furniture_link = self.page.get_by_role("link", name="Furniture")
        self.saved_addresses_link = self.page.get_by_role("link", name="Saved addresses")
        self.deals_link = self.page.get_by_role("link", name="Deals")
        self.stores_link = self.page.get_by_role("link", name="Stores")
        self.spinbutton = self.page.locator("[data-pc-extend=\"inputtext\"]")
        self.logout_button = self.page.get_by_role("button", name="Logout")
        self.accessibility_link = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.payment_methods_link = self.page.get_by_role("link", name="Payment methods")
        self.beauty_link = self.page.get_by_role("link", name="Beauty")
        self.fashion_link = self.page.get_by_role("link", name="Fashion")
        self.continue_button = self.page.get_by_role("button", name="Continue")
        self.find_a_store_link = self.page.get_by_role("link", name="Find a store")
        self.orders_track_purchases_link = self.page.get_by_role("link", name="Orders Track purchases")
        self.we_belong_to_something_beautiful = self.page.get_by_role("heading", name="We belong to something beautiful")
        self.sign_up_button = self.page.get_by_role("button", name="Sign up")
        self.help = self.page.get_by_role("heading", name="Help")
        self.input_field_2 = self.page.get_by_placeholder("Email address")
        self.input_field_3 = self.page.get_by_role("textbox", name="Search products")
        self.sneha_my_account_link = self.page.get_by_role("link", name="Sneha My account")
        self.electronics_link = self.page.get_by_role("link", name="Electronics")
        self.kitchen_link = self.page.get_by_role("link", name="Kitchen")
        self.contact_us_link = self.page.get_by_role("link", name="Contact us")
        self.beauty_profile_link = self.page.get_by_role("link", name="Beauty profile")
        self.track_your_order_link = self.page.get_by_role("link", name="Track your order")
        self.accessibility_link_2 = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.rewards_link = self.page.get_by_role("link", name="Rewards")
        self.privacy_policy_link = self.page.get_by_role("link", name="Privacy Policy")
        self.cart_1_link = self.page.get_by_role("link", name="Cart (1)")
        self.canada_english_link = self.page.get_by_role("link", name="Canada \u00b7 English")
        self.sustainability_link = self.page.get_by_role("link", name="Sustainability")
        self.home_appliances_link = self.page.get_by_role("link", name="Home Appliances")
        self.returns_link = self.page.get_by_role("link", name="Returns")
        self.smart_home_link = self.page.get_by_role("link", name="Smart Home")
        self.united_states_english_link = self.page.get_by_role("link", name="United States \u00b7 English")
        self.go_to_cart_link = self.page.get_by_role("link", name="Go to cart")
        self.grocery_link = self.page.get_by_role("link", name="Grocery")
        self.india_english_link = self.page.get_by_role("link", name="India \u00b7 English")
        self.get_the_app_link = self.page.get_by_role("link", name="Get the app")
        self.cart_0_link = self.page.get_by_role("link", name="Cart (0)")
        self.terms_of_use_link = self.page.get_by_role("link", name="Terms of Use")
        self.new_arrivals_link = self.page.get_by_role("link", name="New Arrivals")
        self.add_to_cart_button = self.page.get_by_role("button", name="Add to cart")
        self.shopverse_link = self.page.get_by_role("link", name="Shopverse home")

    def add_product_to_cart(self):
        """
        Add the currently viewed product to the shopping cart. Use this method when a manual test step requires placing the visible product shown on the detail page into the cart. The expected outcome is that the product is added to the cart, which is often indicated by a cart icon update or notification. Use this method when a manual test step requires adding product.
        """
        return self.actions.click(self.add_to_cart_button)

    def open_cart(self):
        """
        Navigate from the product detail page to the shopping cart page. Use this method when a manual test step asks to view the cart, go to the cart page, or review items in the shopping cart. The expected user-visible outcome is that the shopping cart view is opened with its contents displayed. Use this method when a manual test step requires navigating to shopping cart.
        """
        return self.actions.click(self.go_to_cart_link)

    def verify_about_shopverse_heading(self):
        """
        Verify the heading on PAGE_10f508a60ab50c5a using the observed expected value/text 'About Shopverse'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: About Shopverse
        """
        return self.actions.expect_visible(self.about_shopverse)
    def verify_men_go_walk_arch_fit_hands_free_heading(self):
        """
        Verify the heading on PAGE_10f508a60ab50c5a using the observed expected value/text 'Men · GO WALK ARCH FIT - HANDS FREE'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Men · GO WALK ARCH FIT - HANDS FREE
        """
        return self.actions.expect_visible(self.men_go_walk_arch_fit_hands_free)
    def verify_we_belong_to_something_beautiful_heading(self):
        """
        Verify the heading on PAGE_10f508a60ab50c5a using the observed expected value/text 'We belong to something beautiful'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: We belong to something beautiful
        """
        return self.actions.expect_visible(self.we_belong_to_something_beautiful)
    def verify_region_language_heading(self):
        """
        Verify the heading on PAGE_10f508a60ab50c5a using the observed expected value/text 'Region & language'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Region & language
        """
        return self.actions.expect_visible(self.region_language)
    def verify_help_heading(self):
        """
        Verify the heading on PAGE_10f508a60ab50c5a using the observed expected value/text 'Help'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Help
        """
        return self.actions.expect_visible(self.help)

    # Generated deterministically from synchronized M2A Application Knowledge evidence.
