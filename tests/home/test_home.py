from modules.home.pages.home import HomePage


def test_home_page_load(authenticated_page):
    """Verify home page loads successfully"""
    home = HomePage(authenticated_page)
    home.wait_for_home_to_load()


def test_expand_project_from_home(authenticated_page):
    """Verify project can be searched and expanded"""
    home = HomePage(authenticated_page)

    home.wait_for_home_to_load()
    home.search_project("Core QA Only")
    home.expand_project("Core QA Only")

    # Verify project is visible in page content
    assert "Core QA Only" in authenticated_page.content()
