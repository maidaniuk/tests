import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
URI = "https://mate.academy"

def get_links_courses(URI: str):
    driver.get(url=URI)
    WebDriverWait(driver=driver, timeout=2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-qa='header-courses-dropdown-button']"))).click()
    return get_elements_by_css_selector(driver, "div[data-qa='header-courses-dropdown']", "a[class*='DropdownProfessionsItem_link__4NmVV hide-for-large']", "href")    

def get_element_by_css_selector(driver: str, css_selector: str, attribute: str):
    return WebDriverWait(driver=driver, timeout=2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))).get_attribute(attribute)

def get_elements_by_css_selector(driver: str, css_selector_out: str, css_selector_in: str, attribute: str, lists = []):
    elements_by_selector = []
    if (len(lists) > 0):
        elements = lists
    else:
        elements = WebDriverWait(driver=driver, timeout=2).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector_out)))
    for elem in elements:
        element_in = elem.find_elements(By.CSS_SELECTOR, css_selector_in)
        if len(element_in) > 0:
            for e in element_in:
                elements_by_selector.append(e.get_attribute(attribute))
    return elements_by_selector

def get_courses_info(URI: str) -> None:
    course_properties = {}
    all_courses = {}
    link_courses = get_links_courses(URI)

    for link in link_courses:
        index_course = link.rpartition('/')[-1]  
        driver.get(url=link)
        course_duration = WebDriverWait(driver=driver, timeout=2).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[ text() = 'Тривалість']/parent::div")))
        course_properties['name'] = get_element_by_css_selector(driver, "div[class=CoverHeadingLight_heading__BNTR_] h1", "textContent")
        course_properties['about'] = get_element_by_css_selector(driver, "p[class*=SalarySection_aboutProfession__C6ftM]", "textContent")
        course_properties['format'] = get_elements_by_css_selector(driver, "div[class*=TableColumnsView_headerCellGray__jDSLp]", "p", "textContent")
        course_properties['modules_count'] = len(WebDriverWait(driver=driver, timeout=2).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p[class*=CourseModulesList_topicName__7vxtk]"))))
        course_properties['topics_count'] = get_element_by_css_selector(driver, "div[class*=CourseProgram_cards__CD13X] p", "textContent")
        course_properties['duration'] = get_elements_by_css_selector(driver, "div", "div[class*=TableColumnsView_tableCellGray__4hadg]", "textContent", course_duration)

        all_courses[index_course] = course_properties
        course_properties = {}
    print(all_courses)
            
def main() -> None:
    get_courses_info(URI)

if __name__ == "__main__":
    main()