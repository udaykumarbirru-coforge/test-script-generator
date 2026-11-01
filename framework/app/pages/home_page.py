import re

from playwright.sync_api import Page

from framework.core.actions import PlaywrightActions


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.actions = PlaywrightActions(page)
        self.explore_link = self.page.locator("app-home-page").get_by_role("link", name="Explore")
        self.add_to_cart_button = self.page.locator("app-product-card").get_by_role("button", name="Add Men \u00b7 GO WALK MAX CUSHIONING ARCH FIT - JESPER to cart")
        self.link_link = self.page.locator("[href=\"#/product/new-balance-men-fresh-foam-x-1080-v14\"]")
        self.men_asics_gel_kayano_31_link = self.page.locator("app-product-card").get_by_role("link", name="Men \u00b7 ASICS GEL-KAYANO 31")
        self.about_shopverse = self.page.get_by_role("heading", name="About Shopverse")
        self.top_electronics_electronics_browse_laptops_headphones_speakers_and_smart_enterta = self.page.get_by_role("link", name="TOP ELECTRONICS Electronics Browse laptops, headphones, speakers and smart entertainment picks in one curated shelf. SHOP NOW")
        self.fashion_link = self.page.locator("app-header").get_by_role("link", name="Fashion")
        self.sustainability_link = self.page.locator("app-footer").get_by_role("link", name="Sustainability")
        self.men_go_walk_max_cushioning_arch_fit_jesper_link = self.page.locator("app-product-card").get_by_role("link", name="Men \u00b7 GO WALK MAX CUSHIONING ARCH FIT - JESPER")
        self.men_go_walk_max_cushioning_arch_fit_jesper_link_2 = self.page.locator("app-product-card").get_by_role("link", name="Men \u00b7 GO WALK MAX CUSHIONING ARCH FIT - JESPER")
        self.stores_link = self.page.locator("app-footer").get_by_role("link", name="Stores")
        self.furniture_link = self.page.locator("app-header").get_by_role("link", name="Furniture")
        self.returns_link = self.page.locator("app-footer").get_by_role("link", name="Returns")
        self.home_appliances_link = self.page.locator("app-home-page").get_by_role("link", name="Home Appliances")
        self.just_dropped_new_arrivals_explore_fresh_marketplace_launches_across_phones_appli = self.page.get_by_role("link", name="JUST DROPPED New Arrivals Explore fresh marketplace launches across phones, appliances, beauty and daily-use essentials. SHOP NOW")
        self.add_to_cart_button_2 = self.page.locator("app-product-card").get_by_role("button", name="Add Men \u00b7 GO WALK ARCH FIT - HANDS FREE to cart")
        self.link_link_2 = self.page.locator("[href=\"#/product/performance-go-run-ride-11\"]")
        self.wishlist_link = self.page.locator("app-footer").get_by_role("link", name="Wishlist")
        self.new_arrivals = self.page.get_by_role("heading", name="New Arrivals")
        self.men_go_walk_arch_fit_hands_free_link = self.page.locator("app-product-card").get_by_role("link", name="Men \u00b7 GO WALK ARCH FIT - HANDS FREE")
        self.orders_link = self.page.locator("app-footer").get_by_role("link", name="Orders")
        self.home_upgrades_home_appliances_discover_vacuums_air_fryers_washers_and_premium_ap = self.page.get_by_role("link", name="HOME UPGRADES Home Appliances Discover vacuums, air fryers, washers and premium appliances for practical everyday living. SHOP NOW")
        self.add_to_cart_button_3 = self.page.locator("app-product-card").get_by_role("button", name="Add Performance \u00b7 GO RUN RIDE 11 to cart")
        self.add_to_cart_button_4 = self.page.locator("app-product-card").get_by_role("button", name="Add Unisex \u00b7 adidas Samba OG to cart")
        self.product_search_input = self.page.get_by_role("textbox", name="Search products")
        self.india_english_link = self.page.locator("app-footer").get_by_role("link", name="India \u00b7 English")
        self.deals_link = self.page.get_by_role("link", name="Deals")
        self.men_go_walk_arch_fit_2_link = self.page.locator("app-product-card").get_by_role("link", name="Men \u00b7 GO WALK ARCH FIT 2")
        self.accessibility_link = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.unisex_nike_air_force_1_07_link = self.page.locator("app-product-card").get_by_role("link", name="Unisex \u00b7 Nike Air Force 1 07")
        self.get_the_app_link = self.page.locator("app-footer").get_by_role("link", name="Get the app")
        self.contact_us_link = self.page.locator("app-footer").get_by_role("link", name="Contact us")
        self.sign_up_button = self.page.get_by_role("button", name="Sign up")
        self.link_link_3 = self.page.locator("[href=\"#/product/adidas-unisex-samba-og\"]")
        self.add_to_cart_button_5 = self.page.locator("app-product-card").get_by_role("button", name="Add Men \u00b7 New Balance Fresh Foam X 1080 v14 to cart")
        self.customer_service_chat_link = self.page.locator("app-footer").get_by_role("link", name="Customer service chat")
        self.track_your_order_link = self.page.locator("app-footer").get_by_role("link", name="Track your order")
        self.customer_service_chat_link_2 = self.page.locator("app-footer").get_by_role("link", name="Customer service chat")
        self.sneha_my_account_link = self.page.get_by_role("link", name="Sneha My account")
        self.account_menu_link = self.page.get_by_role(
            "link", name=re.compile(r".+ My account")
        )
        self.furniture_link_2 = self.page.locator("app-home-page").get_by_role("link", name="Furniture")
        self.sitemap_link = self.page.get_by_role("link", name="Sitemap")
        self.link_link_4 = self.page.locator("[href=\"#/product/performance-go-run-ride-11\"]")
        self.link_link_5 = self.page.locator("[href=\"#/product/asics-men-gel-kayano-31\"]")
        self.terms_of_use_link = self.page.locator("app-footer").get_by_role("link", name="Terms of Use")
        self.new_balance_spotlight = self.page.get_by_role("heading", name="New Balance spotlight")
        self.grocery_link = self.page.locator("app-home-page").get_by_role("link", name="Grocery")
        self.middle_east_english_link = self.page.locator("app-footer").get_by_role("link", name="Middle East \u00b7 English")
        self.united_states_english_link = self.page.locator("app-footer").get_by_role("link", name="United States \u00b7 English")
        self.add_to_cart_button_6 = self.page.locator("app-product-card").get_by_role("button", name="Add Men \u00b7 ASICS GEL-KAYANO 31 to cart")
        self.payment_methods_link = self.page.locator("app-footer").get_by_role("link", name="Payment methods")
        self.stores_link_2 = self.page.locator("app-footer").get_by_role("link", name="Stores")
        self.men_go_walk_arch_fit_hands_free_link_2 = self.page.locator("app-product-card").get_by_role("link", name="Men \u00b7 GO WALK ARCH FIT - HANDS FREE")
        self.add_to_cart_button_7 = self.page.locator("app-product-card").get_by_role("button", name="Add Men \u00b7 GO WALK ARCH FIT 2 to cart")
        self.input_field_2 = self.page.get_by_placeholder("Email address")
        self.payment_methods_link_2 = self.page.locator("app-footer").get_by_role("link", name="Payment methods")
        self.view_all_link = self.page.get_by_role("link", name="View all")
        self.explore_link_2 = self.page.locator("app-home-page").get_by_role("link", name="Explore")
        self.beauty_profile_link = self.page.locator("app-footer").get_by_role("link", name="Beauty profile")
        self.link_link_6 = self.page.locator("[href=\"#/product/men-go-walk-arch-fit-2\"]")
        self.add_to_cart_button_8 = self.page.locator("app-product-card").get_by_role("button", name="Add Men \u00b7 ASICS GEL-KAYANO 31 to cart")
        self.just_dropped = self.page.get_by_role("heading", name="Just dropped")
        self.add_to_cart_button_9 = self.page.locator("app-product-card").get_by_role("button", name="Add Unisex \u00b7 adidas Samba OG to cart")
        self.men_new_balance_fresh_foam_x_1080_v14_link = self.page.locator("app-product-card").get_by_role("link", name="Men \u00b7 New Balance Fresh Foam X 1080 v14")
        self.performance_go_run_ride_11_link = self.page.locator("app-product-card").get_by_role("link", name="Performance \u00b7 GO RUN RIDE 11")
        self.beauty_profile_link_2 = self.page.locator("app-footer").get_by_role("link", name="Beauty profile")
        self.accessibility_link_2 = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.link_link_7 = self.page.locator("[href=\"#/product/new-balance-men-fresh-foam-x-1080-v14\"]")
        self.privacy_policy_link = self.page.locator("app-footer").get_by_role("link", name="Privacy Policy")
        self.link_link_8 = self.page.locator("[href=\"#/product/adidas-unisex-samba-og\"]")
        self.kitchen_link = self.page.locator("app-header").get_by_role("link", name="Kitchen")
        self.affiliate_program_link = self.page.locator("app-footer").get_by_role("link", name="Affiliate program")
        self.new_arrivals_link = self.page.locator("app-home-page").get_by_role("link", name="New Arrivals")
        self.search_button = self.page.get_by_role("button", name="Search products")
        self.terms_of_use_link_2 = self.page.locator("app-footer").get_by_role("link", name="Terms of Use")
        self.footwear_link = self.page.locator("app-home-page").get_by_role("link", name="Footwear")
        self.unisex_adidas_samba_og_link = self.page.locator("app-product-card").get_by_role("link", name="Unisex \u00b7 adidas Samba OG")
        self.cart_0_link = self.page.get_by_role("link", name="Cart (0)")
        self.link_link_9 = self.page.locator("[href=\"#/product/men-go-walk-max-cushioning-arch-fit-jesper\"]")
        self.explore_link_3 = self.page.locator("app-home-page").get_by_role("link", name="Explore")
        self.rewards_link = self.page.locator("app-footer").get_by_role("link", name="Rewards")
        self.men_new_balance_fresh_foam_x_1080_v14_link_2 = self.page.locator("app-product-card").get_by_role("link", name="Men \u00b7 New Balance Fresh Foam X 1080 v14")
        self.electronics_link = self.page.locator("app-header").get_by_role("link", name="Electronics")
        self.add_to_cart_button_10 = self.page.locator("app-product-card").get_by_role("button", name="Add Unisex \u00b7 Nike Air Force 1 07 to cart")
        self.performance_go_run_ride_11_link_2 = self.page.locator("app-product-card").get_by_role("link", name="Performance \u00b7 GO RUN RIDE 11")
        self.beauty_link = self.page.locator("app-home-page").get_by_role("link", name="Beauty")
        self.men_asics_gel_kayano_31_link_2 = self.page.locator("app-product-card").get_by_role("link", name="Men \u00b7 ASICS GEL-KAYANO 31")
        self.link_link_10 = self.page.locator("[href=\"#/product/men-go-walk-arch-fit-hands-free\"]")
        self.home_appliances_link_2 = self.page.locator("app-header").get_by_role("link", name="Home Appliances")
        self.men_go_walk_arch_fit_2_link_2 = self.page.locator("app-product-card").get_by_role("link", name="Men \u00b7 GO WALK ARCH FIT 2")
        self.track_your_order_link_2 = self.page.locator("app-footer").get_by_role("link", name="Track your order")
        self.returns_link_2 = self.page.locator("app-footer").get_by_role("link", name="Returns")
        self.shop_all_browse_categories_link = self.page.get_by_role("link", name="Shop All Browse categories")
        self.careers_link = self.page.locator("app-footer").get_by_role("link", name="Careers")
        self.find_a_store_link = self.page.locator("app-footer").get_by_role("link", name="Find a store")
        self.link_link_11 = self.page.locator("[href=\"#/product/men-go-walk-max-cushioning-arch-fit-jesper\"]")
        self.unisex_adidas_samba_og_link_2 = self.page.locator("app-product-card").get_by_role("link", name="Unisex \u00b7 adidas Samba OG")
        self.wishlist_link_2 = self.page.locator("app-footer").get_by_role("link", name="Wishlist")
        self.shipping_link = self.page.locator("app-footer").get_by_role("link", name="Shipping")
        self.electronics_link_2 = self.page.locator("app-home-page").get_by_role("link", name="Electronics")
        self.add_to_cart_button_11 = self.page.locator("app-product-card").get_by_role("button", name="Add Unisex \u00b7 adidas Samba OG to cart")
        self.smart_home_link = self.page.locator("app-header").get_by_role("link", name="Smart Home")
        self.careers_link_2 = self.page.locator("app-footer").get_by_role("link", name="Careers")
        self.united_states_english_link_2 = self.page.locator("app-footer").get_by_role("link", name="United States \u00b7 English")
        self.sign_in_link = self.page.get_by_role("link", name="Sign In Access your account")
        self.fashion_link_2 = self.page.locator("app-home-page").get_by_role("link", name="Fashion")
        self.unisex_nike_air_force_1_07_link_2 = self.page.locator("app-product-card").get_by_role("link", name="Unisex \u00b7 Nike Air Force 1 07")
        self.shopverse_link = self.page.get_by_role("link", name="Shopverse home")
        self.middle_east_english_link_2 = self.page.locator("app-footer").get_by_role("link", name="Middle East \u00b7 English")
        self.saved_addresses_link = self.page.locator("app-footer").get_by_role("link", name="Saved addresses")
        self.add_to_cart_button_12 = self.page.locator("app-product-card").get_by_role("button", name="Add Men \u00b7 GO WALK ARCH FIT - HANDS FREE to cart")
        self.india_english_link_2 = self.page.locator("app-footer").get_by_role("link", name="India \u00b7 English")
        self.new_arrivals_link_2 = self.page.locator("app-header").get_by_role("link", name="New Arrivals")
        self.grocery_link_2 = self.page.locator("app-header").get_by_role("link", name="Grocery")
        self.add_to_cart_button_13 = self.page.locator("app-product-card").get_by_role("button", name="Add Men \u00b7 GO WALK MAX CUSHIONING ARCH FIT - JESPER to cart")
        self.link_link_12 = self.page.locator("[href=\"#/product/asics-men-gel-kayano-31\"]")
        self.input_field_3 = self.page.get_by_placeholder("Mobile phone number")
        self.link_link_13 = self.page.locator("[href=\"#/product/men-go-walk-arch-fit-hands-free\"]")
        self.get_the_app_link_2 = self.page.locator("app-footer").get_by_role("link", name="Get the app")
        self.add_to_cart_button_14 = self.page.locator("app-product-card").get_by_role("button", name="Add Men \u00b7 GO WALK ARCH FIT 2 to cart")
        self.add_to_cart_button_15 = self.page.locator("app-product-card").get_by_role("button", name="Add Men \u00b7 GO WALK ARCH FIT - HANDS FREE to cart")
        self.orders_track_purchases_link = self.page.get_by_role("link", name="Orders Track purchases")
        self.add_to_cart_button_16 = self.page.locator("app-product-card").get_by_role("button", name="Add Unisex \u00b7 Nike Air Force 1 07 to cart")
        self.smart_home_link_2 = self.page.locator("app-home-page").get_by_role("link", name="Smart Home")
        self.shop_all_link = self.page.get_by_role("link", name="Shop all")
        self.privacy_policy_link_2 = self.page.locator("app-footer").get_by_role("link", name="Privacy Policy")
        self.sustainability_link_2 = self.page.locator("app-footer").get_by_role("link", name="Sustainability")
        self.add_to_cart_button_17 = self.page.locator("app-product-card").get_by_role("button", name="Add Performance \u00b7 GO RUN RIDE 11 to cart")
        self.about_us_link = self.page.locator("app-footer").get_by_role("link", name="About us")
        self.orders_link_2 = self.page.locator("app-footer").get_by_role("link", name="Orders")
        self.logout_button = self.page.get_by_role("button", name="Logout")
        self.kitchen_link_2 = self.page.locator("app-home-page").get_by_role("link", name="Kitchen")
        self.mobiles_link = self.page.locator("app-header").get_by_role("link", name="Mobiles")
        self.find_a_store_link_2 = self.page.locator("app-footer").get_by_role("link", name="Find a store")
        self.accessibility_link_3 = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.canada_english_link = self.page.locator("app-footer").get_by_role("link", name="Canada \u00b7 English")
        self.link_link_14 = self.page.locator("[href=\"#/product/nike-unisex-air-force-1-07\"]")
        self.customer_service_chat_link_3 = self.page.locator("app-footer").get_by_role("link", name="Customer service chat")
        self.continue_button = self.page.get_by_role("button", name="Continue")
        self.link_link_15 = self.page.locator("[href=\"#/product/men-go-walk-arch-fit-2\"]")
        self.accessibility_link_4 = self.page.locator("app-footer").get_by_role("link", name="Accessibility")
        self.link_link_16 = self.page.locator("[href=\"#/product/nike-unisex-air-force-1-07\"]")
        self.contact_us_link_2 = self.page.locator("app-footer").get_by_role("link", name="Contact us")
        self.canada_english_link_2 = self.page.locator("app-footer").get_by_role("link", name="Canada \u00b7 English")
        self.flagship_phones_mobiles_compare_premium_smartphones_foldables_and_value_first_up = self.page.get_by_role("link", name="FLAGSHIP PHONES Mobiles Compare premium smartphones, foldables and value-first upgrades with cleaner category navigation. SHOP NOW")
        self.add_to_cart_button_18 = self.page.locator("app-product-card").get_by_role("button", name="Add Men \u00b7 GO WALK ARCH FIT - HANDS FREE to cart")
        self.beauty_link_2 = self.page.locator("app-header").get_by_role("link", name="Beauty")
        self.add_to_cart_button_19 = self.page.locator("app-product-card").get_by_role("button", name="Add Men \u00b7 New Balance Fresh Foam X 1080 v14 to cart")
        self.about_us_link_2 = self.page.locator("app-footer").get_by_role("link", name="About us")
        self.shipping_link_2 = self.page.locator("app-footer").get_by_role("link", name="Shipping")
        self.footwear_link_2 = self.page.locator("app-header").get_by_role("link", name="Footwear")
        self.rewards_link_2 = self.page.locator("app-footer").get_by_role("link", name="Rewards")
        self.trending_picks = self.page.get_by_role("heading", name="Trending picks")
        self.explore_link_4 = self.page.locator("app-home-page").get_by_role("link", name="Explore")
        self.affiliate_program_link_2 = self.page.locator("app-footer").get_by_role("link", name="Affiliate program")
        self.track_your_order_link_3 = self.page.locator("app-footer").get_by_role("link", name="Track your order")
        self.saved_addresses_link_2 = self.page.locator("app-footer").get_by_role("link", name="Saved addresses")
        self.mobiles_link_2 = self.page.locator("app-home-page").get_by_role("link", name="Mobiles")

    def initiate_sign_in(self):
        """
        Navigate to the sign in page or form to allow user authentication. Use this method when you need to start the login process or access the authentication page from the homepage. The user is expected to see the login screen or form upon completion. Use this method when a manual test step requires navigating to user session.
        """
        return self.actions.click(self.sign_in_link)

    def search_for_products(self, search_query: str):
        """
        Search for products by entering keywords into the search input and submitting the search. Use this method to execute a product search from the homepage by specifying a search term, after which the user is navigated to a results or catalog page listing relevant products. Use this method when a manual test step requires searching for product. It completes the related multi-control interaction as one reusable business operation.

        Args:
            search_query: The keyword or phrase to search for products.
        """
        self.actions.fill(self.product_search_input, search_query)
        return self.actions.click(self.search_button)

    def logout(self):
        """
        Log out the currently signed-in user from their account using the homepage. Use this method when a manual test step requires ending the current user session from the main navigation. The expected outcome is the user being signed out on completion. Use this method when a manual test step requires signing out of user session.
        """
        return self.actions.click(self.logout_button)

    def verify_just_dropped_heading(self):
        """
        Verify the heading on PAGE_6d0fd18e438790c9 using the observed expected value/text 'Just dropped'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Just dropped
        """
        return self.actions.expect_visible(self.just_dropped)
    def verify_trending_picks_heading(self):
        """
        Verify the heading on PAGE_6d0fd18e438790c9 using the observed expected value/text 'Trending picks'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: Trending picks
        """
        return self.actions.expect_visible(self.trending_picks)
    def verify_about_shopverse_heading(self):
        """
        Verify the heading on PAGE_6d0fd18e438790c9 using the observed expected value/text 'About Shopverse'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: About Shopverse
        """
        return self.actions.expect_visible(self.about_shopverse)
    def verify_new_arrivals_heading(self):
        """
        Verify the heading on PAGE_6d0fd18e438790c9 using the observed expected value/text 'New Arrivals'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: New Arrivals
        """
        return self.actions.expect_visible(self.new_arrivals)
    def verify_new_balance_spotlight_heading(self):
        """
        Verify the heading on PAGE_6d0fd18e438790c9 using the observed expected value/text 'New Balance spotlight'. Use this method when a manual test step needs to validate page heading (heading). It confirms that the expected UI evidence is visible.

        Expected evidence: New Balance spotlight
        """
        return self.actions.expect_visible(self.new_balance_spotlight)

    # Generated deterministically from synchronized M2A Application Knowledge evidence.
