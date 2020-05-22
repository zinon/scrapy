function main(splash)
    assert(splash:go(splash.args.url))
    splash:wait(5)

    local get_element_dim_by_xpath = splash:jsfunc([[
        function(xpath) {
            var element = document.evaluate(xpath, document, null,
                XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            var element_rect = element.getClientRects()[0];
            return {"x": element_rect.left, "y": element_rect.top}
        }
    ]])

    -- -- Find the YEAR drop down
    local year_drop_dimensions = get_element_dim_by_xpath(
        '//h2[contains(@class, "label ") and contains(text(), "Year ")]')
    splash:set_viewport_full()
    splash:mouse_click(year_drop_dimensions.x, year_drop_dimensions.y)
    splash:wait(1.5)

    -- -- Clicks the 202X year
    local year_dimensions = get_element_dim_by_xpath(
        '//li[contains(@data-value, "2020")]/span')
    splash:set_viewport_full()
    splash:mouse_click(year_dimensions.x, year_dimensions.y)
    splash:wait(5)

    -- Find the MAKE drop down
    local make_drop_dimensions = get_element_dim_by_xpath(
        '//h2[contains(@class, "label ") and contains(text(), "Make ")]')
    splash:set_viewport_full()
    splash:mouse_click(make_drop_dimensions.x, make_drop_dimensions.y)
    splash:wait(1.5)

    -- Clicks the Toyota make
    local make_dimensions = get_element_dim_by_xpath(
        '//li[contains(@data-filters, "make_toyota")]/span')
    splash:set_viewport_full()
    splash:mouse_click(make_dimensions.x, make_dimensions.y)
    splash:wait(5)

    return splash:html()
end





function main(splash)
    assert(splash:go(splash.args.url))
    splash:wait(5)

    local get_element_dim_by_xpath = splash:jsfunc([[
        function(xpath) {
            var element = document.evaluate(xpath, document, null,
                XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            var element_rect = element.getClientRects()[0];
            return {"x": element_rect.left, "y": element_rect.top}
        }
    ]])

    -- -- Find the YEAR drop down
    local year_drop_dimensions = get_element_dim_by_xpath(
        '//h2[contains(@class, "label ") and contains(text(), "Year ")]')
    splash:set_viewport_full()
    splash:mouse_click(year_drop_dimensions.x, year_drop_dimensions.y)
    splash:wait(1.5)

    -- -- Clicks the 202X year
    local year_dimensions = get_element_dim_by_xpath(
        '//li[contains(@data-value, "2020")]/span')
    splash:set_viewport_full()
    splash:mouse_click(year_dimensions.x, year_dimensions.y)
    splash:wait(5)

    -- Find the MAKE drop down
    local make_drop_dimensions = get_element_dim_by_xpath(
        '//h2[contains(@class, "label ") and contains(text(), "Make ")]')
    splash:set_viewport_full()
    splash:mouse_click(make_drop_dimensions.x, make_drop_dimensions.y)
    splash:wait(1.5)

    -- Clicks the Toyota make
    local make_dimensions = get_element_dim_by_xpath(
        '//li[contains(@data-filters, "make_toyota")]/span')
    splash:set_viewport_full()
    splash:mouse_click(make_dimensions.x, make_dimensions.y)
    splash:wait(5)

    next_button = splash:select("*[class='page-next ']")
    next_button.mouse_click()
    splash:wait(4)
    return {
        url = splash:url(),
        html = splash:html()
    }
end





function main(splash)
    assert(splash:go(splash.args.url))
    splash:wait(5)

    next_button = splash:select("*[class='page-next ']")
    next_button.mouse_click()
    splash:wait(4)
    return {
        url = splash:url(),
        html = splash:html()
    }
end